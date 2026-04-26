"""Hasta demografisi ve özet FHIR kaynakları."""

from __future__ import annotations

from typing import Any

from fastmcp import FastMCP

from fhir_nexus.fhir_client import FhirClient, FhirClientError
from fhir_nexus.utils.data_cleaner import compact_fhir_dict


def register(mcp: FastMCP) -> None:
    @mcp.tool()
    async def patient_demographics(patient_id: str) -> dict[str, Any]:
        """OpenEMR'den Patient kaynağını ID ile getirir (sadeleştirilmiş JSON)."""
        client = FhirClient()
        try:
            resource = await client.get(f"Patient/{patient_id}")
        except FhirClientError as e:
            return {"ok": False, "error": str(e)}
        return {"ok": True, "patient": compact_fhir_dict(resource)}

    @mcp.tool()
    async def patient_search(family: str | None = None, given: str | None = None) -> dict[str, Any]:
        """İsim ile Patient araması (family, given opsiyonel)."""
        client = FhirClient()
        params: dict[str, str] = {}
        if family:
            params["family"] = family
        if given:
            params["given"] = given
        try:
            bundle = await client.get("Patient", params=params or None)
        except FhirClientError as e:
            return {"ok": False, "error": str(e)}
        return {"ok": True, "bundle": compact_fhir_dict(bundle)}
