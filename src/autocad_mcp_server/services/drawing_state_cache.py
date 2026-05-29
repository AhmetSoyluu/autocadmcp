from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class CachedEntity:
    """Cached metadata for a single drawing entity."""
    handle: str
    entity_type: str
    layer: str
    color: int = 256  # BYLAYER
    linetype: str = "BYLAYER"
    properties: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class DrawingCache:
    """In-memory cache for a single drawing's state."""
    drawing_path: str
    last_refreshed: float = 0.0
    entity_count: int = 0
    layer_names: list[str] = field(default_factory=list)
    block_names: list[str] = field(default_factory=list)
    text_style_names: list[str] = field(default_factory=list)
    dimension_style_names: list[str] = field(default_factory=list)
    linetype_names: list[str] = field(default_factory=list)
    xref_names: list[str] = field(default_factory=list)
    entities: dict[str, CachedEntity] = field(default_factory=dict)
    extents: dict[str, float] = field(default_factory=dict)
    variables: dict[str, Any] = field(default_factory=dict)


class DrawingStateCache:
    """Per-drawing in-memory cache for entity metadata and drawing state.

    This avoids redundant round-trips to AutoCAD for information that
    doesn't change between tool calls (layers, blocks, styles, etc.).
    Cache entries expire after a configurable TTL.
    """

    DEFAULT_TTL_SECONDS = 30.0

    def __init__(self, ttl_seconds: float = DEFAULT_TTL_SECONDS) -> None:
        self._caches: dict[str, DrawingCache] = {}
        self._ttl = ttl_seconds

    def get(self, drawing_path: str) -> DrawingCache | None:
        """Return cached state if still valid, else None."""
        cache = self._caches.get(drawing_path)
        if cache is None:
            return None
        if time.time() - cache.last_refreshed > self._ttl:
            return None  # expired
        return cache

    def put(self, drawing_path: str, cache: DrawingCache) -> None:
        """Store/update cache entry."""
        cache.last_refreshed = time.time()
        self._caches[drawing_path] = cache

    def invalidate(self, drawing_path: str) -> None:
        """Remove cache for a specific drawing (after a mutation)."""
        self._caches.pop(drawing_path, None)

    def invalidate_all(self) -> None:
        """Clear all caches."""
        self._caches.clear()

    def is_stale(self, drawing_path: str) -> bool:
        cache = self._caches.get(drawing_path)
        if cache is None:
            return True
        return time.time() - cache.last_refreshed > self._ttl

    def update_entities(self, drawing_path: str, entities: dict[str, CachedEntity]) -> None:
        """Merge new entity data into an existing cache."""
        cache = self._caches.get(drawing_path)
        if cache is None:
            cache = DrawingCache(drawing_path=drawing_path)
            self._caches[drawing_path] = cache
        cache.entities.update(entities)
        cache.entity_count = len(cache.entities)
        cache.last_refreshed = time.time()

    def update_layers(self, drawing_path: str, layers: list[str]) -> None:
        cache = self._caches.get(drawing_path)
        if cache is None:
            cache = DrawingCache(drawing_path=drawing_path)
            self._caches[drawing_path] = cache
        cache.layer_names = layers
        cache.last_refreshed = time.time()

    def update_blocks(self, drawing_path: str, blocks: list[str]) -> None:
        cache = self._caches.get(drawing_path)
        if cache is None:
            cache = DrawingCache(drawing_path=drawing_path)
            self._caches[drawing_path] = cache
        cache.block_names = blocks
        cache.last_refreshed = time.time()

    def get_stats(self) -> dict[str, Any]:
        """Return cache statistics."""
        now = time.time()
        entries = []
        for path, cache in self._caches.items():
            age = now - cache.last_refreshed
            entries.append({
                "drawing": path,
                "entity_count": cache.entity_count,
                "layers": len(cache.layer_names),
                "blocks": len(cache.block_names),
                "age_seconds": round(age, 1),
                "stale": age > self._ttl,
            })
        return {
            "total_cached_drawings": len(self._caches),
            "ttl_seconds": self._ttl,
            "entries": entries,
        }

    def build_refresh_lisp(self) -> str:
        """Generate LISP to refresh the cache with drawing state."""
        return (
            '(progn'
            # Layers
            ' (vlax-for layer (vla-get-layers (vla-get-activedocument (vlax-get-acad-object)))'
            ' (princ (strcat "MCP_CACHE_LAYER:" (vla-get-name layer)'
            ' ",color=" (itoa (vla-get-color layer))'
            ' ",frozen=" (if (= (vla-get-freeze layer) :vlax-true) "Y" "N")'
            ' ",locked=" (if (= (vla-get-lock layer) :vlax-true) "Y" "N")'
            ' ",on=" (if (= (vla-get-layeron layer) :vlax-true) "Y" "N") "\\n")))'
            # Blocks
            ' (vlax-for blk (vla-get-blocks (vla-get-activedocument (vlax-get-acad-object)))'
            ' (if (and (= (vla-get-isxref blk) :vlax-false) (= (vla-get-islayout blk) :vlax-false))'
            ' (princ (strcat "MCP_CACHE_BLOCK:" (vla-get-name blk) "\\n"))))'
            # Text styles
            ' (vlax-for ts (vla-get-textstyles (vla-get-activedocument (vlax-get-acad-object)))'
            ' (princ (strcat "MCP_CACHE_TEXTSTYLE:" (vla-get-name ts) "\\n")))'
            # Linetypes
            ' (vlax-for lt (vla-get-linetypes (vla-get-activedocument (vlax-get-acad-object)))'
            ' (princ (strcat "MCP_CACHE_LINETYPE:" (vla-get-name lt) "\\n")))'
            # System variables
            ' (princ (strcat "MCP_CACHE_VAR:LUNITS=" (itoa (getvar "LUNITS")) "\\n"))'
            ' (princ (strcat "MCP_CACHE_VAR:LUPREC=" (itoa (getvar "LUPREC")) "\\n"))'
            ' (princ (strcat "MCP_CACHE_VAR:INSUNITS=" (itoa (getvar "INSUNITS")) "\\n"))'
            ' (princ (strcat "MCP_CACHE_VAR:DIMSTYLE=" (getvar "DIMSTYLE") "\\n"))'
            ' (princ (strcat "MCP_CACHE_VAR:TEXTSTYLE=" (getvar "TEXTSTYLE") "\\n"))'
            ' (princ (strcat "MCP_CACHE_VAR:CLAYER=" (getvar "CLAYER") "\\n"))'
            # Extents
            ' (setq ext_min (getvar "EXTMIN") ext_max (getvar "EXTMAX"))'
            ' (princ (strcat "MCP_CACHE_EXTENTS:"'
            ' (rtos (car ext_min) 2 4) "," (rtos (cadr ext_min) 2 4) ","'
            ' (rtos (car ext_max) 2 4) "," (rtos (cadr ext_max) 2 4) "\\n"))'
            # Entity count
            ' (setq ss (ssget "X")) (setq ecnt (if ss (sslength ss) 0))'
            ' (princ (strcat "MCP_CACHE_ENTITYCOUNT:" (itoa ecnt) "\\n"))'
            ' (princ))'
        )

    def parse_refresh_output(self, drawing_path: str, stdout: str) -> DrawingCache:
        """Parse the output of build_refresh_lisp and create a DrawingCache."""
        cache = DrawingCache(drawing_path=drawing_path)
        layers: list[str] = []
        blocks: list[str] = []
        text_styles: list[str] = []
        linetypes: list[str] = []
        variables: dict[str, Any] = {}

        for line in stdout.splitlines():
            line = line.strip()
            if line.startswith("MCP_CACHE_LAYER:"):
                parts = line.removeprefix("MCP_CACHE_LAYER:").split(",")
                layer_name = parts[0] if parts else ""
                if layer_name:
                    layers.append(layer_name)
            elif line.startswith("MCP_CACHE_BLOCK:"):
                name = line.removeprefix("MCP_CACHE_BLOCK:").strip()
                if name:
                    blocks.append(name)
            elif line.startswith("MCP_CACHE_TEXTSTYLE:"):
                name = line.removeprefix("MCP_CACHE_TEXTSTYLE:").strip()
                if name:
                    text_styles.append(name)
            elif line.startswith("MCP_CACHE_LINETYPE:"):
                name = line.removeprefix("MCP_CACHE_LINETYPE:").strip()
                if name:
                    linetypes.append(name)
            elif line.startswith("MCP_CACHE_VAR:"):
                kv = line.removeprefix("MCP_CACHE_VAR:")
                k, _, v = kv.partition("=")
                if k:
                    variables[k.strip()] = v.strip()
            elif line.startswith("MCP_CACHE_EXTENTS:"):
                coords = line.removeprefix("MCP_CACHE_EXTENTS:").split(",")
                if len(coords) >= 4:
                    cache.extents = {
                        "min_x": float(coords[0]),
                        "min_y": float(coords[1]),
                        "max_x": float(coords[2]),
                        "max_y": float(coords[3]),
                    }
            elif line.startswith("MCP_CACHE_ENTITYCOUNT:"):
                try:
                    cache.entity_count = int(line.removeprefix("MCP_CACHE_ENTITYCOUNT:").strip())
                except ValueError:
                    pass

        cache.layer_names = layers
        cache.block_names = blocks
        cache.text_style_names = text_styles
        cache.linetype_names = linetypes
        cache.variables = variables
        cache.last_refreshed = time.time()
        self._caches[drawing_path] = cache
        return cache
