import logging
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR
import traceback
from typing import Callable, Awaitable


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()  # Output to console
    ]
)

logger = logging.getLogger(__name__)


class LoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware to log incoming requests and outgoing responses
    """
    async def dispatch(self, request: Request, call_next: Callable[..., Awaitable]):
        # Log incoming request
        logger.info(f"Incoming request: {request.method} {request.url}")
        
        try:
            response = await call_next(request)
            
            # Log response status
            logger.info(f"Response status: {response.status_code}")
            
            return response
        except Exception as e:
            # Log exceptions
            logger.error(f"Exception occurred: {str(e)}")
            logger.error(traceback.format_exc())
            
            # Re-raise the exception to be handled by the global exception handler
            raise


def add_exception_handlers(app):
    """
    Add global exception handlers to the FastAPI app
    """
    @app.exception_handler(HTTPException)
    async def http_exception_handler(request, exc):
        logger.warning(f"HTTPException: {exc.status_code} - {exc.detail}")
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": "HTTP Exception",
                "status_code": exc.status_code,
                "message": exc.detail
            }
        )
    
    @app.exception_handler(Exception)
    async def general_exception_handler(request, exc):
        logger.error(f"Unhandled exception: {str(exc)}")
        logger.error(traceback.format_exc())
        return JSONResponse(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": "Internal Server Error",
                "status_code": HTTP_500_INTERNAL_SERVER_ERROR,
                "message": "An unexpected error occurred"
            }
        )


def setup_logging_and_error_handling(app):
    """
    Set up logging and error handling for the application
    """
    # Add logging middleware
    app.add_middleware(LoggingMiddleware)
    
    # Add exception handlers
    add_exception_handlers(app)