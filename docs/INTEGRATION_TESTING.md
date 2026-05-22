# Integration testing

These tests are marked with `@pytest.mark.integration` and are intended for Windows machines with AutoCAD installed.

## Required environment variables

- `AUTOCAD_MCP_ACAD_PATH`
- `AUTOCAD_MCP_ACCORECONSOLE_PATH`
- `AUTOCAD_MCP_ALLOWED_DWG_ROOTS`

## Run only integration tests

```bash
pytest -m integration
```

## Run one integration file

```bash
pytest tests/integration/test_core_console_metadata.py
```

## Notes

Unit tests are designed to run without AutoCAD. Integration tests should be run only after local paths and licenses are verified.
