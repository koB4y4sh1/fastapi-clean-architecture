

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import get_settings
from src.urls import api_router
from src.utils.exception_handlers import register_exception_handlers
from src.utils.middleware.logging import LoggingMiddleware

def create_app() -> FastAPI:

    # ✅ 設定情報取得
    settings = get_settings()

    # ✅ FastAPIアプリケーションの作成
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        servers=settings.SERVERS,
    )

    # ✅ CORS Middleware 設定
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOW_ORIGINS,
        allow_credentials=settings.ALLOW_CREDENTIALS,
        allow_methods=settings.ALLOW_METHODS,
        allow_headers=settings.ALLOW_HEADERS,
    )

    # ✅ APIルータ登録
    app.include_router(api_router, prefix=settings.API_PREFIX)
    
    # ✅ ミドルウェア登録
    app.add_middleware(LoggingMiddleware)

    # ✅ 例外ハンドラ登録
    register_exception_handlers(app)

    return app

load_dotenv()
app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)