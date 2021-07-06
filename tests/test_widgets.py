from typing import Any, Dict, Type

import jinja2
import pytest
from reforms import Reforms
from reforms.widgets import (
    BaseWidget,
    Checkbox,
    EmailInput,
    HiddenInput,
    Input,
    TextInput,
)

all_widgets = (
    Checkbox,
    EmailInput,
    TextInput,
    HiddenInput,
)

input_widgets = (
    Checkbox,
    EmailInput,
    TextInput,
    HiddenInput,
)

widgets_with_placeholder = [w for w in input_widgets if w is not Checkbox]
widgets_with_value = [w for w in input_widgets if w is not Checkbox]


@pytest.fixture
def env() -> jinja2.Environment:
    reforms = Reforms()
    return reforms.env


@pytest.fixture
def render_settings() -> Dict[str, Any]:
    return {"name": "example", "field_id": "example", "field_class": "example"}


def test_widget_rendering_without_name(env: jinja2.Environment):
    widget = BaseWidget()
    widget.template = "input.html"

    with pytest.raises(ValueError):
        widget.render(env)


@pytest.mark.parametrize("widget_class", all_widgets)
def test_non_empty_template(widget_class: Type[BaseWidget]):
    assert widget_class.template


@pytest.mark.parametrize("widget_class", input_widgets)
def test_non_empty_input_type(widget_class: Type[Input]):
    assert widget_class.input_type


@pytest.mark.parametrize("widget_class", input_widgets)
def test_input_type_rendering(widget_class: Type[Input], env: jinja2.Environment):
    widget = widget_class(name="type")
    assert f'type="{widget_class.input_type}"' in str(widget.render(env))


@pytest.mark.parametrize(
    ("widget_class", "settings", "expected_html_part"),
    [
        (widget_class, settings, expected_html_part)
        for widget_class in all_widgets
        for settings, expected_html_part in (
            ({"name": "e"}, ' name="e"'),
            ({"field_id": "example"}, ' id="example"'),
            ({"field_class": "example"}, ' class="example"'),
            ({"disabled": True}, " disabled"),
        )
    ],
)
def test_widget_base_attrs_rendering(
    widget_class: Type[BaseWidget],
    settings: Dict[str, Any],
    expected_html_part: str,
    env: jinja2.Environment,
):
    if "name" not in settings:
        settings["name"] = "example"

    widget = widget_class(**settings)
    assert expected_html_part in str(widget.render(env))


def test_checkbox_widget_checked(env: jinja2.Environment):
    widget = Checkbox(name="temp", required=False, default=True)
    assert "checked" in str(widget.render(env))


@pytest.mark.parametrize(
    ("required", "default"),
    [
        pytest.param(required, default, id=f"required={required}, default={default}")
        for required, default in (
            (True, False),
            (True, True),
            (False, False),
        )
    ],
)
def test_checkbox_widget_not_checked(
    env: jinja2.Environment, required: bool, default: bool
):
    widget = Checkbox(name="temp", required=required, default=default)
    assert "checked" not in str(widget.render(env))


@pytest.mark.parametrize("widget_class", all_widgets)
def test_label_rendering(
    widget_class: Type[BaseWidget],
    env: jinja2.Environment,
):
    settings = {
        "name": "temp",
        "field_id": "example",
        "label": "example label",
    }
    expected_html = f'<label for="{settings["field_id"]}">{settings["label"]}</label>'
    widget = widget_class(**settings)

    assert expected_html in str(widget.render(env))


@pytest.mark.parametrize("widget_class", widgets_with_placeholder)
def test_placeholder_rendering(widget_class: Type[BaseWidget], env: jinja2.Environment):
    placeholder_settings = {"placeholder": "example text"}
    widget = widget_class(name="temp", **placeholder_settings)
    assert 'placeholder="example text"' in str(widget.render(env))


@pytest.mark.parametrize("widget_class", widgets_with_placeholder)
def test_placeholder_no_rendering(
    widget_class: Type[BaseWidget], env: jinja2.Environment
):
    widget = widget_class(name="temp")
    assert "placeholder=" not in str(widget.render(env))


@pytest.mark.parametrize(
    ("widget_class", "settings", "expected_html_part"),
    [
        (widget_class, settings, expected_html_part)
        for widget_class in widgets_with_value
        for settings, expected_html_part in (
            ({"default": "example", "required": False}, 'value="example"'),
        )
    ],
)
def test_value_rendering(
    widget_class: Type[BaseWidget],
    settings: Dict[str, Any],
    expected_html_part: str,
    env: jinja2.Environment,
):
    widget = widget_class(name="temp", **settings)
    assert expected_html_part in str(widget.render(env))


@pytest.mark.parametrize(
    ("widget_class", "settings"),
    [
        (widget_class, settings)
        for widget_class in widgets_with_value
        for settings in (
            {"required": True},
            {"default": "example", "required": True},
        )
    ],
)
def test_value_no_rendering(
    widget_class: Type[BaseWidget],
    settings: Dict[str, Any],
    env: jinja2.Environment,
):
    widget = widget_class(name="temp", **settings)
    assert "value=" not in str(widget.render(env))
