import logging

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.config import CONFIG
from app.modules import admin, juice
from app.modules.auth import LoginRequest, create_access_token, verify_password

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Fruit Juice API", version="1.0.0")

if CONFIG.ENV() == "DEV":
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(juice.router)
app.include_router(admin.router)


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.post("/login")
async def login(request: LoginRequest):
    if not verify_password(request.password, CONFIG.ADMIN_PASSWORD_HASH()):
        logger.warning("Failed login attempt")
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(subject="admin")
    logger.info("Successful admin login")
    return {"access_token": access_token, "token_type": "bearer"}


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
