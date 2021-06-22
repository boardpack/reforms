from pathlib import Path
from typing import Any, Iterable, Mapping, Optional, Sequence, Type, Union

try:
    import jinja2
except ImportError:  # pragma: no cover
    jinja2 = None  # type: ignore

from markupsafe import Markup
from pydantic import BaseModel, Protocol, StrBytes
from pydantic.fields import ModelField

from .fields import BaseField

__all__ = ["Reforms"]


class Form(BaseModel):
    env: jinja2.Environment
    model: Type[BaseModel]

    class Config:
        arbitrary_types_allowed = True

    class _RenderField(BaseModel):
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
            return field_type.render(self.env, self.data)

    def __str__(self) -> str:
        return self.render()

    def __html__(self) -> str:
        return self.render()

    def __getattr__(self, item: str) -> Any:
        if item in self.model.__fields__:
            field: ModelField = self.model.__fields__[item]
            return self._RenderField(env=self.env, data=field)

        return super().__getattr__(item)  # type: ignore

    def __call__(self, *args: Sequence[Any], **kwargs: Mapping[Any, Any]) -> BaseModel:
        return self.model(*args, **kwargs)

    def render(self) -> str:
        fields: Iterable[ModelField] = self.model.__fields__.values()
        return Markup(
            "<br>".join(
                str(self._RenderField(env=self.env, data=field)) for field in fields
            )
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


class Reforms:
    def __init__(
        self, *, directory: Optional[str] = None, package: Optional[str] = None
    ) -> None:
        assert (
            directory is not None or package is not None
        ), "Either 'directory' or 'package' must be specified."
        self.env = self.load_template_env(directory=directory, package=package)

    def load_template_env(
        self, *, directory: Optional[str] = None, package: Optional[str] = None
    ) -> "jinja2.Environment":
        loader: jinja2.BaseLoader
        if directory is not None and package is None:
            loader = jinja2.FileSystemLoader(directory)
        elif directory is None and package is not None:
            loader = jinja2.PackageLoader(package, "templates")
        else:
            assert directory is not None
            assert package is not None
            loader = jinja2.ChoiceLoader(
                [
                    jinja2.FileSystemLoader(directory),
                    jinja2.PackageLoader(package, "templates"),
                ]
            )
        return jinja2.Environment(loader=loader, autoescape=True)

    def Form(self, model: Type[BaseModel]) -> Form:
        return Form(env=self.env, model=model)
