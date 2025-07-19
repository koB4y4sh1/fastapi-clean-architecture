import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI
from src.utils.exception_handlers import register_exception_handlers
from src.utils.exceptions import LLMServiceError, CustomAppException

app = FastAPI()
register_exception_handlers(app)
client = TestClient(app)

@app.get("/llm-error")
def raise_llm():
    raise LLMServiceError()

@app.get("/custom-error")
def raise_custom():
    raise CustomAppException()

def test_llm_service_error():
    response = client.get("/llm-error")
    assert response.status_code == 500
    assert response.json()["detail"] == "AI処理中にエラーが発生しました。"

def test_custom_app_exception():
    response = client.get("/custom-error")
    assert response.status_code == 400
    assert response.json()["detail"] == "アプリケーションエラーが発生しました。" 