from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from src.utils.exceptions import LLMServiceError, CustomAppException  # 独自例外
from typing import Type


def register_exception_handlers(app: FastAPI):
    exception_mappings: dict[Type[Exception], dict] = {
        LLMServiceError: {
            "status_code": 500,
            "detail": "AI処理中にエラーが発生しました。",
        },
        CustomAppException: {
            "status_code": 400,
            "detail": "アプリケーションエラーが発生しました。",
        },
    }

    for exc_type, response in exception_mappings.items():
        @app.exception_handler(exc_type)
        async def _handler(request: Request, exc: Exception, response=response):
            return JSONResponse(
                status_code=response["status_code"],
                content={"detail": response["detail"]},
            )
