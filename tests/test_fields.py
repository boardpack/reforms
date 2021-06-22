from typing import Any

import pytest

from pydantic import BaseModel, Field, ValidationError
from reforms import bool_field, email_field, str_field


@pytest.mark.parametrize(
    "field_type, value",
    [
        (str_field, "value"),
        (bool_field, False),
        (email_field, "example@example.com"),
    ],
)
def test_field(field_type: Field, value: Any):
    class MyForm(BaseModel):
        my_field: field_type()

    form = MyForm(my_field=value)
    assert form.my_field == value


@pytest.mark.parametrize(
    "field_type, value",
    [
        (str_field, None),
        (bool_field, "False"),
        (email_field, "example@.com"),
    ],
)
def test_field_fail(field_type: Field, value: Any):
    class MyForm(BaseModel):
        my_field: field_type()

    with pytest.raises(ValidationError):
        MyForm(my_field=value)


@pytest.mark.parametrize(
    "field_type, default_value",
    [
        (str_field, "value"),
        (bool_field, False),
        (email_field, "example@example.com"),
    ],
)
def test_field_default(field_type: Field, default_value: Any):
    class MyForm(BaseModel):
        my_field: field_type() = default_value

    form = MyForm()
    assert form.my_field == default_value
