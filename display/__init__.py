"""Display helper modules for Learn2Slither."""

from .info import RenderInfo, SessionStats
from .settings import DisplaySettings
from .layout import ViewerLayout
from .theme import DisplayTheme, THEMES, DEFAULT_THEME_KEY, get_theme, list_themes
from .fonts import FontSet, load_fonts
from .hud import draw_hud, draw_legend
from .grid import draw_grid
from .overlays import draw_pause_overlay, draw_game_over_overlay
from .panel import ConfigPanel, PanelFlags

__all__ = [
    "RenderInfo",
    "SessionStats",
    "DisplaySettings",
    "ViewerLayout",
    "DisplayTheme",
    "THEMES",
    "DEFAULT_THEME_KEY",
    "get_theme",
    "list_themes",
    "FontSet",
    "load_fonts",
    "draw_hud",
    "draw_legend",
    "draw_grid",
    "draw_pause_overlay",
    "draw_game_over_overlay",
    "ConfigPanel",
    "PanelFlags",
]
