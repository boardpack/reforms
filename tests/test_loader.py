import sys

import jinja2
import pytest
from reforms import Reforms


@pytest.fixture
def default_package() -> str:
    return "reforms"


@pytest.fixture
def template_package(tmp_path) -> str:
    package_name = "template_package"

    package = tmp_path / package_name
    package.mkdir()
    (package / "templates").mkdir()
    (package / "templates" / "forms").mkdir()
    (package / "__init__.py").touch()

    sys.path.append(str(tmp_path))

    yield package_name

    sys.path.remove(str(tmp_path))


def test_environment_with_directory(tmpdir, default_package: str):
    forms = Reforms(directory=str(tmpdir))
    loaders = forms.env.loader.loaders

    assert isinstance(forms.env.loader, jinja2.ChoiceLoader)
    assert len(loaders) == 2
    assert isinstance(loaders[0], jinja2.FileSystemLoader)
    assert str(tmpdir) in loaders[0].searchpath
    assert isinstance(loaders[1], jinja2.PackageLoader)
    assert loaders[1].package_name == default_package


def test_environment_with_package(template_package: str, default_package: str):
    forms = Reforms(package=template_package)
    loaders = forms.env.loader.loaders

    assert isinstance(forms.env.loader, jinja2.ChoiceLoader)
    assert len(loaders) == 2
    assert isinstance(loaders[0], jinja2.PackageLoader)
    assert loaders[0].package_name == template_package
    assert isinstance(loaders[1], jinja2.PackageLoader)
    assert loaders[1].package_name == default_package


def test_environment_with_directory_and_package(
    tmpdir, template_package: str, default_package: str
):
    forms = Reforms(directory=str(tmpdir), package=template_package)
    loaders = forms.env.loader.loaders

    assert isinstance(forms.env.loader, jinja2.ChoiceLoader)
    assert len(loaders) == 3
    assert isinstance(loaders[0], jinja2.FileSystemLoader)
    assert str(tmpdir) in loaders[0].searchpath
    assert isinstance(loaders[1], jinja2.PackageLoader)
    assert loaders[1].package_name == template_package
    assert isinstance(loaders[2], jinja2.PackageLoader)
    assert loaders[2].package_name == default_package
