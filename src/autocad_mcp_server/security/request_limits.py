from dataclasses import dataclass


@dataclass(frozen=True)
class RequestLimits:
    max_entity_results: int
    max_text_results: int
    max_lisp_chars: int
    max_lisp_depth: int
