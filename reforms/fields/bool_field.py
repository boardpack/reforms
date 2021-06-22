from typing import Any, Dict, List, Optional

from pydantic import StrictBool

from ..validators import BaseValidator
from .base import BaseField

__all__ = ["bool_field"]


def bool_field(
    *,
    field_id: str = "",
    field_class: str = "",
    label: str = "",
    render_kw: Optional[Dict[str, Any]] = None,
    validators: Optional[List[BaseValidator]] = None,
) -> type:
    render_kw = render_kw or {}

    namespace = dict(
        template="forms/checkbox.html",
        _validators=validators or [],
        _render_settings={
            "field_id": field_id,
            "field_class": field_class,
            "label": label,
            **render_kw,
        },
    )

    return type("bool_field", (StrictBool, BaseField), namespace)
