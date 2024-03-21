import pytest
import subprocess
import uuid
import datetime
import requests  # type: ignore[import-untyped]
import time
import os

url = "http://localhost:8000"
post_ecg_url = url + "/electrocardiograms"
health_url = url + "/health"
admin_create_user_url = url + "/admin/user"
login_user = url + "/users/login"


def wait_for_service(url, timeout=30):
    start_time = time.time()
    while True:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                break
        except requests.ConnectionError:
            pass  # Service not ready yet

        if time.time() - start_time > timeout:
            raise TimeoutError("Service did not become ready in time")

        time.sleep(1)


@pytest.fixture(scope="session", autouse=True)
def docker_compose_environment():
    subprocess.run(["docker-compose", "up", "-d"], check=True)

    # Wait for the environment to be ready
    wait_for_service(health_url)
    time.sleep(5)

    yield

    # For debugging purposes
    # logs = subprocess.run(["docker-compose", "logs", "api"], capture_output=True, text=True)
    # print(logs.stdout)

    subprocess.run(["docker-compose", "down"], check=True)


def post_payload_generator():
    return {
        "id": str(uuid.uuid4()),
        "date": datetime.datetime.utcnow().strftime("%Y-%m-%d"),
        "leads": [
            {"name": "I", "num_samples": 6, "signal": [0, 1, -2, 3, 4, 5]},
            {"name": "II", "num_samples": 6, "signal": [0, 1, -2, 3, -4, 5]},
        ],
    }


def _create_http_headers(token):
    return {"Content-Type": "application/json", "Authorization": f"Bearer {token}"}


def _get_jwt():
    headers = _create_http_headers(os.getenv("admin_password"))
    username = "test"
    password = "test"
    payload = {"username": username, "password": password}

    response = requests.post(admin_create_user_url, json=payload, headers=headers)
    response = requests.post(login_user, json=payload)
    jwt = response.json()["jwt_login"]
    return jwt


def test_electrocardiogram():
    headers = _create_http_headers(_get_jwt())
    payload = post_payload_generator()
    response = requests.post(post_ecg_url, json=payload, headers=headers)
    get_insights_url = url + f"/electrocardiograms/{payload['id']}/insights"
    # Sleep to make sure the event is processed
    time.sleep(1)
    response = requests.get(get_insights_url, headers=headers)

    assert response.json()[0]["zero_crossings"] == 2
    assert response.json()[1]["zero_crossings"] == 4
