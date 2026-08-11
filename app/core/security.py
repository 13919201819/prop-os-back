from datetime import datetime, timedelta
from typing import Any, Union
import hashlib
import hmac
import os
from jose import jwt
from passlib.context import CryptContext
from app.core.config import settings

try:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
except Exception:
    pwd_context = None



SALT = b"propos_secure_salt_2026"

def get_password_hash(password: str) -> str:
    if not password:
        return ""
    # Also verify with passlib if available, fallback to PBKDF2
    try:
        if pwd_context:
            return pwd_context.hash(password[:71])
    except Exception:
        pass
    key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), SALT, 100000)
    return f"pbkdf2:{key.hex()}"

import bcrypt

def verify_password(plain_password: str, hashed_password: str) -> bool:
    if not plain_password or not hashed_password:
        return False
    # Check bcrypt format ($2b$, $2a$, $2y$)
    if hashed_password.startswith("$2"):
        try:
            return bcrypt.checkpw(plain_password[:71].encode('utf-8'), hashed_password.encode('utf-8'))
        except Exception:
            pass
    # Check PBKDF2 format
    if hashed_password.startswith("pbkdf2:"):
        expected_key = hashed_password.split("pbkdf2:")[1]
        key = hashlib.pbkdf2_hmac('sha256', plain_password.encode('utf-8'), SALT, 100000)
        return hmac.compare_digest(key.hex(), expected_key)
    # Plain check if legacy
    return plain_password == hashed_password




def create_access_token(subject: Union[str, Any], tenant_id: str, role: str, expires_delta: timedelta = None) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode = {
        "exp": expire,
        "sub": str(subject),
        "tenant_id": str(tenant_id),
        "role": role
    }
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt
