import typing

from pydantic import validator
from pydantic.fields import ModelField

from .base import BaseValidator

__all__ = ["Length"]


class Length(BaseValidator):
    max: int = -1
    min: int = -1
    message: str = ""

    @validator("min")
    def min_or_max(cls, v: int, values: typing.Any) -> int:
        if v == -1 and values["max"] == -1:
            raise ValueError("At least one of `min` or `max` must be specified.")
        if not (values["max"] == -1 or v <= values["max"]):
            raise ValueError("`min` cannot be more than `max`.")

        return v

    def __call__(self, value: typing.Any, field: ModelField) -> typing.Any:
        length = value and len(value) or 0
        if length >= self.min and (self.max == -1 or length <= self.max):
            return value

        if self.message:
            message = self.message
        elif self.max == -1:
            message = "Field must be at least {min} character long."
        elif self.min == -1:
            message = "Field cannot be longer than {max} character."
        elif self.min == self.max:
            message = "Field must be exactly {max} character long."
        else:
            message = "Field must be between {min} and {max} characters long."

        message_params = {
            name: value
            for name, value in (
                ("min", self.min),
                ("max", self.max),
                ("length", length),
            )
            if "{" + name + "}" in message
        }

        raise ValueError(message.format(**message_params))
