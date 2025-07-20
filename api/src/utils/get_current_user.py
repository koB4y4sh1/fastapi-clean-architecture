from fastapi import Request, HTTPException
from src.schema.model.user import User
from src.utils.decode_jwt import decode_jwt

async def get_current_user(request: Request) -> User:
    """
    """
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    token = auth_header[7:]
    payload = decode_jwt(token)
    # if not payload:
    #     raise HTTPException(status_code=401, detail="Invalid token")

    # 任意：ここでGraphAPIやDBから取得した結果を反映してもOK
    
    payload = {} # ダミー値
    return User(
        user_principal_name=payload.get("upn", "test_user.pub@exsample.com"),
        name=payload.get("oid", "abc123"),
        email=payload.get("email", "test_user@pub.example.com")
    )