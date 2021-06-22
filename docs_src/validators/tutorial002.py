from pydantic import BaseModel, ValidationError
from reforms import str_field
from reforms.validators import Length, Required


class ContactUsModel(BaseModel):
    name: str_field(validators=[Length(min=5), Required()])
    message: str_field(validators=[Required(message="Message is required")])


contact = ContactUsModel(name="Roman", message="Some message")
print(contact)

try:
    ContactUsModel(
        message="Temp",
    )
except ValidationError as e:
    print(e)

try:
    ContactUsModel(
        name="Dan",
    )
except ValidationError as e:
    print(e)
