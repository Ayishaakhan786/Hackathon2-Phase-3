"""
Performance monitoring for agent response times
"""
import time
import threading
from collections import deque, defaultdict
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import statistics


class PerformanceMonitor:
    """
    Monitor and track performance metrics for agent operations
    """
    
    def __init__(self, max_samples: int = 1000):
        self.max_samples = max_samples
        self.response_times = deque(maxlen=max_samples)  # Track response times
        self.operation_counts = defaultdict(int)  # Count different operations
        self.error_counts = defaultdict(int)  # Count different errors
        self._lock = threading.Lock()
        
    def record_response_time(self, duration_ms: float, operation_type: str = "chat"):
        """
        Record a response time for an operation
        
        Args:
            duration_ms: Duration of the operation in milliseconds
            operation_type: Type of operation (e.g., 'chat', 'tool_call', 'context_build')
        """
        with self._lock:
            self.response_times.append({
                'duration_ms': duration_ms,
                'operation_type': operation_type,
                'timestamp': datetime.utcnow()
            })
            self.operation_counts[operation_type] += 1
    
    def record_error(self, error_type: str, operation_type: str = "chat"):
        """
        Record an error occurrence
        
        Args:
            error_type: Type of error that occurred
            operation_type: Type of operation during which error occurred
        """
        with self._lock:
            error_key = f"{operation_type}:{error_type}"
            self.error_counts[error_key] += 1
    
    def get_response_time_stats(self, operation_type: str = None, hours: int = 1) -> Dict[str, float]:
        """
        Get response time statistics for a given time period
        
        Args:
            operation_type: Type of operation to get stats for (None for all)
            hours: Number of hours to look back
            
        Returns:
            Dictionary with statistical measures
        """
        cutoff_time = datetime.utcnow() - timedelta(hours=hours)
        
        with self._lock:
            relevant_times = [
                item['duration_ms'] 
                for item in self.response_times 
                if item['timestamp'] >= cutoff_time 
                and (operation_type is None or item['operation_type'] == operation_type)
            ]
        
        if not relevant_times:
            return {
                'avg': 0.0,
                'median': 0.0,
                'p95': 0.0,
                'p99': 0.0,
                'min': 0.0,
                'max': 0.0,
                'count': 0
            }
        
        return {
            'avg': statistics.mean(relevant_times),
            'median': statistics.median(relevant_times),
            'p95': self._percentile(relevant_times, 95),
            'p99': self._percentile(relevant_times, 99),
            'min': min(relevant_times),
            'max': max(relevant_times),
            'count': len(relevant_times)
        }
    
    def get_error_rate(self, operation_type: str = None, hours: int = 1) -> float:
        """
        Get error rate for a given time period
        
        Args:
            operation_type: Type of operation to get error rate for (None for all)
            hours: Number of hours to look back
            
        Returns:
            Error rate as a percentage
        """
        cutoff_time = datetime.utcnow() - timedelta(hours=hours)
        
        with self._lock:
            relevant_operations = sum(
                1 for item in self.response_times
                if item['timestamp'] >= cutoff_time
                and (operation_type is None or item['operation_type'] == operation_type)
            )
            
            if operation_type:
                relevant_errors = sum(
                    count for key, count in self.error_counts.items()
                    if key.startswith(f"{operation_type}:") and operation_type in key
                )
            else:
                relevant_errors = sum(self.error_counts.values())
        
        if relevant_operations == 0:
            return 0.0
        
        return (relevant_errors / relevant_operations) * 100
    
    def get_top_errors(self, limit: int = 5) -> List[Dict[str, any]]:
        """
        Get the top errors by frequency
        
        Args:
            limit: Maximum number of errors to return
            
        Returns:
            List of error dictionaries with type and count
        """
        with self._lock:
            sorted_errors = sorted(
                self.error_counts.items(),
                key=lambda x: x[1],
                reverse=True
            )[:limit]
        
        return [{'error_type': key.split(':')[1], 'operation_type': key.split(':')[0], 'count': value} 
                for key, value in sorted_errors]
    
    def _percentile(self, data: List[float], percentile: float) -> float:
        """
        Calculate percentile of a dataset
        
        Args:
            data: List of numerical values
            percentile: Percentile to calculate (e.g., 95 for 95th percentile)
            
        Returns:
            Calculated percentile value
        """
        if not data:
            return 0.0
        sorted_data = sorted(data)
        index = (percentile / 100) * (len(sorted_data) - 1)
        if index.is_integer():
            return sorted_data[int(index)]
        else:
            lower_index = int(index // 1)
            upper_index = lower_index + 1
            weight = index % 1
            return sorted_data[lower_index] * (1 - weight) + sorted_data[upper_index] * weight


# Global performance monitor instance
perf_monitor = PerformanceMonitor()


def record_response_time(duration_ms: float, operation_type: str = "chat"):
    """
    Record a response time for an operation
    
    Args:
        duration_ms: Duration of the operation in milliseconds
        operation_type: Type of operation (e.g., 'chat', 'tool_call', 'context_build')
    """
    perf_monitor.record_response_time(duration_ms, operation_type)


def record_error(error_type: str, operation_type: str = "chat"):
    """
    Record an error occurrence
    
    Args:
        error_type: Type of error that occurred
        operation_type: Type of operation during which error occurred
    """
    perf_monitor.record_error(error_type, operation_type)


def get_performance_stats(operation_type: str = None, hours: int = 1) -> Dict[str, float]:
    """
    Get performance statistics
    
    Args:
        operation_type: Type of operation to get stats for (None for all)
        hours: Number of hours to look back
        
    Returns:
        Dictionary with performance statistics
    """
    return perf_monitor.get_response_time_stats(operation_type, hours)


def get_error_rate(operation_type: str = None, hours: int = 1) -> float:
    """
    Get error rate
    
    Args:
        operation_type: Type of operation to get error rate for (None for all)
        hours: Number of hours to look back
        
    Returns:
        Error rate as a percentage
    """
    return perf_monitor.get_error_rate(operation_type, hours)


def get_top_errors(limit: int = 5) -> List[Dict[str, any]]:
    """
    Get the top errors by frequency
    
    Args:
        limit: Maximum number of errors to return
        
    Returns:
        List of error dictionaries with type and count
    """
    return perf_monitor.get_top_errors(limit)