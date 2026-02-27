import os

from dotenv import load_dotenv

load_dotenv()


class CONFIG:
    @staticmethod
    def MYSQL_HOST():
        return os.getenv("MYSQL_HOST", "localhost")

    @staticmethod
    def MYSQL_PORT():
        return int(os.getenv("MYSQL_PORT", "3306"))

    @staticmethod
    def MYSQL_USER():
        return os.getenv("MYSQL_USER", "root")

    @staticmethod
    def MYSQL_PASSWORD():
        return os.getenv("MYSQL_PASSWORD", "local_password")

    @staticmethod
    def MYSQL_DATABASE():
        return os.getenv("MYSQL_DATABASE", "juice_db")

    @staticmethod
    def ADMIN_PASSWORD_HASH():
        return os.getenv("ADMIN_PASSWORD_HASH", "")

    @staticmethod
    def JWT_SECRET():
        # Vulnerable: falls back to a hardcoded weak secret if JWT_SECRET is not set
        return os.getenv("JWT_SECRET", "secret")

    @staticmethod
    def JWT_ALGORITHM():
        return "HS256"

    @staticmethod
    def ACCESS_TOKEN_EXPIRE_MINUTES():
        return int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "1440"))

    @staticmethod
    def ENV():
        return os.getenv("ENV", "DEV")
