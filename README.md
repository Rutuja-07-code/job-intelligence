# Job Intelligence Backend

A production-style backend API for managing users, companies, and job opportunities.

This project was built to learn and implement real backend engineering concepts including REST APIs, authentication, authorization, PostgreSQL, SQLAlchemy, database migrations, automated testing, Docker, and cloud deployment.

## 🚀 Live Demo

### API Documentation
https://job-intelligence-cuml.onrender.com/docs

### Live Backend
https://job-intelligence-cuml.onrender.com

The API is publicly deployed and can be explored through the Swagger UI.

---

## ✨ Features

- User registration and login
- Secure password hashing
- JWT-based authentication
- Protected API endpoints
- User-based authorization
- Company management
- Job management
- Company-job relationships
- User ownership of jobs
- PostgreSQL database
- SQLAlchemy ORM
- Alembic database migrations
- Automated API testing with Pytest
- Dockerized application
- Production deployment
- Interactive Swagger/OpenAPI documentation

---

## 🛠️ Tech Stack

### Backend
- Python
- FastAPI
- SQLAlchemy
- Pydantic
- PostgreSQL
- Alembic

### Authentication
- JWT
- Passlib
- bcrypt
- OAuth2 Bearer Authentication

### Testing
- Pytest
- FastAPI TestClient

### Deployment
- Docker
- Render
- Supabase PostgreSQL

### Development Tools
- Git
- GitHub
- Swagger / OpenAPI

---

## 🏗️ Architecture

```text
                    Client
                      │
                      ▼
                  FastAPI
                      │
              ┌───────┴───────┐
              │               │
              ▼               ▼
          Routers          Dependencies
              │               │
              ▼               ▼
          Services      Authentication
              │
              ▼
        Repositories
              │
              ▼
          SQLAlchemy
              │
              ▼
         PostgreSQL
```

---

## 🔐 Authentication Flow

The API uses JWT-based authentication.

```text
User
 │
 ├── Register
 │      │
 │      ▼
 │   Password Hash
 │      │
 │      ▼
 │   PostgreSQL
 │
 └── Login
        │
        ▼
    Verify Password
        │
        ▼
    Generate JWT
        │
        ▼
   Protected Endpoints
```

Protected requests use:

```text
Authorization: Bearer <access_token>
```

The backend validates the JWT and identifies the authenticated user before allowing access to protected resources.

---

## 🔒 Authorization

The application implements user-based resource ownership.

For example:

```text
User A
  │
  └── Creates Job A

User B
  │
  └── Cannot access Job A
```

This prevents users from accessing jobs that belong to another user.

---

## 🗄️ Database Design

PostgreSQL is used as the primary database.

### Main Tables

```text
users
  │
  └──────────────┐
                 │
                 ▼
                jobs
                 │
                 │
                 ▼
             companies
```

### Users
Stores:
- User ID
- Email
- Password hash
- Created timestamp

### Companies
Stores:
- Company ID
- Company name
- Website
- Created timestamp

### Jobs
Stores:
- Job ID
- Company ID
- User ID
- Job title
- Description
- Location
- Created timestamp

Foreign keys are used to maintain relationships between related records.

---

## 🔄 Database Migrations

Alembic is used to manage database schema changes.

Migration history includes:

```text
Initial database
      ↓
Add job location
      ↓
Add users
      ↓
Add user ownership to jobs
```

Apply migrations with:

```bash
alembic upgrade head
```

Check the current migration:

```bash
alembic current
```

---

## 🧪 Testing

The project includes automated API tests for important backend behavior.

Tests cover:
- User registration
- Duplicate registration
- Successful login
- Incorrect password
- Invalid JWT
- Valid JWT
- User-specific job access
- Company creation

Run the test suite:

```bash
python -m pytest
```

---

## 📂 Project Structure

