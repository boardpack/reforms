import jinja2
from reforms import Reforms


def test_forms_from_directory(tmpdir):
    forms = Reforms(directory=str(tmpdir))
    assert isinstance(forms.env.loader, jinja2.FileSystemLoader)


def test_forms_with_directory_override(tmpdir):
    forms = Reforms(directory=str(tmpdir), package="reforms")
    assert isinstance(forms.env.loader, jinja2.ChoiceLoader)
