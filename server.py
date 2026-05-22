import math
import pythoncom
import win32com.client
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP Server for AutoCAD
mcp = FastMCP("AutoCAD")


def get_autocad():
    """
    Connects to an active running AutoCAD application using multiple strategies.
    """
    errors = []

    # Strategy 1: Standard Running Object Table lookup
    try:
        acad = win32com.client.GetActiveObject("AutoCAD.Application")
        acad.Visible = True
        return acad
    except Exception as e:
        errors.append(f"GetActiveObject: {e}")

    # Strategy 2: Dispatch — connects to running singleton instance
    try:
        acad = win32com.client.Dispatch("AutoCAD.Application")
        acad.Visible = True
        return acad
    except Exception as e:
        errors.append(f"Dispatch: {e}")

    # Strategy 3: GetObject with class moniker
    try:
        acad = win32com.client.GetObject(Class="AutoCAD.Application")
        acad.Visible = True
        return acad
    except Exception as e:
        errors.append(f"GetObject: {e}")

    raise RuntimeError(
        "Could not connect to AutoCAD.\n"
        + "\n".join(errors)
        + "\n\nFix: Run BOTH AutoCAD and terminal with the SAME privilege level."
    )


def to_acad_point(x, y, z=0.0):
    """Converts x, y, z coordinates to an AutoCAD compatible double array VARIANT."""
    return win32com.client.VARIANT(
        pythoncom.VT_ARRAY | pythoncom.VT_R8, (float(x), float(y), float(z))
    )


def refresh_screen(acad, doc):
    """
    Force AutoCAD to refresh its display so newly drawn objects become visible.
    Uses multiple methods for maximum compatibility.
    """
    try:
        doc.Regen(1)  # acAllViewports = 1
    except Exception:
        pass
    try:
        acad.ZoomExtents()
    except Exception:
        pass
    try:
        acad.Update()
    except Exception:
        pass
    try:
        doc.SendCommand("REGEN\n")
    except Exception:
        pass


def set_layer(doc, entity, layer_name):
    """
    Applies a layer name to an entity.
    Creates the layer automatically if it doesn't exist.
    """
    if not layer_name or layer_name == "0":
        return
    try:
        try:
            doc.Layers.Item(layer_name)
        except Exception:
            doc.Layers.Add(layer_name)
        entity.Layer = layer_name
    except Exception:
        pass


# ─── DRAWING TOOLS ───────────────────────────────────────────────

@mcp.tool()
def draw_line(x1: float, y1: float, x2: float, y2: float, layer: str = "0") -> str:
    """
    Draw a single line between two 2D points (x1, y1) and (x2, y2).
    The line will be immediately visible in AutoCAD.
    """
    pythoncom.CoInitialize()
    try:
        acad = get_autocad()
        doc = acad.ActiveDocument
        ms = doc.ModelSpace

        p1 = to_acad_point(x1, y1)
        p2 = to_acad_point(x2, y2)

        line = ms.AddLine(p1, p2)
        set_layer(doc, line, layer)
        refresh_screen(acad, doc)
        return f"SUCCESS: Line drawn from ({x1}, {y1}) to ({x2}, {y2}) on layer '{layer}'."
    except Exception as e:
        return f"ERROR: {str(e)}"
    finally:
        pythoncom.CoUninitialize()


@mcp.tool()
def draw_circle(cx: float, cy: float, radius: float, layer: str = "0") -> str:
    """
    Draw a circle centered at (cx, cy) with the specified radius.
    The circle will be immediately visible in AutoCAD.
    """
    pythoncom.CoInitialize()
    try:
        acad = get_autocad()
        doc = acad.ActiveDocument
        ms = doc.ModelSpace

        center = to_acad_point(cx, cy)
        circle = ms.AddCircle(center, float(radius))
        set_layer(doc, circle, layer)
        refresh_screen(acad, doc)
        return f"SUCCESS: Circle drawn at ({cx}, {cy}) radius {radius} on layer '{layer}'."
    except Exception as e:
        return f"ERROR: {str(e)}"
    finally:
        pythoncom.CoUninitialize()


