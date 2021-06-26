from pydantic import BaseModel
from reforms import bool_field, email_field, str_field
from reforms.validators import Length


class UserModel(BaseModel):
    first_name: str_field(
        label="First Name",
        field_id="firstName",
        placeholder="John",
        validators=[Length(min=5)],
    )
    last_name: str_field(
        label="Last Name",
        field_id="lastName",
        placeholder="Doe",
        validators=[Length(min=5)],
    )
    email: email_field(
        label="Email",
        field_id="email",
        placeholder="john.doe@example.com",
    )
    has_github: bool_field(label="Has Github account?", field_id="hasGithub") = False
