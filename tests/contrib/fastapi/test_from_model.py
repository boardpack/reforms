from typing import Callable, Dict, Type

import pytest
from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel
from reforms import BooleanField, EmailField, StringField
from reforms.contrib.fastapi import from_model


class UserModel(BaseModel):
    name: StringField()
    email: EmailField()
    has_github: BooleanField()


class UserModelWithBoolDefault(BaseModel):
    name: StringField() = "John"
    email: EmailField()
    has_github: BooleanField() = True


@pytest.fixture
def create_app() -> Callable:
    def _create_app(model: Type[BaseModel]) -> FastAPI:
        test_app = FastAPI()

        @test_app.post("/")
        async def index(form: from_model(model) = Depends()):
            return form

        return test_app

    return _create_app


@pytest.fixture
def client(
    create_app: Callable[[Type[BaseModel]], FastAPI], model: Type[BaseModel]
) -> TestClient:
    app = create_app(model)
    return TestClient(app)


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
        (
            UserModelWithBoolDefault,
            {"email": "email@e.com"},
            {"name": "John", "email": "email@e.com", "has_github": True},
        ),
    ],
)
def test_on_model(
    client: TestClient,
    input_data: Dict[str, str],
    expected_data: Dict[str, str],
):
    response = client.post("/", data=input_data)
    assert response.json() == expected_data
