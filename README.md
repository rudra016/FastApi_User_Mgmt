## Fastapi usermanagement service
### Overview

This repository contains the User Management microservice, built using FastAPI with asynchronous endpoints, JWT-based authentication, and integrated caching. This service also interacts with RabbitMQ for user validation messages and listens for order updates via WebSocket from another service.

### Features

- FastAPI-based microservice with async endpoints

- JWT authentication for secure access

- Redis caching for improved performance

- RabbitMQ consumer for inter-service communication with a Django service

- WebSocket listener for real-time order updates

- Sentry for Error Logging and Handling

- Swagger API Documentation available at http://127.0.0.1/docs#/

## Installation

Ensure you have the following installed:

 - Python 3.9+

 - Redis

 - RabbitMQ

#### Clone the Repository
``` 
git clone https://github.com/rudra016/FastApi_User_Mgmt.git
cd your-repo
```
#### Install Dependencies

Create a virtual environment and install the required dependencies:

```
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
pip install -r requirements.txt
```
#### Configuration

Environment Variables

Create a .env file in the root directory and configure the following:

```
JWT_SECRET=your_secret_key
JWT_ALGORITHM=HS256
POSTGRE_URL=your_db_url
RABBITMQ_URL=your_rabbitmq_url
DB_PASS=your_db_passwd
SENTRY_DSN=your_sentry_dsn
```

## Running the Application

### Start Redis

Ensure Redis is running:
```
redis-server
```

### Running the FastAPI Server

```
cd user-management-service
uvicorn main:app --reload
```

### Start RabbitMQ

Ensure RabbitMQ is running (in root folder of repo):
```
python rabbitmq_consumer.py
```

### Start Websocket Listener

Ensure RabbitMQ is running (in root folder of repo):
```
python websocket_client.py
```

## API Endpoints

### Authentication
 - ```POST /auth/signup``` - Register a new user

 - ```POST /auth/login``` - Authenticate and receive a JWT token

### Protected Route

 - ```GET /protected ``` - Access user details (requires authentication)

## API Documentation
(Accessable only after running the project locally)
Swagger UI: http://127.0.0.1/docs#/

### Load Testing

You can find the load testing results in ![Load Testing Report](/Locust_2025-02-25-13h55_locustfile.py_http___127.0.0.1_8000.html)

### Deployment

#### Using Docker

To deploy using Docker, build and run the container:
```
docker build -t user-management .
docker run -p 8000:8000 --env-file .env user-management-service
```
#### Using Docker-Compose
```
docker-compose up -d
```

