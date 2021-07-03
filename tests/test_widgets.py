from typing import Any, Dict, Type

import jinja2
import pytest
from reforms import Reforms
from reforms.widgets import BaseWidget, Checkbox, EmailInput, Input, TextInput

all_widgets = (
    Checkbox,
    EmailInput,
    TextInput,
)

input_widgets = (
    Checkbox,
    EmailInput,
    TextInput,
)


@pytest.fixture
def environment() -> jinja2.Environment:
    reforms = Reforms()
    return reforms.env


@pytest.fixture
def render_settings() -> Dict[str, Any]:
    return {"name": "example", "field_id": "example", "field_class": "example"}


@pytest.fixture
def render_settings_with_label(render_settings: Dict[str, Any]) -> Dict[str, Any]:
    return {
        **render_settings,
        "label": "example label",
    }


@pytest.fixture
def input_render_settings() -> Dict[str, Any]:
    return {
        "value": "example",
        "disabled": True,
    }


@pytest.mark.parametrize("widget_class", all_widgets)
def test_non_empty_template(widget_class: Type[BaseWidget]):
    assert widget_class.template


@pytest.mark.parametrize("widget_class", input_widgets)
def test_non_empty_input_type(widget_class: Type[Input]):
    assert widget_class.input_type


@pytest.mark.parametrize("widget_class", all_widgets)
def test_widget_rendering(
    widget_class: Type[BaseWidget],
    render_settings: Dict[str, Any],
    environment: jinja2.Environment,
):
    widget = widget_class(**render_settings)
    rendered_html = str(widget.render(environment))

    for part in [
        f'{k.replace("field_", "")}="{v}"' for k, v in render_settings.items()
    ]:
        assert part in rendered_html


@pytest.mark.parametrize("widget_class", input_widgets)
def test_input_widget_rendering(
    widget_class: Type[Input],
    input_render_settings: Dict[str, Any],
    environment: jinja2.Environment,
):
    widget = widget_class(**input_render_settings)
    rendered_html = str(widget.render(environment))

    assert f'type="{widget_class.input_type}"' in rendered_html

    for k, v in input_render_settings.items():
        assert f'{k}="{v}"' if k != "disabled" else k in rendered_html


@pytest.mark.parametrize("widget_class", all_widgets)
def test_label_rendering(
    widget_class: Type[BaseWidget],
    render_settings_with_label: Dict[str, Any],
    environment: jinja2.Environment,
):
    expected_html = (
        f'<label for="{render_settings_with_label["field_id"]}">'
        f'{render_settings_with_label["label"]}</label>'
    )

    widget = widget_class(**render_settings_with_label)
    assert expected_html in str(widget.render(environment))
