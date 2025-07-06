from jose import JWTError, jwt

SECRET_KEY = "your-secret"
ALGORITHM = "HS256"

def decode_jwt(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload  # dict形式で "sub", "email", "exp" など
    except JWTError:
        return None
