from copy import deepcopy
from typing import Any, Dict

import jinja2
from markupsafe import Markup

__all__ = (
    "BaseWidget",
    "TextInput",
    "EmailInput",
    "Checkbox",
)


class BaseWidget:
    template: str = ""

    def __init__(self, **render_settings: Any) -> None:
        self._render_settings: Dict[str, Any] = render_settings

    @property
    def settings(self) -> Dict[str, Any]:
        return deepcopy(self._render_settings)

    def render(self, env: jinja2.Environment, **kwargs: Any) -> str:
        if not env or not isinstance(env, jinja2.Environment):
            raise ValueError(
                "You can't render field outside of any form. Please define Form class "
                "first."
            )
        if not self.template:
            raise ValueError(
                "You can't render the field without the template reference. Please "
                "define 'template' attribute in your field definition."
            )

        self._render_settings.update(kwargs)

        template: jinja2.Template = env.get_template(self.template)
        return Markup(template.render(self.settings))

    def __str__(self) -> str:
        return "{class_name}(template='{template}', {attrs})".format(
            class_name=self.__class__.__name__,
            template=self.template,
            attrs=", ".join(
                "{}={!r}".format(k, v) for k, v in self._render_settings.items()
            ),
        )


class Input(BaseWidget):
    input_type: str = ""
    template: str = "input.html"

    @property
    def settings(self) -> Dict[str, Any]:
        base_settings = super().settings

        if hasattr(self, "input_type"):
            base_settings["type"] = self.input_type

        return base_settings

    def render(self, env: jinja2.Environment, **kwargs: Any) -> str:
        if not self.input_type:
            raise AttributeError(
                "Input is a base class, please use one of its children."
            )

        return super().render(env, **kwargs)


class TextInput(Input):
    input_type: str = "text"
    template: str = "text.html"


class EmailInput(Input):
    input_type: str = "email"
    template: str = "email.html"


class Checkbox(BaseWidget):
    template: str = "checkbox.html"
