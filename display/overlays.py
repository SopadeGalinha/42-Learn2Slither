"""Overlay rendering helpers (pause, game over)."""

from __future__ import annotations

try:  # pragma: no cover - optional dependency
    import pygame
except ImportError:  # pragma: no cover
    pygame = None  # type: ignore

from .fonts import FontSet
from .theme import DisplayTheme
from .info import RenderInfo, SessionStats


def draw_pause_overlay(
    screen: "pygame.Surface",
    fonts: FontSet,
    theme: DisplayTheme,
) -> None:
    overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 120))
    screen.blit(overlay, (0, 0))

    center_x = screen.get_width() // 2
    center_y = screen.get_height() // 2 - 20

    pause_surf = fonts.splash_title.render("PAUSED", True, theme.highlight)
    screen.blit(pause_surf, (center_x - pause_surf.get_width() // 2, center_y))

    prompt_surf = fonts.splash.render("[Press SPACE to start]", True, theme.text)
    screen.blit(
        prompt_surf,
        (
            center_x - prompt_surf.get_width() // 2,
            center_y + 50,
        ),
    )


def draw_game_over_overlay(
    screen: "pygame.Surface",
    fonts: FontSet,
    theme: DisplayTheme,
    stats: SessionStats,
    info: RenderInfo,
) -> None:
    overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 160))
    screen.blit(overlay, (0, 0))

    center_x = screen.get_width() // 2
    y = screen.get_height() // 2 - 100

    is_win = info.length >= 10
    title = "VICTORY!" if is_win else "GAME OVER"
    title_color = theme.apple_green if is_win else theme.apple_red
    title_surf = fonts.splash_title.render(title, True, title_color)
    screen.blit(title_surf, (center_x - title_surf.get_width() // 2, y))

    y += 50
    box_width = 200
    box_height = 130
    box_x = center_x - box_width // 2
    box_rect = pygame.Rect(box_x, y, box_width, box_height)
    pygame.draw.rect(screen, theme.hud_background, box_rect, border_radius=8)
    pygame.draw.rect(screen, theme.grid_line, box_rect, width=2, border_radius=8)

    y += 15
    stats_rows = [
        ("Episode", str(info.episode)),
        ("Steps", str(info.step)),
        ("Length", str(info.length)),
        ("Score", str(info.score)),
        ("Best Length", str(stats.max_length)),
    ]

    for label, value in stats_rows:
        label_surf = fonts.small.render(f"{label}:", True, theme.text_dim)
        value_color = theme.highlight if label == "Best Length" else theme.text
        value_surf = fonts.small.render(value, True, value_color)
        screen.blit(label_surf, (box_x + 15, y))
        screen.blit(value_surf, (box_x + box_width - 15 - value_surf.get_width(), y))
        y += 20

    y = box_rect.bottom + 20
    prompt = "[SPACE] Continue  [Q] Quit"
    prompt_surf = fonts.splash_small.render(prompt, True, theme.text_dim)
    screen.blit(prompt_surf, (center_x - prompt_surf.get_width() // 2, y))


__all__ = ["draw_pause_overlay", "draw_game_over_overlay"]
