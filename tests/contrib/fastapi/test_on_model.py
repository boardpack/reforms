from typing import Callable, Dict, Type

import pytest
from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel
from reforms import bool_field, email_field, str_field
from reforms.contrib.fastapi import from_model


class UserModel(BaseModel):
    name: str_field()
    email: email_field()
    has_github: bool_field()


class UserModelWithBoolDefault(BaseModel):
    name: str_field()
    email: email_field()
    has_github: bool_field() = True


@pytest.fixture
def create_app() -> Callable:
    def _create_app(model: Type[BaseModel]) -> FastAPI:
        test_app = FastAPI()

        @test_app.post("/")
        async def index(form: from_model(model) = Depends()):
            return form

        return test_app

    return _create_app


@pytest.mark.parametrize(
    "model, input_data, expected_data",
    [
        (
            UserModel,
            {"name": "name", "email": "email@e.com"},
            {"name": "name", "email": "email@e.com", "has_github": False},
        ),
        (
            UserModel,
            {"name": "name", "email": "email@e.com", "has_github": "on"},
            {"name": "name", "email": "email@e.com", "has_github": True},
        ),
        (
            UserModelWithBoolDefault,
            {"name": "name", "email": "email@e.com"},
            {"name": "name", "email": "email@e.com", "has_github": True},
        ),
    ],
)
def test_on_model(
    model: Type[BaseModel],
    input_data: Dict[str, str],
    expected_data: Dict[str, str],
    create_app: Callable[[Type[BaseModel]], FastAPI],
):
    app = create_app(model)
    client = TestClient(app)

    response = client.post("/", data=input_data)
    response.raise_for_status()

    assert response.json() == expected_data
