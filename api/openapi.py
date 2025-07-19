import yaml
import os
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from main import create_app
from config import settings

def save_openapi_spec(app:FastAPI, filepath: str):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        yaml.dump(app.openapi(), f, allow_unicode=True, sort_keys=False)

def custom_openapi(app: FastAPI):
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        servers=app.servers,
        description=settings.DESCRIPTION,
        routes=app.routes,
    )

    # 🔐 セキュリティスキーマを定義
    openapi_schema["components"]["securitySchemes"] = settings.SECURITY_SCHEMES

    # 🔐 グローバルにセキュリティを有効にする
    openapi_schema["security"] = settings.SECURITY

    app.openapi_schema = openapi_schema
    return app.openapi_schema

if __name__ == "__main__":
    app = create_app()
    output_path = "../docs/openapi.yaml"
    app.openapi = lambda: custom_openapi(app)
    save_openapi_spec(app, output_path)
    print(f"OpenAPI spec saved to {output_path}")
