import pytest

from reforms import Reforms


@pytest.fixture()
def forms() -> Reforms:
    default_forms = Reforms(package="reforms")
    return default_forms
