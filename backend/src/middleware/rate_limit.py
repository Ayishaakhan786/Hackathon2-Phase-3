"""
Rate limiting implementation for chat API endpoints
"""
import time
import threading
from collections import defaultdict, deque
from typing import Dict, Optional


class RateLimiter:
    """
    A simple rate limiter that tracks requests by user ID and IP address
    """
    
    def __init__(self):
        # Store request times for each user
        self.user_requests = defaultdict(deque)
        # Store request times for each IP
        self.ip_requests = defaultdict(deque)
        # Thread lock for thread safety
        self._lock = threading.Lock()
    
    def is_allowed(
        self, 
        user_id: str, 
        ip_address: str, 
        user_limit: int = 100,  # 100 requests per minute per user
        user_window: int = 60,  # 60 seconds window
        ip_limit: int = 1000,   # 1000 requests per minute per IP
        ip_window: int = 60     # 60 seconds window
    ) -> Dict[str, bool]:
        """
        Check if a request is allowed based on rate limits
        
        Args:
            user_id: The user ID making the request
            ip_address: The IP address making the request
            user_limit: Max requests per user per time window
            user_window: Time window in seconds for user limit
            ip_limit: Max requests per IP per time window
            ip_window: Time window in seconds for IP limit
            
        Returns:
            Dictionary with 'user_allowed' and 'ip_allowed' boolean values
        """
        current_time = time.time()
        
        with self._lock:
            # Check user rate limit
            user_req_times = self.user_requests[user_id]
            # Remove requests older than the time window
            while user_req_times and current_time - user_req_times[0] > user_window:
                user_req_times.popleft()
            
            user_allowed = len(user_req_times) < user_limit
            if user_allowed:
                user_req_times.append(current_time)
            
            # Check IP rate limit
            ip_req_times = self.ip_requests[ip_address]
            # Remove requests older than the time window
            while ip_req_times and current_time - ip_req_times[0] > ip_window:
                ip_req_times.popleft()
            
            ip_allowed = len(ip_req_times) < ip_limit
            if ip_allowed:
                ip_req_times.append(current_time)
            
            return {
                "user_allowed": user_allowed,
                "ip_allowed": ip_allowed
            }


# Global rate limiter instance
rate_limiter = RateLimiter()


def check_rate_limit(user_id: str, ip_address: str) -> Dict[str, bool]:
    """
    Check rate limits for a given user and IP
    
    Args:
        user_id: The user ID making the request
        ip_address: The IP address making the request
        
    Returns:
        Dictionary with rate limit status
    """
    return rate_limiter.is_allowed(
        user_id=user_id,
        ip_address=ip_address
    )


def get_remaining_limits(user_id: str, ip_address: str) -> Dict[str, int]:
    """
    Get the number of remaining requests for user and IP
    
    Args:
        user_id: The user ID
        ip_address: The IP address
        
    Returns:
        Dictionary with remaining request counts
    """
    current_time = time.time()
    
    with rate_limiter._lock:
        # Calculate remaining user requests
        user_req_times = rate_limiter.user_requests[user_id]
        while user_req_times and current_time - user_req_times[0] > 60:  # 60-second window
            user_req_times.popleft()
        user_remaining = max(0, 100 - len(user_req_times))  # Assuming 100 per minute limit
        
        # Calculate remaining IP requests
        ip_req_times = rate_limiter.ip_requests[ip_address]
        while ip_req_times and current_time - ip_req_times[0] > 60:  # 60-second window
            ip_req_times.popleft()
        ip_remaining = max(0, 1000 - len(ip_req_times))  # Assuming 1000 per minute limit
        
        return {
            "user_remaining": user_remaining,
            "ip_remaining": ip_remaining
        }