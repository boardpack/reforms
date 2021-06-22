from typing import Any, Callable, Optional, Sequence

from pydantic.fields import ModelField

from .base import BaseValidator

__all__ = ["AnyOf"]


class AnyOf(BaseValidator):
    values: Sequence[Any]
    message: str = "Invalid value, must be one of: {values}."
    values_formatter: Optional[Callable[[Sequence[Any]], str]] = None

    def __call__(self, value: Any, field: ModelField) -> Any:
        if value in self.values:
            return value

        if not self.values_formatter:
            self.values_formatter = self.default_values_formatter

        raise ValueError(self.message.format(values=self.values_formatter(self.values)))

    @staticmethod
    def default_values_formatter(values: Sequence[Any]) -> str:
        return ", ".join(str(x) for x in values)
