from typing import Any, Dict, List, Optional

from pydantic import EmailStr

from ..validators import BaseValidator
from .base import BaseField

__all__ = ["email_field"]


def email_field(
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
        template="forms/input.html",
        _validators=validators or [],
        _render_settings={
            "input_type": "email",
            "field_id": field_id,
            "field_class": field_class,
            "label": label,
            "placeholder": placeholder,
            "disabled": disabled,
            **render_kw,
        },
    )

    return type("email_field", (EmailStr, BaseField), namespace)
