from typing import Any, Callable, Type

from fastapi.requests import Request
from pydantic import BaseModel

from ...fields import bool_field

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

    async def _from_model(request: Request) -> Any:
        form = dict(await request.form())

        for field in model.__fields__.values():
            # convert checkbox value into bool type
            if field.type_.__name__ == bool_field().__name__:
                if field.required:
                    form[field.name] = field.name in form  # type: ignore
                else:
                    form[field.name] = True if field.name in form else field.default

        return model.parse_obj(form)

    return _from_model
