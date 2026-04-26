"""Laboratuvar ve ilaç çakışması analizleri için iskelet."""

from __future__ import annotations

from typing import Any

from fastmcp import FastMCP

from fhir_nexus.fhir_client import FhirClient, FhirClientError
from fhir_nexus.utils.data_cleaner import compact_fhir_dict


def register(mcp: FastMCP) -> None:
    @mcp.tool()
    async def patient_observations(patient_id: str, count: int = 20) -> dict[str, Any]:
        """Hastaya ait Observation (lab/vital) özet listesi."""
        client = FhirClient()
        params = {"patient": patient_id, "_count": str(count), "_sort": "-date"}
        try:
            bundle = await client.get("Observation", params=params)
        except FhirClientError as e:
            return {"ok": False, "error": str(e)}
        return {"ok": True, "bundle": compact_fhir_dict(bundle)}

    @mcp.tool()
    async def patient_medications(patient_id: str, count: int = 50) -> dict[str, Any]:
        """Aktif / kayıtlı MedicationRequest kayıtları (çakışma analizi için ham veri)."""
        client = FhirClient()
        params = {"patient": patient_id, "_count": str(count)}
        try:
            bundle = await client.get("MedicationRequest", params=params)
        except FhirClientError as e:
            return {"ok": False, "error": str(e)}
        return {"ok": True, "bundle": compact_fhir_dict(bundle), "note": "Çakışma motoru henüz bağlı değil; veri toplama aşaması."}
