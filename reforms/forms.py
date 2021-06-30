from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence, Type, Union

import jinja2
from markupsafe import Markup
from pydantic import BaseModel, Protocol, StrBytes
from pydantic.fields import ModelField

from .fields.base import RenderField

__all__ = ["Form"]


class Form(BaseModel):
    env: jinja2.Environment
    model: Type[BaseModel]

    class Config:
        arbitrary_types_allowed = True

    def __str__(self) -> str:
        return self.render()

    def __html__(self) -> str:
        return self.render()

    def __getattr__(self, item: str) -> Any:
        if item in self.model.__fields__:
            field: ModelField = self.model.__fields__[item]
            return RenderField(env=self.env, data=field)

        return super().__getattr__(item)  # type: ignore

    def __call__(self, *args: Sequence[Any], **kwargs: Mapping[Any, Any]) -> BaseModel:
        return self.model(*args, **kwargs)

    def render(self) -> str:
        fields: Iterable[ModelField] = self.model.__fields__.values()
        return Markup(
            "<br>".join(str(RenderField(env=self.env, data=field)) for field in fields)
        )

    def parse_obj(self, obj: Any) -> BaseModel:  # type: ignore
        return self.model.parse_obj(obj)

    def parse_raw(  # type: ignore
        self,
        b: StrBytes,
        *,
        content_type: str = None,  # type: ignore
        encoding: str = "utf8",
        proto: Protocol = None,  # type: ignore
        allow_pickle: bool = False,
    ) -> BaseModel:
        return self.model.parse_raw(
            b=b,
            content_type=content_type,
            encoding=encoding,
            proto=proto,
            allow_pickle=allow_pickle,
        )

    def parse_file(  # type: ignore
        self,
        path: Union[str, Path],
        *,
        content_type: str = None,  # type: ignore
        encoding: str = "utf8",
        proto: Protocol = None,  # type: ignore
        allow_pickle: bool = False,
    ) -> BaseModel:
        return self.model.parse_file(
            path=path,
            content_type=content_type,
            encoding=encoding,
            proto=proto,
            allow_pickle=allow_pickle,
        )
