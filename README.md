# AutoCAD MCP Server

AutoCAD MCP Server is a Windows-focused, security-first MCP server for interacting with DWG files through either a live AutoCAD desktop session (COM Interop) or background execution with `accoreconsole.exe`.

Python is used instead of TypeScript because Windows COM automation is more mature and stable through `pywin32`, and the same runtime can also manage `accoreconsole.exe` processes, timeouts, temp workspaces, and path sandboxing with less integration overhead.

## Features

The server exposes four MCP tools:

- `read_dwg_metadata`: returns layers, block references, text/mtext content, and drawing summary as JSON.
- `execute_autolisp`: runs policy-checked AutoLISP in either a live session or a background console run.
- `query_geometry`: returns entity coordinates, bounding boxes, lengths, and areas.
- `manage_layers_and_blocks`: creates and changes layers, and inserts blocks with validated parameters.

## Security model

This server is intentionally restrictive.

Only DWG files under configured allowed roots can be opened. All incoming paths are normalized and validated against path traversal and sandbox escape attempts. Core Console jobs run through a single queue to prevent process collisions. AutoLISP execution is blocked unless the request passes the built-in policy checks.

## Requirements

- Windows 10 or 11
- Python 3.11+
- AutoCAD installed locally
- `acad.exe` for live COM operations
- `accoreconsole.exe` for background/offline operations

## Setup

Create a virtual environment and install dependencies:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -e .[dev]
```

Copy the environment template and adjust paths:

```bash
copy .env.example .env
```

## Run the server

Start the MCP server over stdio:

```bash
python -m autocad_mcp_server.main
```

Or use the installed entry point:

```bash
autocad-mcp-server
```

## Tests

Run all unit tests:

```bash
pytest
```

Run one test file:

```bash
pytest tests/unit/test_path_sandbox.py
```

Run one test by name:

```bash
pytest tests/unit/test_lisp_policy.py -k test_rejects_shell_primitives
```

Run integration tests only on a Windows machine with AutoCAD installed:

```bash
pytest -m integration
```

## Claude Desktop configuration

Use `docs/claude_desktop_config.example.json` as a template. The config should point to Python and set environment variables instead of hardcoding sensitive or machine-specific values into the repository.

## Architecture

The server keeps the tool layer thin. MCP tools validate structured requests, then delegate into `DWGService`, which decides whether to use COM or Core Console. Path validation is centralized in `security/path_sandbox.py`. AutoLISP is always checked by `security/lisp_policy.py`. Core Console execution is serialized through `services/execution_queue.py` and `services/core_console_manager.py`. Live AutoCAD access is isolated in `services/interop_manager.py` and `adapters/com_adapter.py`.
