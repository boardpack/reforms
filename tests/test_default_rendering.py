import itertools
from typing import Any, Callable, Mapping, Sequence

import pytest
from pydantic import BaseModel
from reforms import BooleanField, EmailField, Reforms, StringField
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

        return forms.Form(MyModel)

    return wrapped


field_settings = [
    (
        StringField,
        (
            ("field_id", "id", "exampleId"),
            ("field_class", "class", "example-class"),
            ("placeholder", "placeholder", "Example placeholder"),
            ("label", None, "example label text"),
        ),
    ),
    (
        BooleanField,
        (
            ("field_id", "id", "exampleId"),
            ("field_class", "class", "example-class"),
            ("label", None, "example label text"),
        ),
    ),
    (
        EmailField,
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
        field, variant, id=f"{field.__name__}-{'-'.join(i[0] for i in variant)}"
    )
    for field, settings in field_settings
    for i in range(len(settings) + 1)
    for variant in itertools.combinations(settings, i)
]


@pytest.mark.parametrize("field_factory, args", fields_with_attrs_combinations)
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

        assert f'{rendered_name}="{value}"' in rendered_layout


@pytest.mark.parametrize("field_factory, args", fields_with_attrs_combinations)
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
        (StringField, "value", 'value="value"'),
        (BooleanField, False, ""),
        (BooleanField, True, "checked"),
        (EmailField, "example@example.com", 'value="example@example.com"'),
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
        (StringField, 'value="value"'),
        (BooleanField, "checked"),
        (EmailField, 'value="example@example.com"'),
    ],
)
def test_field_without_default(
    field_factory: Callable[[], BaseField], html_part: str, create_form: Callable
):
    exclude_fields = (BooleanField,)
    form = create_form(field_factory)
    rendered_layout = str(form.field)

    assert html_part not in rendered_layout
    if field_factory not in exclude_fields:
        assert " required" in rendered_layout


@pytest.mark.parametrize(
    "field_factory, default_value, disabled, expected",
    [
        (field_factory, default_value, disabled, disabled)
        for disabled in (True, False)
        for field_factory, default_value in (
            (StringField, ""),
            (BooleanField, False),
            (EmailField, "e@e.com"),
        )
    ],
)
def test_field_disabled(
    field_factory: Callable[[], BaseField],
    default_value: Any,
    disabled: bool,
    expected: bool,
    create_form: Callable,
):
    form = create_form(field_factory, default_value=default_value, disabled=disabled)
    rendered_layout = str(form.field)
    actual = " disabled" in rendered_layout

    assert actual is expected


@pytest.mark.parametrize(
    "field_factory, default_value, disabled",
    [(field, None, True) for field in (BooleanField, EmailField, StringField)],
)
def test_disabled_default_value_conflict(
    field_factory: Callable[[], BaseField],
    default_value: Any,
    disabled: bool,
    create_form: Callable,
):
    form = create_form(field_factory, default_value=default_value, disabled=disabled)

    with pytest.raises(ValueError):
        str(form.field)
