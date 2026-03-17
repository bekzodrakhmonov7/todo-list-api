# Todo List API

A RESTful API for managing todo items built with FastAPI, SQLModel, and PostgreSQL.

This project was completed according to the [Todo List API](https://roadmap.sh/projects/todo-list-api) project from roadmap.sh.

> **Note:** Only this README.md file was vibecoded. All the code in this project was written following the roadmap.sh tutorial.

## Project Overview

This is a beginner-friendly REST API that provides todo list functionality with user authentication. Users can register, login, and manage their personal todo items.

## Tech Stack

- **FastAPI** - Modern Python web framework for building APIs
- **SQLModel** - SQL database ORM with Pydantic models
- **PostgreSQL** - Relational database
- **JWT** - JSON Web Tokens for authentication
- **pwdlib** - Password hashing library

## Project Structure

```
.
├── main.py          # FastAPI application with all endpoints
├── models.py        # SQLModel and Pydantic data models
├── db.py            # Database connection and session management
├── config.py        # Configuration and settings from .env
├── security.py      # JWT token and password hashing utilities
├── requirements.txt # Python dependencies
└── .env            # Environment variables (not committed)
```

## API Endpoints

### Health Check
- `GET /health` - Returns service health status

### Authentication
- `POST /auth/register` - Register a new user
- `POST /auth/login` - Login and get access token
- `GET /auth/me` - Get current user info

### Todos (requires Bearer token)
- `POST /todos` - Create a new todo
- `GET /todos` - Get all todos for current user (with pagination)
- `PUT /todos/{todo_id}` - Update a todo
- `DELETE /todos/{todo_id}` - Delete a todo

## Example .env File

Create a `.env` file with the following variables:

```env
POSTGRES_HOST=127.0.0.1
POSTGRES_PORT=5432
POSTGRES_USER=postgres
POSTGRES_PASS=your_secure_password
POSTGRES_DB=todo-api
JWT_HASH=your_jwt_secret_key_min_32_chars
JWT_ALGO=HS256
JWT_EXPIRY_MIN=60
```

## Example Input/Output

### Register a New User

**Request:**
```bash
POST /auth/register
Content-Type: application/json

{
  "username": "johndoe",
  "email": "john@example.com",
  "password": "securepassword123"
}
```

**Response:**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

### Login

**Request:**
```bash
POST /auth/login
Content-Type: application/json

{
  "email": "john@example.com",
  "password": "securepassword123"
}
```

**Response:**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

### Create a Todo

**Request:**
```bash
POST /todos
Authorization: Bearer <your_token>
Content-Type: application/json

{
  "title": "Buy groceries",
  "description": "Milk, eggs, bread, and butter"
}
```

**Response:**
```json
{
  "id": 1,
  "title": "Buy groceries",
  "description": "Milk, eggs, bread, and butter"
}
```

### Get All Todos

**Request:**
```bash
GET /todos?page=1&limit=10
Authorization: Bearer <your_token>
```

**Response:**
```json
{
  "data": [
    {
      "id": 1,
      "title": "Buy groceries",
      "description": "Milk, eggs, bread, and butter"
    }
  ]
}
```

### Update a Todo

**Request:**
```bash
PUT /todos/1
Authorization: Bearer <your_token>
Content-Type: application/json

{
  "title": "Buy groceries and fruits",
  "description": "Milk, eggs, bread, butter, apples, and bananas"
}
```

**Response:**
```json
{
  "id": 1,
  "title": "Buy groceries and fruits",
  "description": "Milk, eggs, bread, butter, apples, and bananas"
}
```

### Delete a Todo

**Request:**
```bash
DELETE /todos/1
Authorization: Bearer <your_token>
```

**Response:** `204 No Content`

## Running the Application

### Prerequisites

- Python 3.11+
- PostgreSQL database

### Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create a `.env` file (see example above)

3. Run the server:
```bash
uvicorn main:app --reload
```

The API will be available at `http://127.0.0.1:8000`

## API Documentation

FastAPI provides automatic interactive API documentation. Once the server is running:

- **Swagger UI:** http://127.0.0.1:8000/docs
- **ReDoc:** http://127.0.0.1:8000/redoc
