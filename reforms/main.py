from typing import List, Optional, Type

import jinja2
from pydantic import BaseModel

from .forms import Form

__all__ = ["Reforms"]


class Reforms:
    default_package_path: str = "templates/forms"
    default_template_package: str = "reforms"

    def __init__(
        self, *, directory: Optional[str] = None, package: Optional[str] = None
    ) -> None:
        self.env = self.load_template_env(directory=directory, package=package)

    def load_template_env(
        self, *, directory: Optional[str] = None, package: Optional[str] = None
    ) -> "jinja2.Environment":
        loaders: List[jinja2.BaseLoader] = [
            jinja2.PackageLoader(
                self.default_template_package, self.default_package_path
            )
        ]

        if package and package != self.default_template_package:
            loaders.append(jinja2.PackageLoader(package, self.default_package_path))
        if directory:
            loaders.append(jinja2.FileSystemLoader(directory))

        loaders.reverse()
        return jinja2.Environment(loader=jinja2.ChoiceLoader(loaders), autoescape=True)

    def Form(self, model: Type[BaseModel]) -> Form:
        return Form(env=self.env, model=model)
