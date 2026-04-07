"""
JWT Authentication Utilities
Handles token generation, validation, and password hashing
"""

from datetime import datetime, timedelta, timezone
from typing import Optional
import os
import secrets
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, Depends, Header

# Configuration
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7"))

# Password hashing - using argon2 (no 72-byte password limit like bcrypt)
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


# ============================================================================
# Password Functions
# ============================================================================

def hash_password(password: str) -> str:
    """Hash a password using bcrypt"""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against its hash"""
    return pwd_context.verify(plain_password, hashed_password)


# ============================================================================
# JWT Token Functions
# ============================================================================

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create JWT access token"""
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create JWT refresh token"""
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    
    to_encode.update({"exp": expire, "type": "refresh"})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str) -> dict:
    """Verify and decode JWT token"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


def get_current_user_id(authorization: Optional[str] = Header(None)) -> int:
    """Extract and validate user ID from Bearer token"""
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header required")
    
    try:
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            raise HTTPException(status_code=401, detail="Invalid authentication scheme")
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid authorization header")
    
    payload = verify_token(token)
    
    # Check token type (should not be refresh token)
    if payload.get("type") == "refresh":
        raise HTTPException(status_code=401, detail="Refresh token cannot be used for API access")
    
    return int(payload.get("sub"))


# ============================================================================
# Password Reset Functions
# ============================================================================

def generate_reset_code() -> str:
    """Generate a random reset code"""
    return secrets.token_urlsafe(32)[:10].upper()


def is_reset_code_valid(reset_code_expiry: Optional[str]) -> bool:
    """Check if reset code has expired"""
    if not reset_code_expiry:
        return False
    
    try:
        expiry = datetime.fromisoformat(reset_code_expiry)
        return datetime.now(timezone.utc) < expiry
    except (ValueError, TypeError):
        return False
