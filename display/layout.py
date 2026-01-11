"""Layout helper dataclasses for the viewer."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ViewerLayout:
    cell_size: int = 32
    grid_padding: int = 8
    hud_height: int = 60
    legend_width: int = 180

    def grid_width(self, board_size: int) -> int:
        return board_size * self.cell_size

    def grid_height(self, board_size: int) -> int:
        return board_size * self.cell_size

    def surface_size(self, board_size: int) -> tuple[int, int]:
        width = self.grid_width(board_size) + \
            self.grid_padding * 3 + self.legend_width
        height = self.grid_height(board_size) + \
            self.grid_padding * 2 + self.hud_height
        return width, height


__all__ = ["ViewerLayout"]
