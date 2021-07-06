from typing import Any, Dict, List, Optional, Type

from ..validators import BaseValidator
from ..widgets import BaseWidget, HiddenInput
from .base import BaseField

__all__ = ["HiddenField"]


def HiddenField(
    *,
    widget: Type[BaseWidget] = HiddenInput,
    field_id: str = "",
    field_class: str = "",
    render_kw: Optional[Dict[str, Any]] = None,
    validators: Optional[List[BaseValidator]] = None,
) -> type:
    namespace = dict(
        widget=widget(
            field_id=field_id,
            field_class=field_class,
            **(render_kw or {}),
        ),
        _validators=validators or [],
    )

    return type("HiddenField", (str, BaseField), namespace)