@mcp.tool()
def draw_polyline(points: list[list[float]], is_closed: bool = False, layer: str = "0") -> str:
    """
    Draw a multi-segmented Lightweight Polyline (LWPolyline).
    'points' is a list of 2D coordinates: [[x1, y1], [x2, y2], [x3, y3], ...]
    The polyline will be immediately visible in AutoCAD.
    """
    pythoncom.CoInitialize()
    try:
        acad = get_autocad()
        doc = acad.ActiveDocument
        ms = doc.ModelSpace

        flat_points = []
        for p in points:
            if len(p) >= 2:
                flat_points.extend([float(p[0]), float(p[1])])

        if len(flat_points) < 4:
            return "ERROR: At least two 2D points are required."

        pts_variant = win32com.client.VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, flat_points)
        polyline = ms.AddLightweightPolyline(pts_variant)

        if is_closed:
            polyline.Closed = True

        set_layer(doc, polyline, layer)
        refresh_screen(acad, doc)
        return f"SUCCESS: Polyline with {len(points)} vertices on layer '{layer}' (Closed: {is_closed})."
    except Exception as e:
        return f"ERROR: {str(e)}"
    finally:
        pythoncom.CoUninitialize()


@mcp.tool()
def draw_rectangle(x: float, y: float, width: float, height: float, layer: str = "0") -> str:
    """
    Draw a rectangle starting at bottom-left corner (x, y) with given width and height.
    The rectangle will be immediately visible in AutoCAD.
    """
    pythoncom.CoInitialize()
    try:
        acad = get_autocad()
        doc = acad.ActiveDocument
        ms = doc.ModelSpace

        pts = [
            float(x), float(y),
            float(x + width), float(y),
            float(x + width), float(y + height),
            float(x), float(y + height),
        ]
        pts_variant = win32com.client.VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, pts)
        rect = ms.AddLightweightPolyline(pts_variant)
        rect.Closed = True
        set_layer(doc, rect, layer)
        refresh_screen(acad, doc)
        return f"SUCCESS: Rectangle at ({x}, {y}) size {width}x{height} on layer '{layer}'."
    except Exception as e:
        return f"ERROR: {str(e)}"
    finally:
        pythoncom.CoUninitialize()


@mcp.tool()
def add_text(text: str, x: float, y: float, height: float = 2.5, width: float = 0.0, layer: str = "0") -> str:
    """
    Add a multi-line text (MText) block at coordinates (x, y).
    The text will be immediately visible in AutoCAD.
    """
    pythoncom.CoInitialize()
    try:
        acad = get_autocad()
        doc = acad.ActiveDocument
        ms = doc.ModelSpace

        ins_point = to_acad_point(x, y)
        mtext = ms.AddMText(ins_point, float(width), text)
        mtext.Height = float(height)

        set_layer(doc, mtext, layer)
        refresh_screen(acad, doc)
        return f"SUCCESS: Text '{text}' at ({x}, {y}) height {height} on layer '{layer}'."
    except Exception as e:
        return f"ERROR: {str(e)}"
    finally:
        pythoncom.CoUninitialize()


# ─── LAYER & BLOCK TOOLS ────────────────────────────────────────

@mcp.tool()
def create_layer(name: str, color_index: int = 7) -> str:
    """
    Create a new layer with an optional ACI (AutoCAD Color Index) from 1 to 255.
    (e.g., 1=Red, 2=Yellow, 3=Green, 4=Cyan, 5=Blue, 6=Magenta, 7=White/Black).
    """
    pythoncom.CoInitialize()
    try:
        acad = get_autocad()
        doc = acad.ActiveDocument

        try:
            layer = doc.Layers.Item(name)
            status = "already exists (updated color)"
        except Exception:
            layer = doc.Layers.Add(name)
            status = "created"

        if 1 <= color_index <= 255:
            layer.Color = color_index

        return f"SUCCESS: Layer '{name}' {status} with color {color_index}."
    except Exception as e:
        return f"ERROR: {str(e)}"
    finally:
        pythoncom.CoUninitialize()


@mcp.tool()
def insert_block(block_name: str, x: float, y: float, scale: float = 1.0, rotation_deg: float = 0.0, layer: str = "0") -> str:
    """
    Insert a pre-defined Block Reference at coordinates (x, y).
    The block definition MUST already exist in the drawing.
    """
    pythoncom.CoInitialize()
    try:
        acad = get_autocad()
        doc = acad.ActiveDocument
        ms = doc.ModelSpace

        ins_point = to_acad_point(x, y)
        rad_rotation = math.radians(rotation_deg)

        block_ref = ms.InsertBlock(ins_point, block_name, scale, scale, scale, rad_rotation)
        set_layer(doc, block_ref, layer)
        refresh_screen(acad, doc)
        return f"SUCCESS: Block '{block_name}' at ({x}, {y}) scale {scale} rotation {rotation_deg}°."
    except Exception as e:
        return f"ERROR: {str(e)}"
    finally:
        pythoncom.CoUninitialize()


