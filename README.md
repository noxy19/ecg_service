# ECG service

The ECG Insight Microservice is an API designed to analyze electrocardiograms (ECG) by processing submissions and calculating zero crossings in the signal of each lead.

## Prerequisites

Before running the microservice, ensure you have the following installed:

- Docker
- Docker Compose

## How to Run It


Copy the .env.template file to a .env file. The template contains the necessary default values for running the application locally.

```bash
cp .env.template .env
```

Use Docker Compose to build and launch the microservice.

```bash
docker-compose up
```

To test the service, access the Swagger UI at `localhost:8000/docs`.

- **Create a User**: Use `/admin/user` with `admin_password` from `.env` for authentication.
- **Login**: Obtain a JWT via `/users/login` for further requests.
- **Submit ECG**: Post ECG data to `/electrocardiograms`, using the JWT for authorization.
- **Get Insights**: Retrieve zero crossings by hitting `/electrocardiograms/{ecg-id}/insights` with the ECG ID.


## Running test locally
To run tests, ensure Python and Poetry are installed. Follow these steps to set up and execute tests:

- **Install Dependencies**: First, execute `poetry install` in your project directory. This command installs all necessary dependencies as defined in your pyproject.toml file.
- **Activate Virtual Environment**: After installing the dependencies, activate the project's virtual environment by running `poetry shell`.
- **Run Tests**: With the virtual environment activated, you can now run `pytest` directly to execute the tests.

This method ensures that all dependencies are installed and the correct environment is activated for running your tests.

## Software Architecture Decisions

Our application is designed using the Hexagonal Architecture (also known as Ports and Adapters) to promote separation of concerns and enhance maintainability and scalability. It organizes into three primary layers:

- **Application Layer**: Acts as the mechanism through which external clients interact with our application, orchestrating the flow of data to and from the domain layer, and directing the domain layer to perform operations based on external requests.

- **Domain Layer**: Contains the core business logic, and entities of the application. This layer is kept independent of the external world, ensuring that our business logic can operate regardless of the infrastructure or application layers' implementations.

- **Infrastructure Layer**: Implements the ports defined by the domain layer. It includes external components such as databases, web frameworks, and messaging systems, in our case, PostgreSQL for relational data persistence, Amazon SQS for message queuing and FastAPI as our web framework.

The architecture comprises two services:

- **API Service**: Facilitates interactions with external clients, providing endpoints for submitting ECG data and retrieving insights.

- **Queue Consumer Service**: Processes ECG data asynchronously, utilizing SQS for managing workload distribution and scalability.

This structure allows for clear separation between business logic, application logic, and external interfaces, promoting ease of testing, maintenance, and future scalability.