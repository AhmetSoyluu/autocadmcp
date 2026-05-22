# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development commands

Create and activate a virtual environment, then install dependencies:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -e .[dev]
```

Run the MCP server over stdio:

```bash
python -m autocad_mcp_server.main
```

Run all tests:

```bash
pytest
```

Run one unit test file:

```bash
pytest tests/unit/test_path_sandbox.py
```

Run one test by name:

```bash
pytest tests/unit/test_lisp_policy.py -k test_rejects_shell_primitives
```

Run integration tests only:

```bash
pytest -m integration
```

Run lint and type checks:

```bash
ruff check .
mypy src
```

Run coverage:

```bash
pytest --cov=autocad_mcp_server --cov-report=term-missing
```

## Architecture overview

This repository is a Python MCP server for AutoCAD automation on Windows. The design intentionally separates MCP-facing tools from AutoCAD process control.

`src/autocad_mcp_server/main.py` is the entrypoint. It loads settings, configures logging, builds the runtime services, and registers the MCP tools.

The tool modules under `src/autocad_mcp_server/tools/` should stay thin. They validate requests, call `DWGService`, and shape responses. Business decisions about execution mode belong in `src/autocad_mcp_server/services/dwg_service.py`, not in tool files.

There are two AutoCAD execution paths. Live desktop automation goes through COM in `src/autocad_mcp_server/services/interop_manager.py` and `src/autocad_mcp_server/adapters/com_adapter.py`. Background/offline processing goes through `accoreconsole.exe` in `src/autocad_mcp_server/services/core_console_manager.py` and `src/autocad_mcp_server/adapters/core_console_adapter.py`.

Core Console jobs must remain serialized through `src/autocad_mcp_server/services/execution_queue.py`. Do not bypass that queue from a tool or service.

The security boundary is centralized. Every incoming DWG path must go through `src/autocad_mcp_server/security/path_sandbox.py` before any file access, copy, open, or script generation. Every AutoLISP execution request must go through `src/autocad_mcp_server/security/lisp_policy.py` before it reaches COM or Core Console.

Structured request and response contracts live in `src/autocad_mcp_server/models/requests.py` and `src/autocad_mcp_server/models/responses.py`. Keep tool I/O changes aligned with these models and update tests when schemas change.

## Repository-specific constraints

Never open or modify a DWG path that has not been canonicalized and verified against `allowed_dwg_roots`.

Never execute raw AutoLISP directly from a tool. Route it through `LispPolicy` and `LispRunner` so blocked primitives, payload size limits, and execution depth limits stay enforced.

Never spawn `accoreconsole.exe` directly from a tool or adapter without going through the queue and timeout wrapper.

Graceful degradation matters here. COM failures, hung AutoCAD sessions, and Core Console timeouts should become structured errors instead of crashing the MCP process.
