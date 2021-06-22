import typing

from pydantic.fields import ModelField

from .base import BaseValidator

__all__ = ["Required"]


class Required(BaseValidator):
    message: str = "This field is required."

    def __call__(self, value: typing.Any, field: ModelField) -> typing.Any:
        if value and (not isinstance(value, str) or value.strip()):
            return value

        raise ValueError(self.message)
