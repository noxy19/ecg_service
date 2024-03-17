FROM python:3.11-slim
RUN apt-get update && apt-get install

RUN pip install poetry==1.8.2


WORKDIR /app
ENV PYTHONPATH "${PYTHONPATH}:/app/src"
COPY pyproject.toml poetry.lock* ./
RUN poetry config virtualenvs.create false
RUN poetry install --without dev --no-interaction --no-root

COPY src ./src

