from __future__ import annotations

import math
import os
from typing import TYPE_CHECKING, Optional
from dataclasses import dataclass

# Hide pygame welcome message
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

try:
    import pygame
except ImportError as exc:  # pragma: no cover - optional dependency
    raise ImportError(
        "Pygame is required for the viewer. Install with `pip install pygame`."
    ) from exc

from ._types import BoardCell

if TYPE_CHECKING:
    from .board import GameBoard

# Type alias for RGB color tuples
Color = tuple[int, int, int]

# UI Colors
COLOR_BG: Color = (28, 30, 38)  # Dark background
COLOR_GRID_BG: Color = (20, 22, 28)  # Slightly lighter grid background
COLOR_GRID_LINE: Color = (50, 54, 65)  # Subtle grid lines
COLOR_HUD_BG: Color = (18, 20, 26)  # Dark HUD background
COLOR_TEXT: Color = (220, 222, 230)  # Light text
COLOR_TEXT_DIM: Color = (140, 142, 150)  # Dimmer text
COLOR_APPLE_GREEN: Color = (80, 220, 100)  # Bright green apple
COLOR_APPLE_RED: Color = (240, 80, 80)  # Bright red apple
COLOR_SNAKE_HEAD: Color = (100, 180, 255)  # Blue snake head
COLOR_SNAKE_HEAD_HIGHLIGHT: Color = (150, 220, 255)  # Highlighted blue snake head
COLOR_SNAKE_BODY: Color = (60, 130, 220)  # Blue snake body
COLOR_WALL: Color = (120, 120, 130)  # Gray walls
COLOR_HIGHLIGHT: Color = (255, 220, 80)  # Highlight color

# Font sizes
FONT_SIZE_HUD = 13
FONT_SIZE_TITLE = 16
FONT_SIZE_SMALL = 11
FONT_SIZE_SPLASH_TITLE = 32
FONT_SIZE_SPLASH = 14
FONT_SIZE_SPLASH_SMALL = 12


@dataclass
class RenderInfo:
    episode: int = 0
    step: int = 0
    reward: float = 0.0
    length: int = 0
    score: int = 0
    done: bool = False
    fps: int = 10


