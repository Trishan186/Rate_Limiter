
# Rate Limiter Backend

## 1. Project Overview

The Rate Limiter Backend is a Python-based application that controls the number of requests a client can send to a server within a specified period of time.

This project uses the **Token Bucket Algorithm** to manage incoming requests and prevent excessive API usage.

It is developed using Python, FastAPI, and SQLite.

## 2. Objectives

- Control the number of incoming client requests.
- Prevent excessive API requests.
- Protect server resources from overloading.
- Store client rate-limiting information in a database.
- Provide API endpoints to check request status.

## 3. Technologies Used

- Python 3.14
- FastAPI
- SQLite
- SQLAlchemy
- Uvicorn

## 4. Algorithm Used: Token Bucket

The Token Bucket Algorithm is used to control incoming requests.

The configuration is:

- Maximum bucket capacity: 5 tokens
- Token refill rate: 1 token every 12 seconds

### Working Principle

1. Each client is assigned a bucket containing a maximum of 5 tokens.
2. Every incoming request requires one token.
3. If a token is available, the request is accepted and one token is deducted.
4. If no token is available, the request is rejected with HTTP 429 (Too Many Requests).
5. Tokens are replenished automatically over time.
6. The bucket cannot contain more than 5 tokens.

## 5. Database Design

SQLite is used to store client rate-limiting information.

The database table is named `client_rate_limits`.

| Column | Description |
|---|---|
| client_id | Unique identifier of the client |
| tokens | Available tokens |
| last_refill | Last token refill timestamp |

## 6. Project Structure

```text
Rate_Limiter/
│
├── backend/
│   ├── __init__.py
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   └── rate_limiter.py
│
├── requirements.txt
├── .gitignore
└── README.md
```

The SQLite database file is generated automatically when the application runs.

## 7. Installation and Setup

### Step 1: Clone the Repository

```bash
git clone https://github.com/Trishan186/Rate_Limiter.git
```

### Step 2: Navigate to the Project Folder

```bash
cd Rate_Limiter
```

### Step 3: Create a Virtual Environment

```bash
python -m venv venv
```

### Step 4: Activate the Virtual Environment

For Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### Step 5: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 6: Run the Application

```bash
python -m uvicorn backend.main:app --reload
```

The application will start at:

http://127.0.0.1:8000

## 8. API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Checks whether the API is running |
| POST | `/request/{client_id}` | Processes a client request |
| GET | `/rate-limit/{client_id}` | Checks the client's rate-limit status |

## 9. API Testing

FastAPI provides an interactive Swagger UI for testing the endpoints.

Open the following URL in your browser:

http://127.0.0.1:8000/docs

You can test all available API endpoints directly through Swagger UI.

### Expected Behaviour

- Requests are accepted when tokens are available.
- One token is deducted for every accepted request.
- Requests are rejected with HTTP 429 when insufficient tokens are available.
- Tokens are replenished automatically over time.

## 10. Conclusion

This project demonstrates the implementation of a Token Bucket based Rate Limiter using Python and FastAPI.

SQLite provides persistent storage for client information, while the Token Bucket Algorithm controls incoming requests.

The project helps demonstrate API development, database integration, and request management.

---

**Developed by:** Trishan Bera

**Project:** Rate Limiter Backend