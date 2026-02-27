# Backend Development Guide

## Project Overview

This is a FastAPI-based REST API for a demo project that manages "Fruit Juice" (a riff off of the OWASP Juice Shop Application) that has read endpoints for clients and full CRUD endpoints for admins. Admin endpoints should be secured with JWT-based authentication.

**Tech Stack:**
- FastAPI 0.115.5 (async web framework)
- MySQL with PyMySQL
- Pydantic 2.10.3 (data validation)
- JWT authentication (python-jose 3.3.0)
- bcrypt 4.2.1 (password hashing)
- Uvicorn 0.32.1 (ASGI server)

## Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app initialization, main endpoints
│   ├── config.py            # Environment configuration management
│   ├── database.py          # MongoDB connection setup
│   └── modules/
│       ├── auth.py          # Authentication logic and JWT handling
│       ├── juice.py         # Juice read endpoints (router)
|       |-- admin.py         # Juice Admin CRUD endpoints (router w/ jwt auth)
│       └── domain_models.py # Pydantic models, enums, ObjectId handling
├── generate_password_hash.py # Utility script for bcrypt password hashing
├── requirements.txt
├── .env.example
└── README.md
```

**Module Organization Pattern:**
- **Separation of concerns**: Configuration, database, authentication, and business logic in distinct files
- **Feature-based routing**: Related endpoints grouped in router modules (e.g., `juice.py`)
- **Domain models isolated**: Prevents circular imports, centralizes validation logic

## Coding Conventions

### Import Organization

Always organize imports in this order:
1. Standard library imports
2. Third-party library imports
3. Local application imports

```python
# Example from juice.py
import logging
from app.database import db
from app.modules.domain_models import Juice, CreateJuiceRequest
from app.modules.auth import get_current_user
from pydantic import BaseModel
from fastapi import APIRouter, HTTPException, Depends
```

### Function Definitions

- Use async handlers for I/O-bound operations in main.py: `async def login(...)`
- Use synchronous functions for simple operations: `def create_juice(...)`
- Always include type hints for parameters and return types
- Use Pydantic BaseModel for request/response validation

```python
@router.post("/juices", response_model=Challenge)
def create_challenge(request: CreateJuiceRequest, _: dict = Depends(get_current_user)):
    # Implementation
    pass
```

### Error Handling

- Use `HTTPException` from FastAPI for API errors with appropriate status codes
- Log warnings for authentication failures and not-found scenarios
- Log info for successful operations
- Use try-except for JWT verification with specific exception types
- Exit with `exit(-1337)` for critical database connection failures

```python
# Error handling pattern
try:
    payload = jwt.decode(token, CONFIG.JWT_SECRET(), algorithms=[CONFIG.JWT_ALGORITHM()])
    return payload
except JWTError as e:
    logger.warning(f"JWT verification failed: {e}")
    raise HTTPException(status_code=401, detail="Invalid authentication credentials")
```

### Logging Patterns

Create a module-level logger in every module:

```python
import logging
logger = logging.getLogger(__name__)
```

**Log Levels:**
- `logger.info()`: Successful operations (login, challenge creation, correct flag submission)
- `logger.warning()`: Failed attempts, not-found resources, JWT failures
- `logger.error()`: Configuration issues, database errors

```python
logger.info(f"Created new challenge with ID: {result.inserted_id}")
logger.warning(f"No challenge found with slug: {slug}")
```

## Key Patterns

### Authentication & Authorization

**Dependency Injection Pattern:**
```python
from fastapi import Depends
from app.modules.auth import get_current_user

@router.post("/challenges")
def create_challenge(request: CreateChallengeRequest, _: dict = Depends(get_current_user)):
    # Only authenticated users can access this endpoint
    # The underscore (_) indicates we don't use the user dict
    pass
```

**JWT Token Flow:**
1. User posts password to `/login`
2. Backend verifies password with bcrypt
3. Backend creates JWT token with admin subject
4. Client stores token and includes in `Authorization: Bearer <token>` header
5. Protected endpoints use `Depends(get_current_user)` to validate token

### Configuration Management

Use the static `CONFIG` class pattern for environment variables:

```python
# config.py
class CONFIG:
    @staticmethod
    def MONGO_CONN_STR():
        return os.getenv("MONGO_CONN_STR")
```

**Access throughout codebase:**
```python
from app.config import CONFIG
connection_string = CONFIG.MONGO_CONN_STR()
```

**Critical Variables:**
- `MONGO_CONN_STR`, `MONGO_DATABASE`: Database connection
- `ADMIN_PASSWORD_HASH`: bcrypt hash of admin password
- `JWT_SECRET`: Secret key for JWT encoding/decoding
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Token expiry (default: 1440 = 24 hours)
- `ENV`: Environment (DEV/PROD) - controls CORS middleware

### Database Operations

Access MongoDB collections through the `db` dictionary:

```python
from app.database import db

