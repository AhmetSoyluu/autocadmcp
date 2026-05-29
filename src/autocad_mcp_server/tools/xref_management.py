from __future__ import annotations

from autocad_mcp_server.models.requests import XrefManagementRequest
from autocad_mcp_server.services.dwg_service import DWGService
from autocad_mcp_server.tools.common import error_response, success_response


def register_xref_management_tool(mcp, service: DWGService) -> None:
    @mcp.tool()
    async def attach_xref(
        dwg_path: str,
        xref_path: str,
        x: float = 0,
        y: float = 0,
        scale: float = 1.0,
        rotation_deg: float = 0,
        execution_mode: str = "auto",
    ) -> dict:
        """Attach an external reference (xref) DWG file."""
        request = XrefManagementRequest(
            dwg_path=dwg_path, action="attach_xref",
            parameters={"xref_path": xref_path, "x": x, "y": y, "scale": scale, "rotation_deg": rotation_deg},
            execution_mode=execution_mode,
        )
        try:
            result = await service.execute_xref_management(request)
            return success_response("attach_xref", result.execution_mode, result.payload, result.warnings)
        except Exception as exc:
            return error_response("attach_xref", execution_mode, exc)

    @mcp.tool()
    async def detach_xref(dwg_path: str, xref_name: str, execution_mode: str = "auto") -> dict:
        """Detach (remove) an external reference from the drawing."""
        request = XrefManagementRequest(
            dwg_path=dwg_path, action="detach_xref",
            parameters={"xref_name": xref_name}, execution_mode=execution_mode,
        )
        try:
            result = await service.execute_xref_management(request)
            return success_response("detach_xref", result.execution_mode, result.payload, result.warnings)
        except Exception as exc:
            return error_response("detach_xref", execution_mode, exc)

    @mcp.tool()
    async def reload_xref(dwg_path: str, xref_name: str, execution_mode: str = "auto") -> dict:
        """Reload an external reference to reflect latest changes."""
        request = XrefManagementRequest(
            dwg_path=dwg_path, action="reload_xref",
            parameters={"xref_name": xref_name}, execution_mode=execution_mode,
        )
        try:
            result = await service.execute_xref_management(request)
            return success_response("reload_xref", result.execution_mode, result.payload, result.warnings)
        except Exception as exc:
            return error_response("reload_xref", execution_mode, exc)

    @mcp.tool()
    async def bind_xref(dwg_path: str, xref_name: str, execution_mode: str = "auto") -> dict:
        """Bind (embed) an external reference permanently into the drawing."""
        request = XrefManagementRequest(
            dwg_path=dwg_path, action="bind_xref",
            parameters={"xref_name": xref_name}, execution_mode=execution_mode,
        )
        try:
            result = await service.execute_xref_management(request)
            return success_response("bind_xref", result.execution_mode, result.payload, result.warnings)
        except Exception as exc:
            return error_response("bind_xref", execution_mode, exc)

    @mcp.tool()
    async def list_xrefs(dwg_path: str, execution_mode: str = "auto") -> dict:
        """List all external references in the drawing."""
        request = XrefManagementRequest(
            dwg_path=dwg_path, action="list_xrefs", execution_mode=execution_mode,
        )
        try:
            result = await service.execute_xref_management(request)
            return success_response("list_xrefs", result.execution_mode, result.payload, result.warnings)
        except Exception as exc:
            return error_response("list_xrefs", execution_mode, exc)

    @mcp.tool()
    async def attach_image(
        dwg_path: str,
        image_path: str,
        x: float = 0,
        y: float = 0,
        scale: float = 1.0,
        rotation_deg: float = 0,
        execution_mode: str = "auto",
    ) -> dict:
        """Attach a raster image to the drawing."""
        request = XrefManagementRequest(
            dwg_path=dwg_path, action="attach_image",
            parameters={"image_path": image_path, "x": x, "y": y, "scale": scale, "rotation_deg": rotation_deg},
            execution_mode=execution_mode,
        )
        try:
            result = await service.execute_xref_management(request)
            return success_response("attach_image", result.execution_mode, result.payload, result.warnings)
        except Exception as exc:
            return error_response("attach_image", execution_mode, exc)

    @mcp.tool()
    async def attach_pdf_underlay(
        dwg_path: str,
        pdf_path: str,
        x: float = 0,
        y: float = 0,
        scale: float = 1.0,
        page: int = 1,
        execution_mode: str = "auto",
    ) -> dict:
        """Attach a PDF file as an underlay."""
        request = XrefManagementRequest(
            dwg_path=dwg_path, action="attach_pdf_underlay",
            parameters={"pdf_path": pdf_path, "x": x, "y": y, "scale": scale, "page": page},
            execution_mode=execution_mode,
        )
        try:
            result = await service.execute_xref_management(request)
            return success_response("attach_pdf_underlay", result.execution_mode, result.payload, result.warnings)
        except Exception as exc:
            return error_response("attach_pdf_underlay", execution_mode, exc)
