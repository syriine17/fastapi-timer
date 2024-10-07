# FastAPI Timer Service

A FastAPI service for executing delayed tasks with timer functionality. This project allows users to set timers and retrieve them, supporting horizontal scalability and designed with PEP8 compliance in mind.

## Table of Contents

- [Features](#features)
- [Technologies Used](#technologies-used)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
  - [Set Timer](#set-timer)
  - [Get Timer](#get-timer)
- [Running Tests](#running-tests)
- [API Documentation](#api-documentation)
  - [How to Use the Swagger UI](#how-to-use-the-swagger-ui)
  - [Example Endpoints](#example-endpoints)

## Features

- Set timers with specified hours, minutes, and seconds.
- Retrieve timer details.
- UUID-based identification for timers.
- Scalable architecture using Docker.

## Technologies Used

- **FastAPI**: A modern web framework for building APIs.
- **PostgreSQL**: A powerful relational database.
- **Alembic**: For database migrations.
- **Docker**: For containerization.

## Prerequisites

Make sure you have the following installed:

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)
- Python 3.8 or later (for local development)

## Installation

1. **Clone the repository**:

   ```sh
   git clone https://github.com/yourusername/fastapi-timer.git
   cd fastapi-timer
   ```

2. **Build the Docker containers**:

    ```sh
    docker-compose build
    ```

3. **Start the application and the database**:

    ```sh
    docker-compose up
    ```
4.  ** Run migrations to create the database tables**:

    ```sh
    docker-compose exec fastapi-app alembic upgrade head
    ```

5. **Usage**
Set Timer
Send a POST request to set-timer with a JSON body containing url, hours, minutes, and seconds.

    Example request:

    ```sh
    curl -X POST "http://localhost:8000/timer" \
    -H "Content-Type: application/json" \
    -d '{"url": "http://example.com", "hours": 1, "minutes": 30, "seconds": 15}'
    ```

Get Timer
Send a GET request to get-timer/{timer_id} to retrieve the timer details.

    Example request:

    ```sh
    curl "http://localhost:8000/timer/aac29dae4b61"
    ```

6. **To run the tests, execute the following command:**

    ```sh
    docker-compose exec fastapi-app pytest /app/tests/
    ```

7. **API Documentation**
FastAPI provides automatic interactive API documentation using Swagger UI. You can access it at:

Swagger UI
How to Use the Swagger UI
Navigate to the URL: Open your web browser and go to http://localhost:8000/docs.

Explore the Endpoints: You will see a list of all available API endpoints.

For POST requests, enter the request body in JSON format.
For GET requests, enter path parameters directly.
Execute Requests: After filling in the necessary fields, click on the "Execute" button to send the request and see the response.

Example Endpoints
Set Timer:

POST /timer
Request Body:
json
{
  "url": "http://example.com",
  "hours": 1,
  "minutes": 30,
  "seconds": 15
}
Get Timer:

GET /timer/{timer_id}
