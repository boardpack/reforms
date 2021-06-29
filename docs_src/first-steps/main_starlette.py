import uvicorn
from starlette.applications import Starlette
from starlette.routing import Route
from starlette.requests import Request
from starlette.responses import RedirectResponse
from starlette.templating import Jinja2Templates
from starlette.status import HTTP_302_FOUND
from reforms import Reforms

from models import UserModel

forms = Reforms(package="reforms")

templates = Jinja2Templates(directory="templates")


async def index(request: Request):
    user_form = forms.Form(UserModel)

    return templates.TemplateResponse(
        "index.html",
        {"request": request, "form": user_form},
    )


async def handle_form(request: Request):
    raw_form = await request.form()
    form = UserModel(**raw_form)

    print(form)
    return RedirectResponse("/", status_code=HTTP_302_FOUND)


if __name__ == "__main__":
    app = Starlette(
        routes=[
            Route('/', endpoint=index),
            Route('/', endpoint=handle_form, methods=["POST"]),
        ],
    )
    uvicorn.run(app)