challenges_collection = db["challenges"]
challenge_data = challenges_collection.find_one({"slug": slug})
```

**Common Operations:**
- `collection.find()`: Returns cursor for all documents
- `collection.find_one(filter)`: Returns single document or None
- `collection.insert_one(document)`: Returns result with `inserted_id`
- `collection.delete_one(filter)`: Deletes matching document

**Pydantic Model Instantiation:**
```python
# Convert MongoDB document to Pydantic model
challenge = Challenge(**challenge_data)
```

### Custom ObjectId Handling

MongoDB's ObjectId requires special handling with Pydantic v2:

```python
from typing import Annotated
from bson import ObjectId
from pydantic import Field

class Challenge(BaseModel):
    id: Annotated[ObjectId, ObjectIdPydanticAnnotation, Field(alias="_id")]
```

The `ObjectIdPydanticAnnotation` handles:
- Validation that string is valid ObjectId
- Serialization to string for JSON responses
- Deserialization from string in requests

### Router Pattern

Create routers in module files and include in main app:

```python
# modules/challenge.py
from fastapi import APIRouter
router = APIRouter()

@router.get("/challenges")
def get_challenges():
    pass

# main.py
from app.modules import challenge
app.include_router(challenge.router)
```

### Pydantic Models

Use Pydantic for all request/response validation:

```python
class CreateChallengeRequest(BaseModel):
    name: str
    description: str
    slug: str
    # ... other fields

@router.post("/challenges", response_model=Challenge)
def create_challenge(request: CreateChallengeRequest):
    challenge_data = request.model_dump()  # Convert to dict
    # Use challenge_data
```

**Enums for Constants:**
```python
from enum import StrEnum

class JuiceType(StrEnum):
    ORANGE = "orange"
    APPLE = "apple"
```

## API Endpoints

### Public Endpoints
- `GET /health`: Health check
- `POST /login`: Admin authentication (returns JWT token)
- `GET /challenges`: List all challenges
- `GET /challenges/{slug}`: Get specific challenge
- `POST /challenges/{challenge_id}/submit`: Submit flag for validation

### Protected Endpoints (Require JWT)
- `POST /challenges`: Create new challenge
- `DELETE /challenges/{slug}`: Delete challenge
- `POST /challenges/{challenge_id}/flags`: Create flag for challenge

**Authentication Header:**
```
Authorization: Bearer <jwt_token>
```

## Development Workflow

### Environment Setup

1. Copy `.env.example` to `.env`
2. Generate password hash:
   ```bash
   python generate_password_hash.py
   ```
3. Generate JWT secret:
   ```bash
   openssl rand -hex 32
   ```
4. Update `.env` with values

### Running the Server

```bash
# Development mode with auto-reload
python app/main.py

# Or with uvicorn directly
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Testing

Currently no automated tests. Manual testing via:
- `requests.http` file (VS Code REST Client extension)
- Swagger UI at `http://localhost:8000/docs`
- ReDoc at `http://localhost:8000/redoc`

## Code Style Guidelines

1. **Type hints everywhere**: All function parameters and return types
2. **Use Pydantic for validation**: Never manually validate request data
3. **Consistent logging**: Module-level logger, appropriate log levels
4. **HTTPException for errors**: Include status code and detail message
5. **Dependency injection**: Use `Depends()` for shared logic (auth, database)
6. **Router organization**: Group related endpoints in separate router modules
7. **Environment variables**: Access only through CONFIG class methods
8. **MySQL patterns**: Direct operations through db dictionary
9. **Async where appropriate**: Use `async def` for I/O-bound operations in main endpoints
10. **Underscore for unused params**: Use `_` when Depends injects value we don't use

## Common Tasks

### Adding a New Endpoint

1. Add route handler to appropriate router module (or create new router)
2. Define Pydantic models for request/response if needed
3. Add authentication if endpoint is protected: `Depends(get_current_user)`
4. Include proper logging and error handling
5. Include router in `main.py` if new

### Adding Authentication to Endpoint

```python
from fastapi import Depends
from app.modules.auth import get_current_user

@router.post("/protected-endpoint")
def my_endpoint(data: RequestModel, _: dict = Depends(get_current_user)):
    # Endpoint logic
    pass
```

### Creating New Pydantic Models

```python
# domain_models.py
from pydantic import BaseModel

class MyModel(BaseModel):
    field1: str
    field2: int
    optional_field: str | None = None
```

### Database Query Pattern

```python
def get_item(item_id: str):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM items WHERE id = %s", (item_id,))
            item_data = cursor.fetchone()
            if not item_data:
                raise HTTPException(status_code=404, detail="Item not found")
            return MyModel(**item_data)
    finally:
        connection.close()
```
