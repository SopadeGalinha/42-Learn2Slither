"""HUD and sidebar rendering for the snake viewer."""

from __future__ import annotations

try:  # pragma: no cover - optional dependency
    import pygame
except ImportError:  # pragma: no cover - optional dependency
    pygame = None  # type: ignore

from .info import RenderInfo, SessionStats
from .theme import DisplayTheme
from .fonts import FontSet
from .layout import ViewerLayout


def _blit_text(
    screen: "pygame.Surface",
    font: "pygame.font.Font",
    text: str,
    color: tuple[int, int, int],
    pos: tuple[int, int],
) -> None:
    surf = font.render(text, True, color)
    screen.blit(surf, pos)


def draw_hud(
    screen: "pygame.Surface",
    fonts: FontSet,
    theme: DisplayTheme,
    layout: ViewerLayout,
    info: RenderInfo,
    board_size: int,
) -> None:
    hud_rect = pygame.Rect(
        0,
        screen.get_height() - layout.hud_height,
        screen.get_width(),
        layout.hud_height,
    )
    pygame.draw.rect(screen, theme.hud_background, hud_rect)

    status = "GAME OVER" if info.done else "PLAYING"
    status_color = theme.apple_red if info.done else theme.apple_green
    col1 = [
        (f"Episode: {info.episode}", theme.text),
        (f"Step: {info.step}", theme.text),
    ]
    col2 = [
        (
            f"Length: {info.length}",
            theme.highlight if info.length >= 10 else theme.text,
        ),
        (f"Score: {info.score}", theme.text),
    ]
    col3 = [
        (
            f"Reward: {info.reward:+.2f}",
            (
                theme.apple_green
                if info.reward > 0
                else theme.apple_red if info.reward < -1 else theme.text_dim
            ),
        ),
        (f"Status: {status}", status_color),
    ]

    columns = [col1, col2, col3]
    col_width = screen.get_width() // len(columns)
    y_start = hud_rect.y + 10
    for i, col in enumerate(columns):
        x = 12 + i * col_width
        y = y_start
        for text, color in col:
            _blit_text(screen, fonts.hud, text, color, (x, y))
            y += 20


def draw_legend(
    screen: "pygame.Surface",
    fonts: FontSet,
    theme: DisplayTheme,
    layout: ViewerLayout,
    stats: SessionStats,
    board_size: int,
    manual_mode: bool,
    step_mode: bool,
) -> None:
    grid_width = layout.grid_width(board_size)
    x = layout.grid_padding * 2 + grid_width + 10
    y = layout.grid_padding

    _blit_text(screen, fonts.title, "Learn2Slither", theme.text, (x, y))
    y += 30
    _blit_text(screen,
               fonts.small, "Reinforcement Learning", theme.text_dim, (x, y))
    y += 25

    legend_items = [
        (theme.apple_green, "Green Apple (+)"),
        (theme.apple_red, "Red Apple (-)"),
        (theme.snake_head, "Snake Head"),
        (theme.snake_body, "Snake Body"),
        (theme.wall, "Wall"),
    ]

    for color, label in legend_items:
        rect = pygame.Rect(x, y, 14, 14)
        pygame.draw.rect(screen, color, rect, border_radius=3)
        _blit_text(screen, fonts.small, label, theme.text, (x + 20, y))
        y += 20

    y += 6
    _blit_text(screen, fonts.small,
               "Goal: Length >= 10", theme.highlight, (x, y))
    y += 20
    pygame.draw.line(screen, theme.grid_line, (x, y), (x + 160, y), 1)
    y += 6
    _blit_text(screen, fonts.small, "This Episode", theme.text, (x, y))
    y += 16

    episode_items = [
        (f"Greens: {stats.episode_greens}", theme.apple_green),
        (f"Reds: {stats.episode_reds}", theme.apple_red),
    ]
    for text, color in episode_items:
        _blit_text(screen, fonts.small, text, color, (x, y))
        y += 14

    y += 8
    pygame.draw.line(screen, theme.grid_line, (x, y), (x + 160, y), 1)
    y += 6
    _blit_text(screen, fonts.small, "Session Best", theme.text, (x, y))
    y += 16

    session_items = [
        f"Max Len: {stats.max_length}",
        f"Wins: {stats.wins}/{stats.episodes_played}",
    ]
    for text in session_items:
        _blit_text(screen, fonts.small, text, theme.text_dim, (x, y))
        y += 14

    y += 8
    if manual_mode:
        controls = "[Arrows] Move"
    elif step_mode:
        controls = "[Space/Enter] Step"
    else:
        controls = "[Space] Pause"
    _blit_text(screen, fonts.small, controls, theme.text_dim, (x, y))
    y += 14
    _blit_text(screen, fonts.small, "[Q/Esc] Quit", theme.text_dim, (x, y))
    y += 14
    _blit_text(screen, fonts.small,
               "[C] Display Panel", theme.text_dim, (x, y))


__all__ = ["draw_hud", "draw_legend"]
