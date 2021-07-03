from pydantic import BaseModel, ValidationError
from reforms import StringField
from reforms.validators import Length


class ContactUsModel(BaseModel):
    name: StringField(validators=[Length(min=5)])
    message: StringField()


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
