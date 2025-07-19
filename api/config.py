from pydantic_settings import BaseSettings
from typing import List, Dict

class Settings(BaseSettings):
    PROJECT_NAME: str = "My FastAPI App"
    API_PREFIX: str = "/api"
    VERSION: str ="1.0.0"
    SERVERS: List[Dict[str, str]] = [
        {"url": "http://localhost:8000", "description": "Local dev"},
        {"url": "https://api.example-dev.com", "description": "Testing"},
        {"url": "https://api.example.com", "description": "Production"},
    ]
    # 🔧 CORS関連設定
    ALLOW_ORIGINS: List[str] = ["*"]
    ALLOW_CREDENTIALS: bool = True
    ALLOW_METHODS: List[str] = ["GET", "POST", "PUT", "DELETE"]
    ALLOW_HEADERS: List[str] = ["Content-Type","Authorization"]

    # 🔧 OpenAPIの設定
    DESCRIPTION: str = "このAPIは、ユーザー管理を行うためのAPIです。"
    SECURITY: List[Dict[str, List[str]]] = [{"bearerAuth": []}]
    SECURITY_SCHEMES: Dict[str, Dict[str, str]] = {
        "bearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
            "description": "認証後にMSALから取得できるGraphAPI認証用アクセストークン"
        }
    }
    
    class Config:
        env_file = ".env"
        extra = "allow"

settings = Settings()
