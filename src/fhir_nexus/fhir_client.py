"""OpenEMR FHIR API ile HTTP iletişimi."""

from __future__ import annotations

import os
from typing import Any

import httpx
from dotenv import load_dotenv

load_dotenv()


class FhirClientError(Exception):
    """FHIR isteği başarısız veya beklenmeyen yanıt."""


class FhirClient:
    """OpenEMR (veya uyumlu) FHIR sunucusuna yönelik ince HTTP sarmalayıcı."""

    def __init__(
        self,
        base_url: str | None = None,
        access_token: str | None = None,
        timeout: float = 30.0,
    ) -> None:
        self._base_url = (base_url or os.getenv("OPENEMR_BASE_URL", "")).rstrip("/")
        self._token = access_token or os.getenv("OPENEMR_ACCESS_TOKEN", "")
        self._timeout = timeout

    def _headers(self) -> dict[str, str]:
        h = {"Accept": "application/fhir+json", "Content-Type": "application/fhir+json"}
        if self._token:
            h["Authorization"] = f"Bearer {self._token}"
        return h

    def _url(self, path: str) -> str:
        path = path.lstrip("/")
        if not self._base_url:
            raise FhirClientError("OPENEMR_BASE_URL tanımlı değil.")
        return f"{self._base_url}/{path}"

    async def get(self, path: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=self._timeout) as client:
            r = await client.get(self._url(path), headers=self._headers(), params=params)
        if r.status_code >= 400:
            raise FhirClientError(f"GET {path} -> {r.status_code}: {r.text[:500]}")
        return r.json()