class Viewer:
    """Pygame-based viewer for the snake board."""

    def __init__(
        self,
        cell_size: int = 40,
        grid_padding: int = 8,
        hud_height: int = 60,
        legend_width: int = 180,
        fps: int = 10,
        step_mode: bool = False,
        manual_mode: bool = False,
        manage_events: bool = True,
    ) -> None:
        self.cell_size = cell_size
        self.grid_padding = grid_padding
        self.hud_height = hud_height
        self.legend_width = legend_width
        self.default_fps = fps
        self.step_mode = step_mode
        self.manual_mode = manual_mode
        self.manage_events = manage_events

        pygame.init()
        pygame.display.set_caption("Learn2Slither - Snake Game")
        self.clock = pygame.time.Clock()
        self._screen: Optional[pygame.Surface] = None

        # Colors (use module constants)
        self.bg = COLOR_BG
        self.grid_bg = COLOR_GRID_BG
        self.grid_line = COLOR_GRID_LINE
        self.hud_bg = COLOR_HUD_BG
        self.text = COLOR_TEXT
        self.text_dim = COLOR_TEXT_DIM
        self.apple_green = COLOR_APPLE_GREEN
        self.apple_red = COLOR_APPLE_RED
        self.snake_head = COLOR_SNAKE_HEAD
        self.snake_body = COLOR_SNAKE_BODY
        self.wall = COLOR_WALL
        self.highlight = COLOR_HIGHLIGHT

        # Fonts
        self.font = pygame.font.SysFont("monospace", FONT_SIZE_HUD)
        self.font_title = pygame.font.SysFont("monospace", FONT_SIZE_TITLE, bold=True)
        self.font_small = pygame.font.SysFont("monospace", FONT_SIZE_SMALL)
        self.font_splash_title = pygame.font.SysFont(
            "monospace", FONT_SIZE_SPLASH_TITLE, bold=True
        )
        self.font_splash = pygame.font.SysFont("monospace", FONT_SIZE_SPLASH)
        self.font_splash_small = pygame.font.SysFont(
            "monospace", FONT_SIZE_SPLASH_SMALL
        )

        self._splash_shown = False
        self._paused = True  # Start paused after splash

    @property
    def screen(self) -> pygame.Surface:
        """Return the screen surface, raising if not initialized."""
        if self._screen is None:
            raise RuntimeError("Screen not initialized. Call _ensure_screen() first.")
        return self._screen

    def _ensure_screen(self, board_size: int) -> None:
        if self._screen is not None:
            return
        grid_size = board_size * self.cell_size
        width = grid_size + self.grid_padding * 3 + self.legend_width
        height = grid_size + self.grid_padding * 2 + self.hud_height
        self._screen = pygame.display.set_mode((width, height))

    def show_splash(self, board_size: int = 10) -> bool:
        """Show splash screen. Returns False if user quit, True if ready to start."""
        self._ensure_screen(board_size)

        width = self.screen.get_width()
        height = self.screen.get_height()
        center_x = width // 2
        frame = 0

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_q, pygame.K_ESCAPE):
                        return False
                    if event.key == pygame.K_RETURN:  # Only ENTER, SPACE is for unpause
                        self._splash_shown = True
                        return True

            self.screen.fill(self.bg)

            # Pulsing title effect
            pulse = abs(math.sin(frame * 0.05)) * 0.3 + 0.7
            title_color = (
                int(self.snake_head[0] * pulse),
                int(self.snake_head[1] * pulse),
                int(self.snake_head[2] * pulse),
            )

            # Snake ASCII art
            snake_art = [
                "    ___     ",
                "   /o o\\    ",
                "  ( === )   ",
                "   \\   /    ",
                "    | |~~~  ",
            ]

            y = height // 12

            for line in snake_art:
                surf = self.font_splash.render(line, True, self.snake_head)
                self.screen.blit(surf, (center_x - surf.get_width() // 2, y))
                y += 18

            # Title
            y += 20
            title_surf = self.font_splash_title.render(
                "LEARN2SLITHER", True, title_color
            )
            self.screen.blit(title_surf, (center_x - title_surf.get_width() // 2, y))

            # Subtitle
            y += 45
            sub_surf = self.font_splash.render(
                "Reinforcement Learning Snake AI", True, self.text_dim
            )
            self.screen.blit(sub_surf, (center_x - sub_surf.get_width() // 2, y))

            # Separator
            y += 35
            pygame.draw.line(
                self.screen, self.grid_line, (center_x - 80, y), (center_x + 80, y), 2
            )

            # Features
            y += 25
            features = [
                ("Q-Learning Algorithm", self.apple_green),
                ("Tabular State Space", self.snake_body),
                ("42 School Project", self.highlight),
            ]
            for text, color in features:
                # Bullet point
                pygame.draw.circle(self.screen, color, (center_x - 90, y + 7), 4)
                feat_surf = self.font_splash_small.render(text, True, self.text)
                self.screen.blit(feat_surf, (center_x - 75, y))
                y += 22

            # Blinking "Press ENTER" text
            y = height - 60
            if (frame // 30) % 2 == 0:
                prompt_surf = self.font_splash.render(
                    "[Press ENTER to start]", True, self.highlight
                )
                self.screen.blit(
                    prompt_surf, (center_x - prompt_surf.get_width() // 2, y)
                )

            # Footer
            y = height - 25
            footer_surf = self.font_splash_small.render(
                "Q/Esc to quit", True, self.text_dim
            )
            self.screen.blit(footer_surf, (center_x - footer_surf.get_width() // 2, y))

            pygame.display.flip()
            self.clock.tick(60)
            frame += 1

        return True

    def _draw_hud(self, info: RenderInfo, board_size: int) -> None:
        grid_width = board_size * self.cell_size + self.grid_padding * 2
        hud_rect = pygame.Rect(
            0,
            self.screen.get_height() - self.hud_height,
            self.screen.get_width(),
            self.hud_height,
        )
        pygame.draw.rect(self.screen, self.hud_bg, hud_rect)

        # Status line
        status = "GAME OVER" if info.done else "PLAYING"
        status_color = self.apple_red if info.done else self.apple_green
        col1 = [
            (f"Episode: {info.episode}", self.text),
            (f"Step: {info.step}", self.text),
        ]
        col2 = [
            (
                f"Length: {info.length}",
                self.highlight if info.length >= 10 else self.text,
            ),
            (f"Score: {info.score}", self.text),
        ]
        col3 = [
            (
                f"Reward: {info.reward:+.2f}",
                (
                    self.apple_green
                    if info.reward > 0
                    else self.apple_red if info.reward < -1 else self.text_dim
                ),
            ),
            (f"Status: {status}", status_color),
        ]

        col_width = grid_width // 3
        y_start = hud_rect.y + 10
        for i, col in enumerate([col1, col2, col3]):
            x = 12 + i * col_width
            y = y_start
            for text, color in col:
                surf = self.font.render(text, True, color)
                self.screen.blit(surf, (x, y))
                y += 20

    def _draw_legend(self, board_size: int) -> None:
        """Draw color legend on the right side."""
        grid_width = board_size * self.cell_size
        x = self.grid_padding * 2 + grid_width + 10
        y = self.grid_padding

        # Title
        title_surf = self.font_title.render("Learn2Slither", True, self.text)
        self.screen.blit(title_surf, (x, y))
        y += 30

        # Subtitle
        sub_surf = self.font_small.render("Reinforcement Learning", True, self.text_dim)
        self.screen.blit(sub_surf, (x, y))
        y += 35

        # Legend items
        legend_items = [
            (self.apple_green, "Green Apple (+)"),
            (self.apple_red, "Red Apple (-)"),
            (self.snake_head, "Snake Head"),
            (self.snake_body, "Snake Body"),
            (self.wall, "Wall"),
        ]

        for color, label in legend_items:
            # Color square
            rect = pygame.Rect(x, y, 16, 16)
            pygame.draw.rect(self.screen, color, rect, border_radius=3)
            # Label
            label_surf = self.font_small.render(label, True, self.text)
            self.screen.blit(label_surf, (x + 24, y + 1))
            y += 24

        # Goal section
        y += 15
        goal_surf = self.font_small.render("Goal: Length >= 10", True, self.highlight)
        self.screen.blit(goal_surf, (x, y))

        # Controls section
        y += 30
        if self.step_mode:
            ctrl_surf = self.font_small.render(
                "[Space/Enter] Step", True, self.text_dim
            )
            self.screen.blit(ctrl_surf, (x, y))
            y += 18
        quit_surf = self.font_small.render("[Q/Esc] Quit", True, self.text_dim)
        self.screen.blit(quit_surf, (x, y))

    def _draw_grid(self, board: GameBoard, info: RenderInfo) -> None:
        size = board.size
        base_x = self.grid_padding
        base_y = self.grid_padding

        # Grid background with border
        grid_rect = pygame.Rect(
            base_x, base_y, size * self.cell_size, size * self.cell_size
        )
        pygame.draw.rect(self.screen, self.grid_bg, grid_rect)
        pygame.draw.rect(self.screen, self.wall, grid_rect, width=2)

        for y in range(size):
            for x in range(size):
                cell = board.get_cell(x, y)
                rect = pygame.Rect(
                    base_x + x * self.cell_size,
                    base_y + y * self.cell_size,
                    self.cell_size,
                    self.cell_size,
                )
                color = None
                border_radius = 4

                if cell == BoardCell.GREEN_APPLE:
                    color = self.apple_green
                    border_radius = self.cell_size // 2  # Circular apple
                elif cell == BoardCell.RED_APPLE:
                    color = self.apple_red
                    border_radius = self.cell_size // 2  # Circular apple
                elif cell == BoardCell.SNAKE_HEAD:
                    color = self.snake_head
                    border_radius = 6
                elif cell == BoardCell.SNAKE_BODY:
                    color = self.snake_body
                elif cell == BoardCell.WALL:
                    color = self.wall

                # Grid lines (subtle)
                pygame.draw.rect(self.screen, self.grid_line, rect, width=1)

                if color:
                    inner = rect.inflate(-6, -6)
                    pygame.draw.rect(
                        self.screen, color, inner, border_radius=border_radius
                    )

                    # Add highlight to snake head
                    if cell == BoardCell.SNAKE_HEAD:
                        highlight_rect = inner.inflate(-8, -8)
                        highlight_rect.topleft = (inner.left + 4, inner.top + 4)
                        pygame.draw.rect(
                            self.screen,
                            COLOR_SNAKE_HEAD_HIGHLIGHT,
                            highlight_rect,
                            border_radius=3,
                        )

    def _handle_events_step(self) -> tuple[bool, bool]:
        """Handle events in step mode; return (should_advance, should_quit)."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False, True
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_q, pygame.K_ESCAPE):
                    return False, True
                if event.key in (pygame.K_SPACE, pygame.K_RETURN, pygame.K_n):
                    return True, False
        return False, False

    def get_manual_action(self) -> int:
        """Wait for arrow key input and return action index. Returns -1 if quit."""
        # Action mapping: 0=UP, 1=LEFT, 2=DOWN, 3=RIGHT
        key_to_action = {
            pygame.K_UP: 0,
            pygame.K_LEFT: 1,
            pygame.K_DOWN: 2,
            pygame.K_RIGHT: 3,
            pygame.K_w: 0,
            pygame.K_a: 1,
            pygame.K_s: 2,
            pygame.K_d: 3,
        }
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return -1
                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_q, pygame.K_ESCAPE):
                        return -1
                    if event.key in key_to_action:
                        return key_to_action[event.key]
            self.clock.tick(30)

    def _handle_events_run(self) -> bool:
        """Handle events in continuous mode; return False to quit."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN and event.key in (
                pygame.K_q,
                pygame.K_ESCAPE,
            ):
                return False
        return True

    def render(self, board: GameBoard, info: Optional[RenderInfo] = None) -> bool:
        """Render the current board. Return False if user requested quit."""
        if info is None:
            info = RenderInfo()
        fps = info.fps or self.default_fps

        self._ensure_screen(board.size)

        # Reset splash flag
        if self._splash_shown:
            self._splash_shown = False

        # Draw current state first (so user sees step 0 when paused)
        self.screen.fill(self.bg)
        self._draw_grid(board, info)
        self._draw_legend(board.size)
        self._draw_hud(info, board.size)

        # Show pause overlay if paused
        if self._paused:
            self._draw_pause_overlay()

        pygame.display.flip()

        # Handle pause state - wait for Space to unpause
        if self._paused and self.manage_events:
            if not self._wait_for_unpause():
                return False
            self._paused = False
            # Redraw without pause overlay
            self.screen.fill(self.bg)
            self._draw_grid(board, info)
            self._draw_legend(board.size)
            self._draw_hud(info, board.size)
            pygame.display.flip()

        self.clock.tick(fps)

        # Handle normal events (after first frame)
        if self.manage_events and not self.manual_mode:
            if self.step_mode:
                if not self._wait_for_step():
                    return False
            else:
                if not self._handle_events_run():
                    return False

        return True

    def _draw_pause_overlay(self) -> None:
        """Draw pause overlay on screen."""
        # Semi-transparent overlay
        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 120))
        self.screen.blit(overlay, (0, 0))

        # Pause text
        center_x = self.screen.get_width() // 2
        center_y = self.screen.get_height() // 2 - 20

        pause_surf = self.font_splash_title.render("PAUSED", True, self.highlight)
        self.screen.blit(pause_surf, (center_x - pause_surf.get_width() // 2, center_y))

        prompt_surf = self.font_splash.render("[Press SPACE to start]", True, self.text)
        self.screen.blit(prompt_surf, (center_x - prompt_surf.get_width() // 2, center_y + 50))

    def _wait_for_unpause(self) -> bool:
        """Wait for user to press Space to unpause. Returns False if quit requested."""
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_q, pygame.K_ESCAPE):
                        return False
                    if event.key == pygame.K_SPACE:  # Only SPACE to unpause
                        return True
            self.clock.tick(30)

    def _wait_for_step(self) -> bool:
        """Wait for user to advance in step mode. Returns False if quit requested."""
        while True:
            advance, quit_requested = self._handle_events_step()
            if quit_requested:
                return False
            if advance:
                return True
            self.clock.tick(30)

    def wait_for_close(self) -> None:
        """Block until user closes the window (Q/Esc/close button)."""
        if self._screen is None:
            return
        print("Press Q or Esc to close viewer...")
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_q, pygame.K_ESCAPE):
                        waiting = False
            self.clock.tick(30)

    def close(self) -> None:
        if self._screen is not None:
            pygame.display.quit()
        pygame.quit()

    def __repr__(self) -> str:
        mode = "manual" if self.manual_mode else "step" if self.step_mode else "continuous"
        return (
            f"Viewer(cell_size={self.cell_size}, fps={self.default_fps}, mode={mode})"
        )


__all__ = ["Viewer", "RenderInfo"]
