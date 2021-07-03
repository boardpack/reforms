from typing import Any, Callable, Dict, Type

from fastapi.requests import Request
from pydantic import BaseModel, StrictBool
from pydantic.fields import ModelField

__all__ = ["from_model"]


def from_model(model: Type[BaseModel]) -> Callable[[Request], Any]:
    """This is a helper to convert raw form data into Pydantic model with help of the
    FastAPI Dependency Injection system (Depends function):

        class UserModel(pydantic.BaseModel):
            name = reforms.str_field(...)
            email = reforms.email_field(...)

        # ...

        @app.post("/", response_class=RedirectResponse)
        async def handle_form(form: from_model(UserModel) = Depends()):
            print(form)
            return RedirectResponse("/", status_code=HTTP_302_FOUND)

    """

    def _convert_bool_value(field: ModelField, form: Dict[str, Any]) -> bool:
        if field.required or field.name in form:
            return field.name in form

        return field.default

    async def _from_model(request: Request) -> Any:
        form = dict(await request.form())

        for field in model.__fields__.values():
            if issubclass(field.type_, StrictBool):
                form[field.name] = _convert_bool_value(field, form)

        return model.parse_obj(form)

    return _from_model
