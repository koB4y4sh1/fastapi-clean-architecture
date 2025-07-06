from time import time
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time()
        print(f"📥 Incoming request: {request.method} {request.url}")
        response: Response = await call_next(request)
        duration = time() - start_time
        print(f"📤 Response status: {response.status_code} | Time: {duration:.2f}s")
        return response
