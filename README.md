# FHIR-Nexus MCP

An autonomous, Enterprise-Grade Medical Data Orchestrator for LLMs. Securely ingests, cleans, and orchestrates FHIR resources from OpenEMR using the Model Context Protocol.

## Architecture
- **FHIR API Client:** OAuth2 / SMART on FHIR integration.
- **Data Preprocessing:** Pandas-based clinical data cleaner.
- **MCP Server:** FastMCP integration for autonomous AI tool calling.
