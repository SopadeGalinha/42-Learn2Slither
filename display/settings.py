"""Runtime display settings for the viewer."""

from __future__ import annotations

from dataclasses import dataclass

from .theme import DEFAULT_THEME_KEY

CELL_MIN = 24
CELL_MAX = 56
LEGEND_MIN = 140
LEGEND_MAX = 260
LEGEND_STEP = 10
CELL_STEP = 4


@dataclass
class DisplaySettings:
    theme_key: str = DEFAULT_THEME_KEY
    cell_size: int = 32
    grid_padding: int = 8
    hud_height: int = 60
    legend_width: int = 180
    show_hud: bool = True
    show_legend: bool = True
    show_grid_lines: bool = True
    agent_view: bool = False

    def adjust_cell_size(self, delta: int) -> bool:
        new_value = max(CELL_MIN, min(CELL_MAX, self.cell_size + delta))
        if new_value == self.cell_size:
            return False
        self.cell_size = new_value
        return True

    def adjust_legend_width(self, delta: int) -> bool:
        new_value = max(LEGEND_MIN, min(LEGEND_MAX, self.legend_width + delta))
        if new_value == self.legend_width:
            return False
        self.legend_width = new_value
        return True


__all__ = ["DisplaySettings"]
