import itertools
from typing import Any, Callable, Mapping, Sequence

import pytest

from pydantic import BaseModel
from reforms import Reforms, bool_field, email_field, str_field
from reforms.fields import BaseField


@pytest.fixture
def create_form(forms: Reforms) -> Callable:
    def wrapped(
        field_factory: Callable, default_value: Any = None, **kwargs: Mapping
    ) -> Reforms.Form:
        if default_value is None:

            class MyModel(BaseModel):
                field: field_factory(**kwargs)

        else:

            class MyModel(BaseModel):
                field: field_factory(**kwargs) = default_value

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

fields_with_attrs_combinations = [
    pytest.param(
        field,
        variant,
        id=f"{field.__name__}-{'-'.join(i[0] for i in variant)}",
    )
    for field, settings in field_settings
    for i in range(len(settings) + 1)
    for variant in itertools.combinations(settings, i)
]


@pytest.mark.parametrize(
    "field_factory, args",
    fields_with_attrs_combinations,
)
def test_render(field_factory: Callable, args: Sequence, create_form: Callable):
    field_kwargs = {name: value for name, _, value in args}
    form = create_form(field_factory, **field_kwargs)
    rendered_layout = str(form.field)

    for field_name, rendered_name, value in args:
        if field_name == "label":
            assert f"{value}</label>" in rendered_layout
            if "field_id" in field_kwargs:
                assert 'for="{}"'.format(field_kwargs["field_id"]) in rendered_layout

            continue

        content = '{name}="{value}"'.format(name=rendered_name, value=value)
        assert content in rendered_layout


@pytest.mark.parametrize(
    "field_factory, args",
    fields_with_attrs_combinations,
)
def test_rendered_spaces(
    field_factory: Callable, args: Sequence, create_form: Callable
):
    field_kwargs = {name: value for name, _, value in args}
    form = create_form(field_factory, **field_kwargs)
    rendered_layout = str(form.field)

    for bad_variant in ("  ", " >"):
        assert bad_variant not in rendered_layout


@pytest.mark.parametrize(
    "field_factory, default_value, html_part",
    [
        (str_field, "value", 'value="value"'),
        (bool_field, False, ""),
        (bool_field, True, "checked"),
        (email_field, "example@example.com", 'value="example@example.com"'),
    ],
)
def test_field_default(
    field_factory: Callable[[], BaseField],
    default_value: Any,
    html_part: str,
    create_form: Callable,
):
    form = create_form(field_factory, default_value=default_value)
    rendered_layout = str(form.field)

    assert html_part in rendered_layout


@pytest.mark.parametrize(
    "field_factory, html_part",
    [
        (str_field, 'value="value"'),
        (bool_field, "checked"),
        (email_field, 'value="example@example.com"'),
    ],
)
def test_field_without_default(
    field_factory: Callable[[], BaseField], html_part: str, create_form: Callable
):
    exclude_fields = (bool_field,)
    form = create_form(field_factory)
    rendered_layout = str(form.field)

    assert html_part not in rendered_layout
    if field_factory not in exclude_fields:
        assert " required" in rendered_layout
