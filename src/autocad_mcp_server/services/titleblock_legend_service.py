from __future__ import annotations


def build_title_block(x: float, y: float, title: str) -> str:
    return (
        f'(command "._rectang" "{x},{y}" "{x+260},{y+90}")\n'
        f'(command "._text" "J" "ML" "{x+10},{y+70}" "3" "0" "{title}")\n'
        f'(command "._text" "J" "ML" "{x+10},{y+45}" "2.2" "0" "PROJECT TITLE BLOCK")\n'
        f'(command "._text" "J" "ML" "{x+10},{y+20}" "2.2" "0" "DRAWN BY AUTOCADMCP")'
    )


def build_legend(x: float, y: float, items: list[str]) -> str:
    lines = [
        f'(command "._rectang" "{x},{y}" "{x+260},{y+140}")',
        f'(command "._text" "J" "ML" "{x+10},{y+120}" "3" "0" "SYMBOL LEGEND")',
    ]
    current_y = y + 95
    for item in items:
        lines.append(f'(command "._text" "J" "ML" "{x+10},{current_y}" "2.2" "0" "{item}")')
        current_y -= 18
    return "\n".join(lines)
