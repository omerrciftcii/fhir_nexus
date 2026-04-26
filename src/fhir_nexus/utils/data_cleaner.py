"""FHIR JSON yanıtlarını sadeleştirme (MCP çıktısı için)."""

from __future__ import annotations

from typing import Any


def compact_fhir_dict(obj: Any, *, max_depth: int = 12) -> Any:
    """
    None değerlerini ve boş koleksiyonları kaldırır; iç içe dict/list üzerinde dolaşır.
    Derinlik sınırı sonsuz FHIR ağaçlarında MCP token patlamasını önler.
    """
    if max_depth < 0:
        return None

    if isinstance(obj, dict):
        out: dict[str, Any] = {}
        for k, v in obj.items():
            if v is None:
                continue
            inner = compact_fhir_dict(v, max_depth=max_depth - 1)
            if inner is None:
                continue
            if inner == {} or inner == []:
                continue
            out[k] = inner
        return out

    if isinstance(obj, list):
        items = [compact_fhir_dict(x, max_depth=max_depth - 1) for x in obj]
        items = [x for x in items if x is not None and x != {} and x != []]
        return items

    return obj
