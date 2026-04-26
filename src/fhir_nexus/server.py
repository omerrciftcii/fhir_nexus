"""FHIR Nexus MCP sunucusu (FastMCP)."""

from __future__ import annotations

from fastmcp import FastMCP

from fhir_nexus.tools import clinical_analyzer, patient_orchestrator

mcp = FastMCP("fhir-nexus")

patient_orchestrator.register(mcp)
clinical_analyzer.register(mcp)


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
