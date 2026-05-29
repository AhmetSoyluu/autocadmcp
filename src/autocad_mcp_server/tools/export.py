from __future__ import annotations

from autocad_mcp_server.models.requests import ExportRequest
from autocad_mcp_server.services.dwg_service import DWGService
from autocad_mcp_server.tools.common import error_response, success_response


def register_export_tool(mcp, service: DWGService) -> None:
    @mcp.tool()
    async def export_to_pdf(
        dwg_path: str,
        output_path: str = "",
        layout_name: str = "Model",
        paper_size: str = "A3",
        scale: float = 1.0,
        color_mode: str = "color",
        execution_mode: str = "auto",
    ) -> dict:
        """Export the drawing to a PDF file."""
        request = ExportRequest(
            dwg_path=dwg_path, format="pdf",
            output_path=output_path, layout_name=layout_name,
            paper_size=paper_size, scale=scale, color_mode=color_mode,
            execution_mode=execution_mode,
        )
        try:
            result = await service.execute_export(request)
            return success_response("export_to_pdf", result.execution_mode, result.payload, result.warnings)
        except Exception as exc:
            return error_response("export_to_pdf", execution_mode, exc)

    @mcp.tool()
    async def export_to_dxf(
        dwg_path: str,
        output_path: str = "",
        execution_mode: str = "auto",
    ) -> dict:
        """Export the drawing to DXF format."""
        request = ExportRequest(
            dwg_path=dwg_path, format="dxf", output_path=output_path,
            execution_mode=execution_mode,
        )
        try:
            result = await service.execute_export(request)
            return success_response("export_to_dxf", result.execution_mode, result.payload, result.warnings)
        except Exception as exc:
            return error_response("export_to_dxf", execution_mode, exc)

    @mcp.tool()
    async def export_to_dwf(
        dwg_path: str,
        output_path: str = "",
        execution_mode: str = "auto",
    ) -> dict:
        """Export the drawing to DWF/DWFx format."""
        request = ExportRequest(
            dwg_path=dwg_path, format="dwf", output_path=output_path,
            execution_mode=execution_mode,
        )
        try:
            result = await service.execute_export(request)
            return success_response("export_to_dwf", result.execution_mode, result.payload, result.warnings)
        except Exception as exc:
            return error_response("export_to_dwf", execution_mode, exc)

    @mcp.tool()
    async def export_to_image(
        dwg_path: str,
        output_path: str = "",
        format: str = "png",
        resolution_dpi: int = 300,
        execution_mode: str = "auto",
    ) -> dict:
        """Export the drawing to a raster image (PNG, JPG, or BMP)."""
        request = ExportRequest(
            dwg_path=dwg_path, format=format, output_path=output_path,
            resolution_dpi=resolution_dpi, execution_mode=execution_mode,
        )
        try:
            result = await service.execute_export(request)
            return success_response("export_to_image", result.execution_mode, result.payload, result.warnings)
        except Exception as exc:
            return error_response("export_to_image", execution_mode, exc)

    @mcp.tool()
    async def export_to_stl(
        dwg_path: str,
        output_path: str = "",
        execution_mode: str = "auto",
    ) -> dict:
        """Export 3D solids to STL format for 3D printing."""
        request = ExportRequest(
            dwg_path=dwg_path, format="stl", output_path=output_path,
            execution_mode=execution_mode,
        )
        try:
            result = await service.execute_export(request)
            return success_response("export_to_stl", result.execution_mode, result.payload, result.warnings)
        except Exception as exc:
            return error_response("export_to_stl", execution_mode, exc)

    @mcp.tool()
    async def export_layer_to_pdf(
        dwg_path: str,
        layers: list[str],
        output_path: str = "",
        paper_size: str = "A3",
        execution_mode: str = "auto",
    ) -> dict:
        """Export only specific layers to a PDF file."""
        request = ExportRequest(
            dwg_path=dwg_path, format="pdf", output_path=output_path,
            layers_to_include=layers, paper_size=paper_size,
            execution_mode=execution_mode,
        )
        try:
            result = await service.execute_export(request)
            return success_response("export_layer_to_pdf", result.execution_mode, result.payload, result.warnings)
        except Exception as exc:
            return error_response("export_layer_to_pdf", execution_mode, exc)
