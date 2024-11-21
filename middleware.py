import time
# from functools import wraps
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from collections import defaultdict
from typing import Dict
from logger import logger

# Rate limiter
class RateLimiter(BaseHTTPMiddleware):
   def __init__(self, app):
    # instanciated the class with parent class BaseHTTPMiddleware
    super().__init__(app)


    self.rate_limit_records: Dict[str, float] = defaultdict(float)

    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host
        current_time = time.time()

        if current_time - self.rate_limit_records[client_ip] < 1:
            time.sleep(1)
        
        self.rate_limit_records[client_ip] = current_time

        # Process the request
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time

        path = request.url.path

        await logger.info(f"Request to {path} took {process_time} seconds")
    

    # def decorator(func):
    #     calls = []

    #     @wraps(func)
    #     async def wrapper(request: Request, *args, **kwargs):
    #         current_time = time.time()
    #         calls_in_time_frame = [call for call in calls if calls > current_time - time_frame]
    #         if len(calls_in_time_frame) >= max_calls:
    #             time.sleep(1)
    #         calls.append(current_time)
    #         return await func(request, *args, **kwargs)
        
    #     return wrapper
    
    # return decorator