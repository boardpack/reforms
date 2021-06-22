from typing import Any, Callable

from pydantic import BaseModel
from starlette.requests import Request

from .fields import bool_field

__all__ = ["on_model"]


def on_model(model: BaseModel) -> Callable[[Request], Any]:
    """This is a helper to convert raw form data into Pydantic model with help of the
    FastAPI Dependency Injection system (Depends function):

        class UserModel(pydantic.BaseModel):
            name = reforms.str_field(...)
            email = reforms.email_field(...)

        # ...

        @app.post("/", response_class=RedirectResponse)
        async def handle_form(form: UserModel = Depends(on_model(UserModel))):
            print(form)
            return RedirectResponse("/", status_code=HTTP_302_FOUND)

    """

    async def _on_model(request: Request) -> Any:
        form = dict(await request.form())

        for field in model.__fields__.values():
            # convert checkbox value into bool type
            if field.type_.__name__ == bool_field().__name__ and field.name in form:
                form[field.name] = form[field.name] == "on"  # type: ignore

        return model.parse_obj(form)

    return _on_model
