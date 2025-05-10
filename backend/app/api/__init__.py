# backend/app/api/__init__.py
from fastapi import APIRouter
from .routes import router

# Export the router
__all__ = ["router"]