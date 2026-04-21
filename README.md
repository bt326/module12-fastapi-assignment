
**Module 12 FastAPI Assignment**

This project is a FastAPI-based calculator and user management application with automated testing, Docker support, and CI/CD using GitHub Actions.

**Features**

Basic calculator operations: add, subtract, multiply, divide

User registration

User login with hashed passwords

CRUD operations for calculations

Automated unit, integration, and end-to-end tests

Dockerized application

GitHub Actions CI/CD pipeline


Tech Stack

Python

FastAPI

SQLAlchemy

SQLite

Pytest

Playwright

Docker

GitHub Actions


**Run Locally**

pip install -r requirements.txt
uvicorn main:app --reload

**Open in browser:**
http://127.0.0.1:8000/docs

**Run Tests**

pytest

Docker

**Build image:**

docker build -t module12-fastapi-assignment .

**Run container:**

docker run -p 8000:8000 module12-fastapi-assignment

**Links**

GitHub Repo: 
https://github.com/bt326/module12-fastapi-assignment

Docker Hub: 
https://hub.docker.com/r/bhavithaamrutha/module12-fastapi-assignment

## Run Integration Tests
pytest tests/integration/

## Manual API Checks (OpenAPI)
Run app:
uvicorn main:app --reload

Open:
http://127.0.0.1:8000/docs

Use Swagger UI to test:
- /users/register
- /users/login
- /calculations
