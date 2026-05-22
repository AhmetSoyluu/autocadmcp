from __future__ import annotations


def build_layer_matrix() -> str:
    return (
        '(command "._-layer" '
        '"M" "A-WALL" "C" "9" "" '
        '"M" "A-AXIS" "C" "1" "L" "CENTER" "" '
        '"M" "S-COL" "C" "2" "" '
        '"M" "M-DUCT" "C" "4" "" '
        '"M" "M-PIPE" "C" "6" "" '
        '"M" "E-POWER" "C" "1" "" '
        '"M" "E-DATA" "C" "5" "" '
        '"M" "TXT-ANNO" "C" "7" "" '
        '"M" "E-ZA-YANGIN" "C" "2" "" '
        '"M" "E-ZA-CCTV" "C" "6" "" '
        '"M" "E-OG-TRAFO" "C" "1" "" '
        '"M" "E-AG-BUSBAR" "C" "4" "" '
        '"M" "E-KANAL" "C" "9" "" "")'
    )
