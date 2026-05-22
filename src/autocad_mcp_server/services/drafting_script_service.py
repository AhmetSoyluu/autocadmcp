from __future__ import annotations

from pathlib import Path

from autocad_mcp_server.models.requests import GenerateElectricalBlueprintRequest
from autocad_mcp_server.security.lisp_policy import LispPolicy
from autocad_mcp_server.services.generators import (
    build_architecture,
    build_electrical,
    build_mechanical,
    build_structure,
    build_weak_current,
)
from autocad_mcp_server.services.layer_profile_service import build_layer_matrix
from autocad_mcp_server.services.layout_geometry_service import legend_origin, title_block_origin
from autocad_mcp_server.services.titleblock_legend_service import build_legend, build_title_block
from autocad_mcp_server.utils.temp_workspace import TempWorkspaceManager


class DraftingScriptService:
    def __init__(self, workspace_manager: TempWorkspaceManager, lisp_policy: LispPolicy) -> None:
        self.workspace_manager = workspace_manager
        self.lisp_policy = lisp_policy

    def _discipline_commands(self, request: GenerateElectricalBlueprintRequest) -> list[str]:
        if request.discipline == "architecture":
            return build_architecture(request)
        if request.discipline == "structure":
            return build_structure(request)
        if request.discipline == "mechanical":
            return build_mechanical(request)
        if request.discipline == "electrical":
            return build_electrical(request)
        if request.discipline == "weak_current":
            return build_weak_current(request)
        return [
            *build_architecture(request),
            *build_structure(request),
            *build_mechanical(request),
            *build_electrical(request),
            *build_weak_current(request),
        ]

    def build_lsp(self, request: GenerateElectricalBlueprintRequest) -> str:
        x, y = request.base_point
        title_x, title_y = title_block_origin(x, y, request.sheet_width)
        legend_x, legend_y = legend_origin(x, y, request.legend_offset_x, request.legend_offset_y)
        legend_items = [
            "WALL = Architectural Wall",
            "AXIS = Structural Grid",
            "DUCT = Mechanical Duct",
            "TRAFO = Transformer",
            "DATA = Weak Current Outlet",
        ]
        commands = [
            '(defun c:GENERATE_UNIVERSAL_DRAFT ()',
            build_layer_matrix(),
            *self._discipline_commands(request),
            build_title_block(title_x, title_y, request.title_block_title),
            build_legend(legend_x, legend_y, legend_items),
            '(princ)',
            ')',
            '(c:GENERATE_UNIVERSAL_DRAFT)',
        ]
        source = "\n".join(commands) + "\n"
        self.lisp_policy.validate(source)
        return source

    def build_scr(self, lsp_path: Path) -> str:
        safe = lsp_path.as_posix().replace('"', '')
        return f'._filedia 0\n(load "{safe}")\n._qsave\n'

    def generate(self, request: GenerateElectricalBlueprintRequest) -> dict[str, object]:
        workspace = self.workspace_manager.create("blueprint")
        lsp_path = workspace / f"{request.output_name}.lsp"
        scr_path = workspace / f"{request.output_name}.scr"
        lsp_source = self.build_lsp(request)
        scr_source = self.build_scr(lsp_path)
        lsp_path.write_text(lsp_source, encoding="utf-8")
        scr_path.write_text(scr_source, encoding="utf-8")
        self.workspace_manager.write_manifest(
            workspace,
            {
                "project_name": request.project_name,
                "discipline": request.discipline,
                "systems": request.systems,
                "artifacts": [str(lsp_path), str(scr_path)],
                "drawing_standard": request.drawing_standard,
            },
        )
        return {
            "workspace": str(workspace),
            "lsp_path": str(lsp_path),
            "scr_path": str(scr_path),
            "generated_files": [str(lsp_path), str(scr_path)],
            "preview_summary": {
                "discipline": request.discipline,
                "systems": request.systems,
                "drawing_standard": request.drawing_standard,
            },
        }
