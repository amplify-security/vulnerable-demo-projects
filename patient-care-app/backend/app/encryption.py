from cryptography.fernet import Fernet
from app.config import settings


def get_fernet():
    return Fernet(settings.PHI_ENCRYPTION_KEY.encode())


def encrypt_phi(value: str) -> bytes:
    if not value:
        return b""
    f = get_fernet()
    return f.encrypt(value.encode())


def decrypt_phi(value: bytes) -> str:
    if not value:
        return ""
    f = get_fernet()
    return f.decrypt(value).decode()
