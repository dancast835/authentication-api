
## Authentication API

Authentication API is a backend-focused project built with FastAPI that provides secure user authentication using JWT tokens.

The project emphasizes backend architecture, security practices, database integration, and API design rather than frontend development.

---

## Live API Documentation

The Authentication API is deployed on Render.

- **Swagger UI:** https://authentication-api-7mz6.onrender.com/docs
- **Base URL:** https://authentication-api-7mz6.onrender.com
- **Health Check:** https://authentication-api-7mz6.onrender.com/health

## Core features (Phase 1 – MVP)

- User registration with secure password hashing
- User login with credential verification
- JWT token generation for authenticated sessions
- Protected API routes requiring valid authentication
- Token expiration handling
- Structured backend architecture using FastAPI

---

## Tech stack

- **Backend:** Python, FastAPI
- **Database:** PostgreSQL
- **ORM:** SQLModel / SQLAlchemy 
- **Authentication:** JWT (JSON Web Tokens)
- **Password Sercurity:** Passlib / bcrypt
- **Containerization:** Docker

---

## Project structure
```
authentication-api/
|
|-- app/     
|   |-- auth/
|        |-- hash_password.py       #Password hashing 
|           
|   |-- database/                   
|        |-- db.py                  # Database configuration
|
|   |-- routes/
|        |-- routes.py              #FastAPI endpoints   
|
|   |-- main.py
|   |-- config.py   
|
|-- tests/
|     |-- test_auth.py
|     |-- test_db.py
|     |-- test_jwt.py            
|
|-- Dockerfile             # Container configuration
|-- README.md
|-- requirements.txt       # Python dependencies
```

---

## Run locally

1. Clone the repository
```bash
git clone https://github.com/dancast835/authentication-api.git
cd authentication-api

2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

3. Install dependencies
pip install -r requirements.txt

4. Create a .env file
DATABASE_URL=your_database_url
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

5. Run the application
uvicorn app.main:app --reload

6. Open your browser at
👉 http://127.0.0.1:8000/docs
```
---

## Roadmap (Phase 2)

- Role Based Access Control (RBAC)
- Refresh token support
- Email verification system
- Password reset functionality

---

## Author

Luis Daniel Castro Ortiz
📍 Casper, WY
GitHub: https://github.com/dancast835

LinkedIn: https://www.linkedin.com/in/luisdanielcastro
