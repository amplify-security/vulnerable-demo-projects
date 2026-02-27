#!/usr/bin/env python3
import bcrypt


def generate_password_hash(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed.decode("utf-8")


if __name__ == "__main__":
    password = input("Enter password to hash: ")
    hashed = generate_password_hash(password)
    print(f"\nBcrypt hash:\n{hashed}")
    print("\nAdd this to your .env file as ADMIN_PASSWORD_HASH")
