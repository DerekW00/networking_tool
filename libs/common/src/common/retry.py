"""Retry utilities for handling transient failures."""

import logging
import random
from functools import wraps
from typing import Callable, Type, Union, List, Any

from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
    before_log,
    after_log,
)


logger = logging.getLogger(__name__)


def with_retry(
    max_attempts: int = 3,
    min_wait: float = 1.0,
    max_wait: float = 10.0,
    retry_exceptions: Union[Type[Exception], List[Type[Exception]]] = Exception,
    jitter: bool = True,
):
    """
    Decorator for retrying functions that may experience transient failures.
    
    Args:
        max_attempts: Maximum number of retry attempts
        min_wait: Minimum wait time between retries (seconds)
        max_wait: Maximum wait time between retries (seconds)
        retry_exceptions: Exception or list of exceptions that trigger retry
        jitter: Whether to add randomness to retry wait time
        
    Returns:
        Decorated function with retry logic
    """
    def decorator(func: Callable) -> Callable:
        @retry(
            stop=stop_after_attempt(max_attempts),
            wait=wait_exponential(multiplier=1, min=min_wait, max=max_wait),
            retry=retry_if_exception_type(retry_exceptions),
            before=before_log(logger, logging.DEBUG),
            after=after_log(logger, logging.DEBUG),
        )
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            # Add jitter to avoid thundering herd problem
            if jitter:
                jitter_time = random.uniform(0, min_wait * 0.1)
                if jitter_time > 0:
                    import time
                    time.sleep(jitter_time)
                    
            return func(*args, **kwargs)
            
        return wrapper
    
    return decorator 