```text
job-intelligence/
│
├── app/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── dependencies.py
│   │
│   ├── routers/
│   │   ├── companies.py
│   │   ├── jobs.py
│   │   └── users.py
│   │
│   ├── services/
│   │   ├── company_service.py
│   │   ├── job_service.py
│   │   └── user_service.py
│   │
│   ├── repositories/
│   │   ├── company_repository.py
│   │   ├── job_repository.py
│   │   └── user_repository.py
│   │
│   └── utils/
│       └── security.py
│
├── alembic/
│   └── versions/
│
├── tests/
│   ├── conftest.py
│   └── test_users.py
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .dockerignore
├── .gitignore
└── README.md
```

---

## 🌐 API Endpoints

### Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/users/register` | Register a new user |
| POST | `/users/login` | Login and receive JWT token |

### Companies

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/companies` | Create a company |
| GET | `/companies` | Get companies |

### Jobs

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/companies/{company_id}/jobs` | Create a job for a company |
| GET | `/jobs` | Get jobs belonging to the authenticated user |
| GET | `/companies/{company_id}/jobs` | Get jobs for a company |

For the complete API specification and interactive testing:

**Swagger UI:**  
https://job-intelligence-cuml.onrender.com/docs

---

## 🐳 Running Locally

### 1. Clone the repository

```bash
git clone https://github.com/Rutuja-07-code/job-intelligence.git
cd job-intelligence
```

### 2. Create a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file:

```env
DATABASE_URL=your_database_url
JWT_SECRET_KEY=your_secret_key
JWT_ALGORITHM=HS256
```

Do not commit `.env` to GitHub.

### 5. Run database migrations

```bash
alembic upgrade head
```

### 6. Start the application

```bash
uvicorn app.main:app --reload
```

The API will run at:

```text
http://localhost:8000
```

Swagger documentation:

```text
http://localhost:8000/docs
```

---

## 🐳 Running with Docker

Build and start the application:

```bash
docker compose up --build
```

The API will be available at:

```text
http://localhost:8000
```

Swagger documentation:

```text
http://localhost:8000/docs
```

---

## ☁️ Deployment

The backend is deployed using Render and Supabase.

```text
                GitHub
                   │
                   ▼
                Render
                   │
                   ▼
          FastAPI Docker Container
                   │
                   ▼
          Supabase PostgreSQL
```

### Deployment Stack

- **Source Code:** GitHub
- **Application:** FastAPI
- **Containerization:** Docker
- **Backend Hosting:** Render
- **Database:** Supabase PostgreSQL
- **Database Migration:** Alembic

### Production API

https://job-intelligence-cuml.onrender.com

### Production Swagger

https://job-intelligence-cuml.onrender.com/docs

---

## 📚 What I Learned

Through this project, I implemented and learned:

- REST API development with FastAPI
- API routing and HTTP methods
- Request and response validation with Pydantic
- SQLAlchemy ORM
- PostgreSQL database design
- Primary keys and foreign keys
- One-to-many relationships
- Repository and service layer architecture
- Dependency injection
- Password hashing
- JWT authentication
- OAuth2 Bearer authentication
- User authorization
- Resource ownership
- Alembic migrations
- Automated API testing with Pytest
- Test database configuration
- Docker and Docker Compose
- Environment variable management
- Swagger/OpenAPI documentation
- Git and GitHub workflow
- Cloud deployment

---

## 🎯 Project Goal

The main goal of this project was to build a complete backend system while understanding how the individual backend components work together.

The project follows this flow:

```text
HTTP Request
     ↓
FastAPI Router
     ↓
Authentication / Validation
     ↓
Service Layer
     ↓
Repository Layer
     ↓
SQLAlchemy
     ↓
PostgreSQL
     ↓
Response
```

This project helped me move from writing individual Python programs to understanding how a real backend application is structured, tested, containerized, and deployed.

---

## 👨‍💻 Author

**Rutuja Barde**

Backend / Software Engineering Student

GitHub:  
https://github.com/Rutuja-07-code
