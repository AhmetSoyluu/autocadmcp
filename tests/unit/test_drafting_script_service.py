import json
from pathlib import Path

from autocad_mcp_server.models.requests import GenerateElectricalBlueprintRequest
from autocad_mcp_server.security.lisp_policy import LispPolicy
from autocad_mcp_server.services.drafting_script_service import DraftingScriptService
from autocad_mcp_server.utils.temp_workspace import TempWorkspaceManager


def test_drafting_service_generates_mixed_lsp_and_scr(tmp_path: Path) -> None:
    service = DraftingScriptService(TempWorkspaceManager(tmp_path), LispPolicy(max_chars=40000, max_depth=64))
    request = GenerateElectricalBlueprintRequest(
        project_name='Hospital Campus',
        discipline='mixed',
        systems=['yangin', 'cctv', 'trafo'],
        output_name='hospital_blueprint',
    )

    payload = service.generate(request)

    lsp_path = Path(payload['lsp_path'])
    scr_path = Path(payload['scr_path'])
    assert lsp_path.exists()
    assert scr_path.exists()
    lsp_text = lsp_path.read_text(encoding='utf-8')
    assert 'A-WALL' in lsp_text
    assert 'S-COL' in lsp_text
    assert 'M-DUCT' in lsp_text
    assert 'E-OG-TRAFO' in lsp_text
    assert 'SYMBOL LEGEND' in lsp_text
    assert 'PROJECT TITLE BLOCK' in lsp_text
    assert '._arc' in lsp_text
    assert '._rectang' in lsp_text


def test_drafting_service_includes_bypass_and_break_logic(tmp_path: Path) -> None:
    service = DraftingScriptService(TempWorkspaceManager(tmp_path), LispPolicy(max_chars=40000, max_depth=64))
    request = GenerateElectricalBlueprintRequest(
        project_name='Bypass Test',
        discipline='mixed',
        systems=['data', 'wall'],
        output_name='bypass_test',
    )

    payload = service.generate(request)
    lsp_text = Path(payload['lsp_path']).read_text(encoding='utf-8')

    assert '._break' in lsp_text
    assert '._arc' in lsp_text


def test_drafting_service_writes_manifest_with_artifacts(tmp_path: Path) -> None:
    service = DraftingScriptService(TempWorkspaceManager(tmp_path), LispPolicy(max_chars=40000, max_depth=64))
    request = GenerateElectricalBlueprintRequest(
        project_name='Factory',
        discipline='electrical',
        systems=['busbar'],
        output_name='factory_power',
    )

    payload = service.generate(request)
    manifest_path = Path(payload['workspace']) / 'manifest.json'
    manifest = json.loads(manifest_path.read_text(encoding='utf-8'))

    assert manifest['project_name'] == 'Factory'
    assert manifest['discipline'] == 'electrical'
    assert len(manifest['artifacts']) == 2
