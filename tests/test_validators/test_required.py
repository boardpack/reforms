from typing import Callable

import pytest

from pydantic import BaseModel, ValidationError
from reforms import Reforms, str_field
from reforms.validators import Required


@pytest.fixture
def create_form(forms: Reforms) -> Callable:
    def wrapped(message: str = "") -> Reforms.Form:
        class MyForm(BaseModel):
            field: str_field(
                validators=[Required(message=message) if message else Required()]
            )

        return forms.Form(MyForm)

    return wrapped


def test_required(create_form):
    form = create_form()
    form(field="foobar")


@pytest.mark.parametrize("bad_value", [None, "", " ", "\t\t"])
def test_required_raises(bad_value, create_form):
    form = create_form()

    with pytest.raises(ValidationError):
        form(field=bad_value)


@pytest.mark.parametrize(
    ("args", "message"),
    (
        ({}, "This field is required."),
        ({"message": "foo"}, "foo"),
    ),
)
def test_data_required_messages(args, message, create_form):
    form = create_form(**args)

    with pytest.raises(ValidationError) as e:
        form(field="")

    assert e.value.errors()[0]["msg"] == message
