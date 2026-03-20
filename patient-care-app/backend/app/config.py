import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    JWT_SECRET: str = os.environ.get("JWT_SECRET", "")
    JWT_ALGORITHM: str = os.environ.get("JWT_ALGORITHM", "HS256")
    JWT_EXPIRATION_MINUTES: int = int(os.environ.get("JWT_EXPIRATION_MINUTES", "30"))
    PHI_ENCRYPTION_KEY: str = os.environ.get("PHI_ENCRYPTION_KEY", "")
    DATABASE_URL: str = os.environ.get("DATABASE_URL", "sqlite:///./patient_care.db")

    def validate(self):
        if not self.JWT_SECRET:
            raise RuntimeError("JWT_SECRET environment variable is required")
        if len(self.JWT_SECRET) < 32:
            raise RuntimeError("JWT_SECRET must be at least 32 characters")
        if not self.PHI_ENCRYPTION_KEY:
            raise RuntimeError("PHI_ENCRYPTION_KEY environment variable is required")


settings = Settings()
