import itertools
from typing import Callable, Mapping, Sequence

import pytest

from pydantic import BaseModel
from reforms import Reforms, bool_field, email_field, str_field


@pytest.fixture
def create_form(forms: Reforms) -> Callable:
    def wrapped(field_factory: Callable, **kwargs: Mapping) -> Reforms.Form:
        class MyModel(BaseModel):
            field: field_factory(**kwargs)

        form = forms.Form(MyModel)
        return form

    return wrapped


field_settings = [
    (
        str_field,
        (
            ("field_id", "id", "exampleId"),
            ("field_class", "class", "example-class"),
            ("placeholder", "placeholder", "Example placeholder"),
            ("label", None, "example label text"),
        ),
    ),
    (
        bool_field,
        (
            ("field_id", "id", "exampleId"),
            ("field_class", "class", "example-class"),
            ("label", None, "example label text"),
        ),
    ),
    (
        email_field,
        (
            ("field_id", "id", "exampleId"),
            ("field_class", "class", "example-class"),
            ("placeholder", "placeholder", "Example placeholder"),
            ("label", None, "example label text"),
        ),
    ),
]


@pytest.mark.parametrize(
    "field_factory, args",
    [
        pytest.param(
            field,
            variant,
            id=f"{field.__name__}-{'-'.join(i[0] for i in variant)}",
        )
        for field, settings in field_settings
        for i in range(len(settings) + 1)
        for variant in itertools.combinations(settings, i)
    ],
)
def test_render(field_factory: Callable, args: Sequence, create_form: Callable):
    field_kwargs = {name: value for name, _, value in args}
    form = create_form(field_factory, **field_kwargs)
    rendered_layout = str(form.field)

    print(rendered_layout)

    for field_name, rendered_name, value in args:
        if field_name == "label":
            assert f"{value}</label>" in rendered_layout
            if "field_id" in field_kwargs:
                assert 'for="{}"'.format(field_kwargs["field_id"]) in rendered_layout

            continue

        content = '{name}="{value}"'.format(name=rendered_name, value=value)
        assert content in rendered_layout
