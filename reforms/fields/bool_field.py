from typing import Any, Dict, List, Optional, Type

from pydantic import StrictBool

from ..validators import BaseValidator
from ..widgets import BaseWidget, Checkbox
from .base import BaseField

__all__ = ["bool_field"]


def bool_field(
    *,
    widget: Type[BaseWidget] = Checkbox,
    field_id: str = "",
    field_class: str = "",
    label: str = "",
    disabled: bool = False,
    render_kw: Optional[Dict[str, Any]] = None,
    validators: Optional[List[BaseValidator]] = None,
) -> type:
    namespace = dict(
        widget=widget(
            field_id=field_id,
            field_class=field_class,
            label=label,
            disabled=disabled,
            **(render_kw or {}),
        ),
        _validators=validators or [],
    )

    return type("bool_field", (StrictBool, BaseField), namespace)
