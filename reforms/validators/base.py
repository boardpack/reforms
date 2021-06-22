import typing

from pydantic import BaseModel
from pydantic.fields import ModelField

__all__ = ["BaseValidator"]


class BaseValidator(BaseModel):
    def __call__(self, value: typing.Any, field: ModelField) -> typing.Any:
        return NotImplemented
