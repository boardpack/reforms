from typing import Any, Dict, Type

import jinja2
import pytest
from reforms import Reforms
from reforms.widgets import BaseWidget, Checkbox, EmailInput, TextInput


@pytest.fixture
def environment() -> jinja2.Environment:
    reforms = Reforms()
    return reforms.env


@pytest.fixture
def render_settings() -> Dict[str, Any]:
    return {"name": "example", "field_id": "example", "field_class": "example"}


@pytest.mark.parametrize(("widget_class",), [(TextInput,), (EmailInput,), (Checkbox,)])
def test_input_widget(
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
