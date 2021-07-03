import sys
from typing import Union

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


def get_loader(
    forms: Reforms, index: int
) -> Union[jinja2.PackageLoader, jinja2.FileSystemLoader]:
    return forms.env.loader.loaders[index]


@pytest.mark.parametrize(
    ("directory", "package"),
    [
        (None, None),
        (pytest.lazy_fixture("tmpdir"), None),
        (None, pytest.lazy_fixture("template_package")),
        (pytest.lazy_fixture("tmpdir"), pytest.lazy_fixture("template_package")),
    ],
)
def test_default_loader(directory, package, default_package):
    forms = Reforms(directory=directory, package=package)

    assert isinstance(forms.env.loader, jinja2.ChoiceLoader)

    assert len(forms.env.loader.loaders) > 0
    assert isinstance(get_loader(forms, -1), jinja2.PackageLoader)
    assert get_loader(forms, -1).package_name == default_package


def test_directory_loader(tmpdir):
    forms = Reforms(directory=str(tmpdir))

    assert isinstance(get_loader(forms, 0), jinja2.FileSystemLoader)
    assert str(tmpdir) in get_loader(forms, 0).searchpath


def test_package_loader(template_package: str):
    forms = Reforms(package=template_package)

    assert isinstance(get_loader(forms, 0), jinja2.PackageLoader)
    assert get_loader(forms, 0).package_name == template_package


def test_package_and_directory_loader(tmpdir, template_package: str):
    forms = Reforms(directory=str(tmpdir), package=template_package)

    assert isinstance(get_loader(forms, 0), jinja2.FileSystemLoader)
    assert str(tmpdir) in get_loader(forms, 0).searchpath

    assert isinstance(get_loader(forms, 1), jinja2.PackageLoader)
    assert get_loader(forms, 1).package_name == template_package
