from pydantic import BaseModel, ValidationError, validator
from reforms import bool_field, str_field


class UserModel(BaseModel):
    name: str_field()
    is_admin: bool_field()
    username: str_field()
    password1: str_field()
    password2: str_field()

    @validator("name")
    def name_must_contain_space(cls, v):
        if " " not in v:
            raise ValueError("must contain a space")
        return v.title()

    @validator("password2")
    def passwords_match(cls, v, values):
        if "password1" in values and v != values["password1"]:
            raise ValueError("passwords do not match")
        return v

    @validator("username")
    def username_alphanumeric(cls, v):
        assert v.isalnum(), "must be alphanumeric"
        return v

    @validator("is_admin")
    def contains_admin_name(cls, v, values):
        if v and ("name" not in values or "admin" not in values["name"].lower()):
            raise ValueError('if user is admin, his name must contain "admin" part')

        return v


user = UserModel(
    name="samuel colvin admin",
    username="scolvin",
    password1="zxcvbn",
    password2="zxcvbn",
    is_admin=True,
)
print(user)

try:
    UserModel(
        name="samuel",
        username="scolvin",
        password1="zxcvbn",
        password2="zxcvbn2",
        is_admin=True,
    )
except ValidationError as e:
    print(e)
