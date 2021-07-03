from typing import Callable

import pytest
from pydantic import BaseModel, ValidationError
from reforms import Reforms, StringField
from reforms.validators import Length


@pytest.fixture
def create_form(forms: Reforms) -> Callable:
    def wrapped(
        min_value: int = -1, max_value: int = -1, message: str = ""
    ) -> Reforms.Form:
        class MyForm(BaseModel):
            field: StringField(
                validators=[Length(min=min_value, max=max_value, message=message)]
            )

        return forms.Form(MyForm)

    return wrapped


@pytest.mark.parametrize("min_value, max_value", [(2, 6), (6, -1), (-1, 6), (6, 6)])
def test_correct_length_passes(min_value, max_value, create_form):
    form = create_form(min_value=min_value, max_value=max_value)
    form(field="foobar")


@pytest.mark.parametrize("min_value, max_value", [(7, -1), (-1, 5)])
def test_bad_length_raises(min_value, max_value, create_form):
    form = create_form(min_value=min_value, max_value=max_value)

    with pytest.raises(ValidationError):
        form(field="foobar")


@pytest.mark.parametrize("min_value, max_value", [(-1, -1), (5, 2)])
def test_bad_length_init_raises(min_value, max_value, create_form):
    with pytest.raises(ValidationError):
        create_form(min_value=min_value, max_value=max_value)


@pytest.mark.parametrize(
    ("kwargs", "message"),
    (
        ({"min_value": 2, "max_value": 5, "message": "{min} and {max}"}, "2 and 5"),
        ({"min_value": 8, "max_value": -1}, "at least 8"),
        ({"min_value": -1, "max_value": 5}, "longer than 5"),
        ({"min_value": 2, "max_value": 5}, "between 2 and 5"),
        ({"min_value": 5, "max_value": 5}, "exactly 5"),
    ),
)
def test_length_messages(kwargs, message, create_form):
    form = create_form(**kwargs)

    with pytest.raises(ValidationError) as e:
        form(field="foobar")

    assert message in e.value.errors()[0]["msg"]
