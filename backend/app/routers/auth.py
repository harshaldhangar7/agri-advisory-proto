"""
Authentication Router
Handles user registration, login, token refresh, and logout
"""

from fastapi import APIRouter, Depends, HTTPException, Header
from sqlmodel import Session, select
from typing import Optional
import logging
from datetime import datetime, timezone, timedelta

from ..db import get_engine
from ..models import User, UserCreate, UserLogin, UserResponse, Token, ForgotPasswordRequest, ResetPasswordRequest
from ..auth import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    verify_token,
    get_current_user_id,
    generate_reset_code,
    is_reset_code_valid,
)

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/auth", tags=["auth"])

def get_session():
    """Get database session"""
    engine = get_engine()
    with Session(engine) as session:
        yield session

# ============================================================================
# AUTHENTICATION ENDPOINTS
# ============================================================================

@router.post("/register", response_model=Token)
def register(
    user_data: UserCreate,
    session: Session = Depends(get_session)
):
    """
    Register a new user account
    
    **Request Body:**
    - `username`: str (3-50 characters, unique)
    - `email`: str (valid email, unique)
    - `password`: str (6-100 characters)
    
    **Response:** Returns access token, refresh token, and user info
    """
    try:
        # Check if username already exists
        stmt = select(User).where(User.username == user_data.username)
        existing_user = session.exec(stmt).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Username already exists")
        
        # Check if email already exists
        stmt = select(User).where(User.email == user_data.email.lower())
        existing_email = session.exec(stmt).first()
        if existing_email:
            raise HTTPException(status_code=400, detail="Email already registered")
        
        # Create new user
        user = User(
            username=user_data.username,
            email=user_data.email.lower(),
            password_hash=hash_password(user_data.password)
        )
        
        session.add(user)
        session.commit()
        session.refresh(user)
        
        logger.info(f"User registered: {user.username}")
        
        # Generate tokens
        access_token = create_access_token({"sub": str(user.id)})
        refresh_token = create_refresh_token({"sub": str(user.id)})
        
        return Token(
            access_token=access_token,
            refresh_token=refresh_token,
            user=UserResponse(
                id=user.id,
                username=user.username,
                email=user.email,
                created_at=user.created_at
            )
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Registration error: {e}")
        raise HTTPException(status_code=500, detail="Registration failed")


@router.post("/login", response_model=Token)
def login(
    credentials: UserLogin,
    session: Session = Depends(get_session)
):
    """
    Login with username and password
    
    **Request Body:**
    - `username`: str
    - `password`: str
    
    **Response:** Returns access token, refresh token, and user info
    """
    try:
        # Find user by username
        stmt = select(User).where(User.username == credentials.username)
        user = session.exec(stmt).first()
        
        if not user or not verify_password(credentials.password, user.password_hash):
            logger.warning(f"Failed login attempt: {credentials.username}")
            raise HTTPException(status_code=401, detail="Invalid username or password")
        
        # Generate tokens
        access_token = create_access_token({"sub": str(user.id)})
        refresh_token = create_refresh_token({"sub": str(user.id)})
        
        logger.info(f"User logged in: {user.username}")
        
        return Token(
            access_token=access_token,
            refresh_token=refresh_token,
            user=UserResponse(
                id=user.id,
                username=user.username,
                email=user.email,
                created_at=user.created_at
            )
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Login error: {e}")
        raise HTTPException(status_code=500, detail="Login failed")


@router.post("/refresh", response_model=Token)
def refresh_token(
    session: Session = Depends(get_session),
    authorization: Optional[str] = Header(None)
):
    """
    Refresh access token using refresh token
    
    **Headers:**
    - `Authorization`: "Bearer {refresh_token}"
    
    **Response:** Returns new access token and refresh token
    """
    try:
        if not authorization:
            raise HTTPException(status_code=401, detail="Refresh token required")
        
        try:
            scheme, token = authorization.split()
            if scheme.lower() != "bearer":
                raise HTTPException(status_code=401, detail="Invalid authentication scheme")
        except ValueError:
            raise HTTPException(status_code=401, detail="Invalid authorization header")
        
        # Verify refresh token
        payload = verify_token(token)
        
        # Check if it's a refresh token
        if payload.get("type") != "refresh":
            raise HTTPException(status_code=401, detail="Access token cannot be used for refresh")
        
        user_id = int(payload.get("sub"))
        
        # Get user
        user = session.get(User, user_id)
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        
        # Generate new tokens
        access_token = create_access_token({"sub": str(user.id)})
        new_refresh_token = create_refresh_token({"sub": str(user.id)})
        
        logger.info(f"Token refreshed for user: {user.username}")
        
        return Token(
            access_token=access_token,
            refresh_token=new_refresh_token,
            user=UserResponse(
                id=user.id,
                username=user.username,
                email=user.email,
                created_at=user.created_at
            )
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Token refresh error: {e}")
        raise HTTPException(status_code=400, detail="Invalid refresh token")


@router.post("/logout")
def logout(
    user_id: int = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    """
    Logout user (invalidates tokens on client side)
    
    **Headers:**
    - `Authorization`: "Bearer {access_token}"
    
    **Response:** Success message
    """
    try:
        user = session.get(User, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        logger.info(f"User logged out: {user.username}")
        return {"message": "Logged out successfully"}
    
    except Exception as e:
        logger.error(f"Logout error: {e}")
        raise HTTPException(status_code=500, detail="Logout failed")


@router.get("/me", response_model=UserResponse)
def get_current_user(
    user_id: int = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    """
    Get current authenticated user info
    
    **Headers:**
    - `Authorization`: "Bearer {access_token}"
    
    **Response:** User information
    """
    try:
        user = session.get(User, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        return UserResponse(
            id=user.id,
            username=user.username,
            email=user.email,
            created_at=user.created_at
        )
    
    except Exception as e:
        logger.error(f"Get user error: {e}")
        raise HTTPException(status_code=500, detail="Failed to get user info")


@router.post("/forgot-password")
def forgot_password(
    request: ForgotPasswordRequest,
    session: Session = Depends(get_session)
):
    """
    Request a password reset code
    
    **Request Body:**
    - `email`: str (registered email address)
    
    **Response:** Success message with reset code (for development)
    
    **Note:** In production, this would send an email instead of returning the code
    """
    try:
        # Find user by email
        stmt = select(User).where(User.email == request.email.lower())
        user = session.exec(stmt).first()
        
        if not user:
            # For security, don't reveal if email exists or not
            logger.warning(f"Password reset requested for non-existent email: {request.email}")
            return {"message": "If that email exists, you will receive a reset code"}
        
        # Generate reset code and expiry
        reset_code = generate_reset_code()
        expiry = (datetime.now(timezone.utc) + timedelta(hours=1)).isoformat()
        
        # Update user with reset code
        user.reset_code = reset_code
        user.reset_code_expiry = expiry
        session.add(user)
        session.commit()
        
        logger.info(f"Password reset requested for user: {user.username}")
        
        # In development, return the code. In production, send via email
        return {
            "message": "Password reset code sent to email",
            "reset_code": reset_code  # Remove in production - send via email instead
        }
    
    except Exception as e:
        logger.error(f"Forgot password error: {e}")
        raise HTTPException(status_code=500, detail="Failed to process password reset request")


@router.post("/reset-password")
def reset_password(
    request: ResetPasswordRequest,
    session: Session = Depends(get_session)
):
    """
    Reset password using reset code
    
    **Request Body:**
    - `email`: str (registered email address)
    - `reset_code`: str (code from password reset email)
    - `new_password`: str (new password, 6-72 characters)
    
    **Response:** Success message
    """
    try:
        # Find user by email
        stmt = select(User).where(User.email == request.email.lower())
        user = session.exec(stmt).first()
        
        if not user:
            raise HTTPException(status_code=400, detail="Invalid email or reset code")
        
        # Validate reset code
        if not user.reset_code or user.reset_code != request.reset_code:
            logger.warning(f"Invalid reset code attempt for user: {user.username}")
            raise HTTPException(status_code=400, detail="Invalid email or reset code")
        
        # Check if reset code has expired
        if not is_reset_code_valid(user.reset_code_expiry):
            logger.warning(f"Expired reset code used for user: {user.username}")
            raise HTTPException(status_code=400, detail="Reset code has expired. Please request a new one.")
        
        # Update password and clear reset code
        user.password_hash = hash_password(request.new_password)
        user.reset_code = None
        user.reset_code_expiry = None
        
        session.add(user)
        session.commit()
        
        logger.info(f"Password reset successful for user: {user.username}")
        
        return {"message": "Password reset successful. Please login with your new password."}
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Reset password error: {e}")
        raise HTTPException(status_code=500, detail="Failed to reset password")
