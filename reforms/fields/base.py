import itertools
from typing import Any, Dict, Iterable, List

import jinja2
from markupsafe import Markup
from pydantic.fields import ModelField
from pydantic.utils import Representation

from ..validators import BaseValidator

__all__ = ["BaseField"]


class BaseField(Representation):
    template: str
    _validators: List[BaseValidator] = []
    _render_settings: Dict[str, Any] = {}

    @classmethod
    def __get_validators__(cls) -> Iterable[BaseValidator]:
        return itertools.chain(cls._validators)

    @classmethod
    def render(cls, env: jinja2.Environment, field: ModelField) -> str:
        if not env or not isinstance(env, jinja2.Environment):
            raise ValueError(
                "You can't render field outside of any form. Please define Form class "
                "first."
            )
        if not cls.template:
            raise ValueError(
                "You can't render the field without the template reference. Please "
                "define 'template' attribute in your field definition."
            )

        cls._render_settings["name"] = field.name
        cls._render_settings["required"] = field.required
        cls._render_settings["default"] = field.default

        if field.required and cls._render_settings["disabled"]:
            raise ValueError(
                f"You can't render {field.name} because of it has disabled option and "
                "doesn't have a default value"
            )

        template: jinja2.Template = env.get_template(cls.template)
        return Markup(template.render(cls._render_settings))
