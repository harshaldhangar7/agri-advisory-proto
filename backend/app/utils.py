import os
from fastapi import HTTPException, Header
from typing import Optional
from datetime import datetime

# API Key validation
def verify_api_key(x_api_key: Optional[str] = Header(None)):
    """Verify API key from request headers"""
    required_key = os.getenv("API_KEY", "default-dev-key")
    
    if not x_api_key:
        raise HTTPException(status_code=401, detail="API key required")
    
    if x_api_key != required_key:
        raise HTTPException(status_code=403, detail="Invalid API key")
    
    return x_api_key

# Standard response wrapper
class ApiResponse:
    """Standardized API response structure"""
    @staticmethod
    def success(data, message: str = "Success"):
        return {
            "status": "success",
            "message": message,
            "data": data,
            "timestamp": datetime.utcnow().isoformat()
        }
    
    @staticmethod
    def error(detail: str, status_code: int = 400):
        return {
            "status": "error",
            "message": detail,
            "data": None,
            "timestamp": datetime.utcnow().isoformat()
        }
