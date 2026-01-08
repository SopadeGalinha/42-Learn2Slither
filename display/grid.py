"""Grid rendering helpers for the snake board."""

from __future__ import annotations

try:  # pragma: no cover - optional dependency
    import pygame
except ImportError:  # pragma: no cover
    pygame = None  # type: ignore

from slither.core._types import BoardCell

from .theme import DisplayTheme
from .layout import ViewerLayout
from .settings import DisplaySettings


def draw_grid(
    screen: "pygame.Surface",
    board,
    theme: DisplayTheme,
    layout: ViewerLayout,
    settings: DisplaySettings,
    visible_cells: set[tuple[int, int]] | None = None,
) -> None:
    size = board.size
    base_x = layout.grid_padding
    base_y = layout.grid_padding

    grid_rect = pygame.Rect(
        base_x,
        base_y,
        layout.grid_width(size),
        layout.grid_height(size),
    )
    pygame.draw.rect(screen, theme.grid_background, grid_rect)
    pygame.draw.rect(screen, theme.grid_border, grid_rect, width=2)

    hidden_bg = tuple(max(0, c - 25) for c in theme.grid_background)

    for y in range(size):
        for x in range(size):
            cell = board.get_cell(x, y)
            rect = pygame.Rect(
                base_x + x * layout.cell_size,
                base_y + y * layout.cell_size,
                layout.cell_size,
                layout.cell_size,
            )

            is_visible = visible_cells is None or (x, y) in visible_cells
            cell_bg = theme.grid_background if is_visible else hidden_bg
            pygame.draw.rect(screen, cell_bg, rect)

            if settings.show_grid_lines:
                pygame.draw.rect(screen, theme.grid_line, rect, width=1)

            color = None
            border_radius = 4

            if cell == BoardCell.GREEN_APPLE:
                color = theme.apple_green
                border_radius = layout.cell_size // 2
            elif cell == BoardCell.RED_APPLE:
                color = theme.apple_red
                border_radius = layout.cell_size // 2
            elif cell == BoardCell.SNAKE_HEAD:
                color = theme.snake_head
                border_radius = 6
            elif cell == BoardCell.SNAKE_BODY:
                color = theme.snake_body
            elif cell == BoardCell.WALL:
                color = theme.wall
                border_radius = 2

            if not color:
                continue

            inner = rect.inflate(-6, -6)
            pygame.draw.rect(screen, color, inner, border_radius=border_radius)

            if cell == BoardCell.SNAKE_HEAD and is_visible:
                highlight_rect = inner.inflate(-8, -8)
                highlight_rect.topleft = (inner.left + 4, inner.top + 4)
                pygame.draw.rect(
                    screen,
                    theme.snake_head_highlight,
                    highlight_rect,
                    border_radius=3,
                )


__all__ = ["draw_grid"]
