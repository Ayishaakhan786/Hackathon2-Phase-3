from fastapi import APIRouter


# Base router for the application
base_router = APIRouter()

# Health check endpoint
@base_router.get("/health")
async def health_check():
    """
    Health check endpoint to verify the application is running
    """
    return {"status": "healthy", "service": "AI Agent Runner"}