import pytest
from fastapi import HTTPException
from utils.middleware.auth import get_token_header

def test_get_token_header_valid():
    assert get_token_header("Bearer testtoken") == "testtoken"

def test_get_token_header_invalid():
    with pytest.raises(HTTPException):
        get_token_header("invalidtoken") 