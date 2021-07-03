import itertools

import pytest
from pydantic import BaseModel
from reforms import Reforms, StringField
from reforms.validators import AnyOf, BaseValidator, Length, NoneOf


@pytest.mark.parametrize(
    "test_value, validator1, validator2",
    [
        (test_value, validator1, validator2)
        for test_value, validator1, validator2 in itertools.chain(
            (
                ("a", validator1, validator2)
                for validator1, validator2 in itertools.combinations(
                    (AnyOf(values=["a", "b", "c"]), Length(min=1)), 2
                )
            ),
            (
                ("d", validator1, validator2)
                for validator1, validator2 in itertools.combinations(
                    (NoneOf(values=["a", "b", "c"]), Length(min=1)), 2
                )
            ),
        )
    ],
)
def test_multiply_validators_passes(
    test_value: str,
    validator1: BaseValidator,
    validator2: BaseValidator,
    forms: Reforms,
):
    class MyForm(BaseModel):
        field: StringField(validators=[validator1, validator2])

    form = forms.Form(MyForm)
    form(field=test_value)


# TODO: add more tests for multiply validators usage
