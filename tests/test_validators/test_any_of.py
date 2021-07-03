from typing import Any, Callable, List

import pytest
from pydantic import BaseModel, ValidationError
from reforms import Reforms, str_field
from reforms.validators import AnyOf


@pytest.fixture
def create_form(forms: Reforms) -> Callable:
    def wrapped(
        values: List[Any], message: str = "", values_formatter: Callable = None
    ) -> Reforms.Form:
        args = {"values": values, "values_formatter": values_formatter}
        if message:
            args["message"] = message

        class MyForm(BaseModel):
            field: str_field(validators=[AnyOf(**args)])

        return forms.Form(MyForm)

    return wrapped


@pytest.mark.parametrize(
    "test_value, test_list", [("b", ["a", "b", "c"]), (2, [1, 2, 3])]
)
def test_any_of_passes(test_value, test_list, create_form):
    form = create_form(values=test_list)
    form(field=test_value)


@pytest.mark.parametrize(
    "test_value, test_list", [("d", ["a", "b", "c"]), (6, [1, 2, 3])]
)
def test_any_of_raises(test_value, test_list, create_form):
    form = create_form(values=test_list)
    with pytest.raises(ValidationError):
        form(field=test_value)


def test_any_of_values_formatter(create_form):
    def formatter(values):
        return "::".join(str(x) for x in reversed(values))

    form = create_form(
        values=[7, 8, 9], message="test {values}", values_formatter=formatter
    )

    with pytest.raises(ValidationError) as e:
        form(field=4)

    assert e.value.errors()[0]["msg"] == "test 9::8::7"
