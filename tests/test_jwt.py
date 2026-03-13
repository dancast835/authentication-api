from app.routes.routes import  create_access_token, verify_token
from datetime import timedelta
import pytest
from fastapi import HTTPException

data = {"sub": "test123@gmail.com"}
test_token = "Estoesdemasiadoseguro@lol"

time_delta = timedelta(minutes=15)

def test_create_access_token():
    token_result = create_access_token(data, time_delta)

    assert token_result is not None
    assert isinstance(token_result, str)

def test_verify_token():
    token_result = create_access_token(data, time_delta)
    verified = verify_token(token_result)

    assert verified == data["sub"]

def test_verify_fake_token():
    fake_token = "Soyreal@creanme"

    with pytest.raises(HTTPException):
        verify_token(fake_token)