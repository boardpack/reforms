import itertools
from typing import Iterable, List

import jinja2
from pydantic import BaseModel
from pydantic.fields import ModelField
from pydantic.utils import Representation

from ..validators import BaseValidator
from ..widgets import BaseWidget

__all__ = ("BaseField", "RenderField")


class BaseField(Representation):
    widget: BaseWidget
    _validators: List[BaseValidator] = []

    @classmethod
    def __get_validators__(cls) -> Iterable[BaseValidator]:
        return itertools.chain(cls._validators)


class RenderField(BaseModel):
    env: jinja2.Environment
    data: ModelField

    class Config:
        arbitrary_types_allowed = True

    def __html__(self) -> str:
        return str(self)

    def __repr__(self) -> str:
        return repr(self.data)

    def __str__(self) -> str:
        field_type: BaseField = self.data.type_

        if self.data.required and field_type.widget.settings.get("disabled"):
            raise ValueError(
                f"You can't render {self.data.name} because of it has disabled option "
                "and doesn't have a default value"
            )

        return field_type.widget.render(
            self.env,
            name=self.data.name,
            required=self.data.required,
            default=self.data.default,
        )