# ─── DIMENSION & HATCH TOOLS ────────────────────────────────────

@mcp.tool()
def add_dimension(x1: float, y1: float, x2: float, y2: float, text_x: float, text_y: float, layer: str = "0") -> str:
    """
    Add a linear aligned dimension between points (x1, y1) and (x2, y2).
    'text_x' and 'text_y' specify the position for the dimension text line.
    """
    pythoncom.CoInitialize()
    try:
        acad = get_autocad()
        doc = acad.ActiveDocument
        ms = doc.ModelSpace

        p1 = to_acad_point(x1, y1)
        p2 = to_acad_point(x2, y2)
        text_pos = to_acad_point(text_x, text_y)

        dim = ms.AddDimAligned(p1, p2, text_pos)
        set_layer(doc, dim, layer)
        refresh_screen(acad, doc)
        return f"SUCCESS: Dimension between ({x1}, {y1}) and ({x2}, {y2})."
    except Exception as e:
        return f"ERROR: {str(e)}"
    finally:
        pythoncom.CoUninitialize()


@mcp.tool()
def add_hatch(polyline_points: list[list[float]], pattern_name: str = "ANSI31", pattern_scale: float = 1.0, layer: str = "0") -> str:
    """
    Fills an enclosed boundary with a Hatch pattern.
    'polyline_points' is a list of 2D boundary points: [[x1, y1], [x2, y2], [x3, y3], ...]
    """
    pythoncom.CoInitialize()
    try:
        acad = get_autocad()
        doc = acad.ActiveDocument
        ms = doc.ModelSpace

        flat_points = []
        for p in polyline_points:
            if len(p) >= 2:
                flat_points.extend([float(p[0]), float(p[1])])

        if len(flat_points) < 6:
            return "ERROR: At least three 2D points are required."

        pts_variant = win32com.client.VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, flat_points)
        pline = ms.AddLightweightPolyline(pts_variant)
        pline.Closed = True

        hatch = ms.AddHatch(1, pattern_name, True)
        hatch.PatternScale = float(pattern_scale)

        boundary = win32com.client.VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_DISPATCH, [pline])
        hatch.AppendOuterLoop(boundary)
        hatch.Evaluate()

        set_layer(doc, pline, layer)
        set_layer(doc, hatch, layer)
        refresh_screen(acad, doc)
        return f"SUCCESS: Hatch '{pattern_name}' added on layer '{layer}'."
    except Exception as e:
        return f"ERROR: {str(e)}"
    finally:
        pythoncom.CoUninitialize()


# ─── CONTROL & INFO TOOLS ───────────────────────────────────────

@mcp.tool()
def zoom_extents() -> str:
    """
    Zoom Extents in AutoCAD to fit all objects in view.
    """
    pythoncom.CoInitialize()
    try:
        acad = get_autocad()
        acad.ZoomExtents()
        try:
            acad.ActiveDocument.Regen(1)
        except Exception:
            pass
        return "SUCCESS: Zoom Extents done."
    except Exception as e:
        return f"ERROR: {str(e)}"
    finally:
        pythoncom.CoUninitialize()


@mcp.tool()
def get_drawing_info() -> str:
    """
    Retrieve document filename, total object count, and layer list from active AutoCAD drawing.
    """
    pythoncom.CoInitialize()
    try:
        acad = get_autocad()
        doc = acad.ActiveDocument
        ms = doc.ModelSpace

        name = doc.Name
        count = ms.Count

        layers = []
        for i in range(doc.Layers.Count):
            layers.append(doc.Layers.Item(i).Name)

        return (
            f"Active File: {name}\n"
            f"Total Objects in ModelSpace: {count}\n"
            f"Layers: {', '.join(layers)}"
        )
    except Exception as e:
        return f"ERROR: {str(e)}"
    finally:
        pythoncom.CoUninitialize()


@mcp.tool()
def send_command(command_string: str) -> str:
    """
    Sends a raw command string directly to the AutoCAD command line.
    (e.g., 'ZOOM E', 'GRID ON', 'PURGE', 'REGEN').
    """
    pythoncom.CoInitialize()
    try:
        acad = get_autocad()
        doc = acad.ActiveDocument

        if not command_string.endswith("\n") and not command_string.endswith(" "):
            command_string += "\n"

        doc.SendCommand(command_string)
        return f"SUCCESS: Command '{command_string.strip()}' sent."
    except Exception as e:
        return f"ERROR: {str(e)}"
    finally:
        pythoncom.CoUninitialize()


if __name__ == "__main__":
    mcp.run(transport="stdio")
