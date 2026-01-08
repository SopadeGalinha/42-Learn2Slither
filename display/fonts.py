"""Font loading utilities for the viewer."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

try:  # pragma: no cover - optional dependency
    import pygame
except ImportError:  # pragma: no cover - optional dependency
    pygame = None  # type: ignore[misc,assignment]


@dataclass(frozen=True)
class FontSet:
    hud: "pygame.font.Font"
    title: "pygame.font.Font"
    small: "pygame.font.Font"
    splash_title: "pygame.font.Font"
    splash: "pygame.font.Font"
    splash_small: "pygame.font.Font"


def load_fonts() -> FontSet:
    if pygame is None:
        raise RuntimeError("pygame is required to load fonts")
    return FontSet(
        hud=pygame.font.SysFont("monospace", 13),
        title=pygame.font.SysFont("monospace", 16, bold=True),
        small=pygame.font.SysFont("monospace", 11),
        splash_title=pygame.font.SysFont("monospace", 32, bold=True),
        splash=pygame.font.SysFont("monospace", 14),
        splash_small=pygame.font.SysFont("monospace", 12),
    )


__all__ = ["FontSet", "load_fonts"]
