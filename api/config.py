from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "My FastAPI App"
    API_PREFIX: str = "/api"
    VERSION: str ="1.0.0"
    SERVERS: list[dict[str, str]] = [
        {"url": "http://localhost:8000", "description": "Local dev"},
        {"url": "https://api.example-dev.com", "description": "Testing"},
        {"url": "https://api.example.com", "description": "Production"},
    ]
    # 🔧 CORS関連設定
    ALLOW_ORIGINS: list[str] = ["*"]
    ALLOW_CREDENTIALS: bool = True
    ALLOW_METHODS: list[str] = ["GET", "POST", "PUT", "DELETE"]
    ALLOW_HEADERS: list[str] = ["Content-Type","Authorization"]

    # 🔧 OpenAPIの設定
    DESCRIPTION: str = "このAPIは、ユーザー管理を行うためのAPIです。"
    SECURITY: list[dict[str, list[str]]] = [{"bearerAuth": []}]
    SECURITY_SCHEMES: dict[str, dict[str, str]] = {
        "bearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
            "description": "認証後にMSALから取得できるGraphAPI認証用アクセストークン"
        }
    }

@lru_cache
def get_settings():
    """ @lru_cacheで.envの結果をキャッシュする """
    return Settings()
