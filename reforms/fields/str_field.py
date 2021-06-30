from typing import Any, Dict, List, Optional

from ..validators import BaseValidator
from ..widgets import TextInput
from .base import BaseField

__all__ = ["str_field"]


def str_field(
    *,
    field_id: str = "",
    field_class: str = "",
    label: str = "",
    placeholder: str = "",
    disabled: bool = False,
    render_kw: Optional[Dict[str, Any]] = None,
    validators: Optional[List[BaseValidator]] = None,
) -> type:
    render_kw = render_kw or {}

    namespace = dict(
        widget=TextInput(
            field_id=field_id,
            field_class=field_class,
            label=label,
            placeholder=placeholder,
            disabled=disabled,
            **render_kw,
        ),
        _validators=validators or [],
    )

    return type("str_field", (str, BaseField), namespace)
