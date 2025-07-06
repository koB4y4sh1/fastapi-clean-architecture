from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from src.utils.decode_jwt import decode_jwt

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        auth_header = request.headers.get("Authorization")
        user = None

        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header[7:]
            payload = decode_jwt(token)
            if payload:
                # GraphAPIやDBから取得するなどの処理を追加

                user = "test_user"  # ここではユーザー名を仮で設定

        request.state.user = user
        return await call_next(request)
