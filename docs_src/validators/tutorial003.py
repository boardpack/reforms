from typing import Callable

from pydantic import BaseModel, ValidationError
from reforms import str_field


def has_lines(n: int = 2) -> Callable:
    def _has_lines(value: str):
        if len(value.split("\n")) < n:
            raise ValueError(f"Value doesn't contain minimum {n} lines")

        return value

    return _has_lines


class MessageModel(BaseModel):
    content: str_field(validators=[has_lines(n=3)])


contact = MessageModel(
    content="""
First sentence.
Second sentence.
Third sentence"""
)

print(contact)

try:
    MessageModel(content="One line")
except ValidationError as e:
    print(e)
