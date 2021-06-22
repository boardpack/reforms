import uvicorn
from fastapi import Depends, FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.status import HTTP_302_FOUND
from reforms import Reforms, on_model

from models import UserModel

app = FastAPI()

forms = Reforms(package="reforms")

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    user_form = forms.Form(UserModel)

    return templates.TemplateResponse(
        "index.html",
        {"request": request, "form": user_form},
    )


@app.post("/", response_class=RedirectResponse)
async def handle_form(form: UserModel = Depends(on_model(UserModel))):
    print(form)
    return RedirectResponse("/", status_code=HTTP_302_FOUND)


if __name__ == "__main__":
    uvicorn.run(app)
