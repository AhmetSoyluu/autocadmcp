from __future__ import annotations


def register_prompts(mcp) -> None:
    """Register MCP Prompts — intelligent CAD prompt templates."""

    @mcp.prompt()
    async def draw_floor_plan(
        width: float = 20.0,
        height: float = 15.0,
        num_rooms: int = 4,
        include_doors: bool = True,
        include_dimensions: bool = True,
    ) -> str:
        """Generate a floor plan layout with rooms, doors, and dimensions."""
        return f"""Create a floor plan with these specifications:
- Overall dimensions: {width}m x {height}m
- Number of rooms: {num_rooms}
- Include doors: {include_doors}
- Include dimensions: {include_dimensions}

Steps:
1. Create layers: A-WALL (color 1), A-DOOR (color 3), A-DIMS (color 6), A-ANNO (color 2)
2. Draw the outer walls as a rectangle at (0,0) to ({width},{height}) on layer A-WALL
3. Divide into {num_rooms} rooms with interior walls
4. {'Add door openings (0.9m wide) on layer A-DOOR' if include_doors else 'Skip doors'}
5. {'Add linear dimensions on layer A-DIMS' if include_dimensions else 'Skip dimensions'}
6. Add room labels as text on layer A-ANNO
7. Zoom extents

Use appropriate lineweights: outer walls 0.5mm, inner walls 0.35mm."""

    @mcp.prompt()
    async def create_title_block(
        company_name: str = "Company Name",
        project_name: str = "Project Name",
        sheet_size: str = "A3",
        scale: str = "1:100",
    ) -> str:
        """Generate a professional title block for a drawing sheet."""
        sizes = {"A4": (297, 210), "A3": (420, 297), "A2": (594, 420), "A1": (841, 594), "A0": (1189, 841)}
        w, h = sizes.get(sheet_size, (420, 297))
        return f"""Create a professional title block:
- Sheet size: {sheet_size} ({w}mm x {h}mm)
- Company: {company_name}
- Project: {project_name}
- Scale: {scale}

Steps:
1. Create layer G-ANNO-TTLB (color 7, lineweight 0.25mm)
2. Draw sheet border rectangle from (10,10) to ({w-10},{h-10})
3. Draw title block box in bottom-right corner ({w-180},{10}) to ({w-10},{10+50})
4. Add horizontal dividers within title block for:
   - Company name (top row, text height 5)
   - Project name (second row, text height 3.5)
   - Drawing title (third row, text height 3.5)
   - Scale: {scale} | Sheet: 1/1 | Date | Rev (bottom row, text height 2.5)
5. Add company logo placeholder
6. Set current layer back to 0"""

    @mcp.prompt()
    async def setup_drawing_standards(
        discipline: str = "architectural",
        unit_system: str = "metric",
    ) -> str:
        """Set up a drawing with proper standards, layers, and styles."""
        unit = "millimeters" if unit_system == "metric" else "inches"
        dim_scale = "1.0" if unit_system == "metric" else "25.4"
        return f"""Set up drawing standards for {discipline} work in {unit_system}:

1. **Units**: Set INSUNITS to {unit}, LUNITS to 2 (decimal), LUPREC to 4
2. **Layers** — Create standard {discipline} layers:
   - 0 (default, white)
   - A-WALL (red, lineweight 0.50)
   - A-WALL-INT (red, lineweight 0.35)
   - A-DOOR (green, lineweight 0.25)
   - A-GLAZ (green, lineweight 0.25)
   - A-COLS (red, lineweight 0.50)
   - A-DIMS (magenta, lineweight 0.18)
   - A-ANNO (yellow, lineweight 0.25)
   - A-FURN (cyan, lineweight 0.18)
   - A-EQPM (blue, lineweight 0.18)
   - A-SYMB (green, lineweight 0.25)
   - DEFPOINTS (no plot)
3. **Text Styles**:
   - Standard (Arial, height 0)
   - Title (Arial Bold, height 5)
   - Note (Arial, height 2.5)
4. **Dimension Style**:
   - Name: Standard-{unit_system[:3].upper()}
   - Text height: 2.5 in {unit}
   - Arrow size: 2.5
   - DIMSCALE: {dim_scale}
5. **Linetypes**: Load CENTER, DASHED, HIDDEN, PHANTOM
6. Save as template"""

    @mcp.prompt()
    async def batch_cleanup(
        folder_path: str = "",
        purge: bool = True,
        audit: bool = True,
        standardize_layers: bool = False,
    ) -> str:
        """Clean up multiple DWG files in a folder."""
        return f"""Batch cleanup DWG files{' in ' + folder_path if folder_path else ''}:

1. List all DWG files in the folder
2. For each file:
   {'- Run PURGE ALL to remove unused elements' if purge else ''}
   {'- Run AUDIT with fix option' if audit else ''}
   {'- Standardize layer names to AIA convention' if standardize_layers else ''}
   - Save the file
3. Generate a summary report with:
   - Files processed
   - Errors found and fixed per file
   - Space saved (before/after file sizes)"""

    @mcp.prompt()
    async def analyze_drawing(dwg_path: str = "") -> str:
        """Perform a comprehensive analysis of a drawing."""
        target = f" for {dwg_path}" if dwg_path else ""
        return f"""Perform comprehensive drawing analysis{target}:

1. **Entity Statistics**:
   - Count objects by type (object_count_by_type)
   - Calculate complexity score (drawing_complexity_score)

2. **Quality Checks**:
   - Detect duplicate objects (find_duplicate_objects)
   - Find unclosed polylines (detect_unclosed_polylines)
   - Check for overlapping entities (find_overlapping_objects)

3. **Layer Report**:
   - Generate layer usage report (layer_usage_report)
   - Identify unused layers

4. **Measurements**:
   - Calculate total line length per layer
   - Get drawing extents

5. **Text Audit**:
   - List all text objects (list_all_text)
   - Check for duplicate text

6. **BOM Generation**:
   - Generate bill of materials from blocks (generate_bom)

Present results in a structured summary table."""

    @mcp.prompt()
    async def create_detail_drawing(
        detail_type: str = "wall_section",
        scale: str = "1:10",
    ) -> str:
        """Generate a construction detail drawing."""
        return f"""Create a {detail_type} construction detail at {scale} scale:

1. Set up detail viewport/area
2. Create appropriate layers for the detail type
3. Draw the {detail_type} components:
   - Structure/framing
   - Insulation (hatch pattern)
   - Finishes
   - Connections/fasteners
4. Add:
   - Material callouts (leaders with text)
   - Dimensions (linear and angular)
   - Section markers
   - Scale reference
5. Add a detail title below: "{detail_type.replace('_', ' ').title()}" at {scale}"""

    @mcp.prompt()
    async def export_drawing_set(
        output_format: str = "pdf",
        include_layouts: bool = True,
    ) -> str:
        """Export a complete drawing set."""
        return f"""Export drawing set to {output_format.upper()}:

1. List all layouts in the drawing
2. For each layout:
   - Set appropriate page setup
   - Configure plot style (monochrome or color)
   - Export to {output_format.upper()}
3. {'Include all paper space layouts' if include_layouts else 'Export model space only'}
4. Name output files with layout names
5. Generate an index/summary of exported sheets"""

    @mcp.prompt()
    async def compare_revisions(
        drawing_a: str = "",
        drawing_b: str = "",
    ) -> str:
        """Compare two drawing revisions and generate a change report."""
        return f"""Compare drawing revisions:
- Drawing A (older): {drawing_a or '[specify path]'}
- Drawing B (newer): {drawing_b or '[specify path]'}

Steps:
1. Open both drawings
2. Use compare_drawings to find differences
3. Generate a report with:
   - Added entities (count and types)
   - Removed entities (count and types)
   - Modified entities
   - Layer changes
   - Block definition changes
4. Highlight areas of change in a markup drawing
5. Create a revision cloud around changed areas"""
