#!/usr/bin/env python3
"""
Module for encrypting and storing user data securely
"""

import bcrypt
from typing import Tuple

def hash_password(password: str) -> bytes:
    """
    Hashes a password using bcrypt and returns the hashed password as bytes.
    """
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode(), salt)
    return hashed

def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    Checks if a password matches the hashed password.
    """
    return bcrypt.checkpw(password.encode(), hashed_password)

if __name__ == "__main__":
    # Example usage
    plain_password = "my_secure_password"
    hashed_pw = hash_password(plain_password)
    print(f"Password: {plain_password}")
    print(f"Hashed: {hashed_pw}")

    # Validate the password
    if is_valid(hashed_pw, plain_password):
        print("Password is valid!")
    else:
        print("Invalid password.")
