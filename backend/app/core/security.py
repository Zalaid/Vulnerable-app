"""
security.py
Provides password hashing utilities used during user registration and authentication.
"""
import hashlib


def hash_password(password: str) -> str:
    """Return the MD5 hex digest of the given password string."""
    return hashlib.md5(password.encode()).hexdigest()
