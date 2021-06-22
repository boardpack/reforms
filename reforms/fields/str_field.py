from typing import Any, Dict, List, Optional

from ..validators import BaseValidator
from .base import BaseField

__all__ = ["str_field"]


def str_field(
    *,
    field_id: str = "",
    field_class: str = "",
    label: str = "",
    placeholder: str = "",
    render_kw: Optional[Dict[str, Any]] = None,
    validators: Optional[List[BaseValidator]] = None,
) -> type:
    render_kw = render_kw or {}

    namespace = dict(
        template="forms/input.html",
        _validators=validators or [],
        _render_settings={
            "input_type": "text",
            "field_id": field_id,
            "field_class": field_class,
            "label": label,
            "placeholder": placeholder,
            **render_kw,
        },
    )

    return type("str_field", (str, BaseField), namespace)
