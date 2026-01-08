"""Color palettes and theme helpers for the viewer."""

from __future__ import annotations

from dataclasses import dataclass

Color = tuple[int, int, int]


@dataclass(frozen=True)
class DisplayTheme:
    name: str
    background: Color
    grid_background: Color
    grid_border: Color
    grid_line: Color
    hud_background: Color
    text: Color
    text_dim: Color
    apple_green: Color
    apple_red: Color
    snake_head: Color
    snake_head_highlight: Color
    snake_body: Color
    wall: Color
    highlight: Color


THEMES: dict[str, DisplayTheme] = {
    "deep-space": DisplayTheme(
        name="Deep Space",
        background=(28, 30, 38),
        grid_background=(20, 22, 28),
        grid_border=(120, 120, 130),
        grid_line=(50, 54, 65),
        hud_background=(18, 20, 26),
        text=(220, 222, 230),
        text_dim=(140, 142, 150),
        apple_green=(80, 220, 100),
        apple_red=(240, 80, 80),
        snake_head=(100, 180, 255),
        snake_head_highlight=(150, 220, 255),
        snake_body=(60, 130, 220),
        wall=(120, 120, 130),
        highlight=(255, 220, 80),
    ),
    "neon-grid": DisplayTheme(
        name="Neon Grid",
        background=(8, 12, 24),
        grid_background=(5, 8, 16),
        grid_border=(90, 220, 190),
        grid_line=(40, 120, 110),
        hud_background=(12, 18, 32),
        text=(200, 255, 245),
        text_dim=(110, 170, 160),
        apple_green=(120, 255, 160),
        apple_red=(255, 130, 150),
        snake_head=(120, 200, 255),
        snake_head_highlight=(200, 255, 255),
        snake_body=(60, 200, 190),
        wall=(90, 220, 190),
        highlight=(255, 210, 120),
    ),
}

DEFAULT_THEME_KEY = "deep-space"


def get_theme(key: str) -> DisplayTheme:
    return THEMES.get(key, THEMES[DEFAULT_THEME_KEY])


def list_themes() -> list[str]:
    return list(THEMES.keys())


__all__ = [
    "Color",
    "DisplayTheme",
    "THEMES",
    "DEFAULT_THEME_KEY",
    "get_theme",
    "list_themes",
]
