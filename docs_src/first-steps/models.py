from pydantic import BaseModel
from reforms import BooleanField, EmailField, StringField
from reforms.validators import Length


class UserModel(BaseModel):
    first_name: StringField(
        label="First Name",
        field_id="firstName",
        placeholder="John",
        validators=[Length(min=5)],
    )
    last_name: StringField(
        label="Last Name",
        field_id="lastName",
        placeholder="Doe",
        validators=[Length(min=5)],
    )
    email: EmailField(
        label="Email",
        field_id="email",
        placeholder="john.doe@example.com",
    )
    has_github: BooleanField(label="Has Github account?", field_id="hasGithub") = False
