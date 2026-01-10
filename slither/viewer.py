"""Pygame viewer that composes rendering helpers from the display package."""

from __future__ import annotations

import math
import os
from typing import TYPE_CHECKING, Optional

from display import (
    ConfigPanel,
    DisplaySettings,
    RenderInfo,
    SessionStats,
    ViewerLayout,
    draw_game_over_overlay,
    draw_grid,
    draw_hud,
    draw_legend,
    draw_pause_overlay,
    get_theme,
    load_fonts,
)
from slither.core._types import BoardCell

# Hide pygame welcome message early
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

try:  # pragma: no cover - optional dependency
    import pygame
except ImportError as exc:  # pragma: no cover - optional dependency
    raise ImportError(
        "Pygame is required for the viewer. Install with `pip install pygame`."
    ) from exc

if TYPE_CHECKING:  # pragma: no cover - import for type checking only
    from .board import GameBoard


class Viewer:
    """Render Learn2Slither boards with customizable display settings."""

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
        self.settings = DisplaySettings(
            cell_size=cell_size,
            grid_padding=grid_padding,
            hud_height=hud_height,
            legend_width=legend_width,
        )
        self.layout = ViewerLayout(
            cell_size=self.settings.cell_size,
            grid_padding=self.settings.grid_padding,
            hud_height=self.settings.hud_height,
            legend_width=self.settings.legend_width,
        )
        self.default_fps = fps
        self.step_mode = step_mode
        self.manual_mode = manual_mode
        self.manage_events = manage_events

        pygame.init()
        pygame.display.set_caption("Learn2Slither - Snake Game")
        self.clock = pygame.time.Clock()

        self.fonts = load_fonts()
        self.theme = get_theme(self.settings.theme_key)
        self.panel = ConfigPanel(self.settings)

        self.stats = SessionStats()
        self._last_length = 0
        self._paused = not self.manual_mode
        self._splash_shown = False
        self._screen: Optional[pygame.Surface] = None
        self._board_size: Optional[int] = None
        self._last_board: Optional["GameBoard"] = None
        self._last_info: Optional[RenderInfo] = None

        # Backwards-compatible sizing attributes
        self.cell_size = self.settings.cell_size
        self.grid_padding = self.settings.grid_padding
        self.hud_height = self.settings.hud_height
        self.legend_width = self.settings.legend_width

    # ------------------------------------------------------------------
    def _ensure_screen(self, board_size: int) -> None:
        self._board_size = board_size
        if self._screen is None:
            width, height = self.layout.surface_size(board_size)
            self._screen = pygame.display.set_mode((width, height))

    # ------------------------------------------------------------------
    def _update_layout_from_settings(self) -> None:
        self.layout.cell_size = self.settings.cell_size
        self.layout.grid_padding = self.settings.grid_padding
        self.layout.hud_height = self.settings.hud_height
        self.layout.legend_width = self.settings.legend_width

        self.cell_size = self.settings.cell_size
        self.grid_padding = self.settings.grid_padding
        self.hud_height = self.settings.hud_height
        self.legend_width = self.settings.legend_width

        if self._screen is not None and self._board_size is not None:
            width, height = self.layout.surface_size(self._board_size)
            self._screen = pygame.display.set_mode((width, height))

    # ------------------------------------------------------------------
    def _apply_panel_flags(self) -> None:
        flags = self.panel.consume_flags()
        if flags.theme_changed:
            self.theme = get_theme(self.settings.theme_key)
        if flags.layout_changed:
            self._update_layout_from_settings()

    # ------------------------------------------------------------------
    def _handle_panel_event(self, event) -> bool:
        handled = self.panel.handle_event(event)
        if handled:
            self._apply_panel_flags()
            self._redraw_last_frame()
        return handled

    # ------------------------------------------------------------------
    def _draw_scene(self, board: "GameBoard", info: RenderInfo) -> None:
        screen = self.screen
        theme = self.theme

        screen.fill(theme.background)
        visible_cells = None
        if self.settings.agent_view:
            visible_cells = self._agent_visible_cells(board)

        draw_grid(
            screen,
            board,
            theme,
            self.layout,
            self.settings,
            visible_cells=visible_cells,
        )

        if self.settings.show_legend:
            draw_legend(
                screen,
                self.fonts,
                theme,
                self.layout,
                self.stats,
                board.size,
                self.manual_mode,
                self.step_mode,
            )
        if self.settings.show_hud:
            draw_hud(screen, self.fonts, theme, self.layout, info, board.size)

        if self._paused:
            draw_pause_overlay(screen, self.fonts, theme)
        if info.done:
            draw_game_over_overlay(screen, self.fonts, theme, self.stats, info)

        self.panel.render(screen, self.fonts, theme)
        pygame.display.flip()

        self._last_board = board
        self._last_info = info

    # ------------------------------------------------------------------
    def _redraw_last_frame(self) -> None:
        if self._last_board is None or self._last_info is None:
            return
        self._draw_scene(self._last_board, self._last_info)

    # ------------------------------------------------------------------
    def _agent_visible_cells(
        self, board: "GameBoard"
    ) -> set[tuple[int, int]] | None:
        head = self._find_head(board)
        if head is None:
            return None

        size = board.size
        visible: set[tuple[int, int]] = {head}
        directions = ((0, -1), (-1, 0), (0, 1), (1, 0))

        for dx, dy in directions:
            x, y = head
            while True:
                x += dx
                y += dy
                if x < 0 or x >= size or y < 0 or y >= size:
                    break
                visible.add((x, y))
                cell = board.get_cell(x, y)
                if cell in (
                    BoardCell.WALL,
                    BoardCell.SNAKE_BODY,
                    BoardCell.GREEN_APPLE,
                    BoardCell.RED_APPLE,
                ):
                    break

        return visible

    # ------------------------------------------------------------------
    def _find_head(self, board: "GameBoard") -> tuple[int, int] | None:
        size = board.size
        for y in range(size):
            for x in range(size):
                if board.get_cell(x, y) == BoardCell.SNAKE_HEAD:
                    return (x, y)
        return None

    # ------------------------------------------------------------------
    def show_splash(self, board_size: int = 10) -> bool:
        """Show splash screen and wait for player confirmation."""
        self._ensure_screen(board_size)
        theme = self.theme

        width = self.screen.get_width()
        height = self.screen.get_height()
        center_x = width // 2
        frame = 0

        while True:
            for event in pygame.event.get():
                if self._handle_panel_event(event):
                    continue
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_q, pygame.K_ESCAPE):
                        return False
                    if event.key == pygame.K_RETURN:
                        self._splash_shown = True
                        return True

            self.screen.fill(theme.background)

            pulse = abs(math.sin(frame * 0.05)) * 0.3 + 0.7
            title_color = (
                int(theme.snake_head[0] * pulse),
                int(theme.snake_head[1] * pulse),
                int(theme.snake_head[2] * pulse),
            )

            snake_art = [
                "    ___     ",
                "   /o o\\    ",
                "  ( === )   ",
                "   \\   /    ",
                "    | |~~~  ",
            ]

            y = height // 12
            for line in snake_art:
                surf = self.fonts.splash.render(line, True, theme.snake_head)
                self.screen.blit(surf, (center_x - surf.get_width() // 2, y))
                y += 18

            y += 20
            title = self.fonts.splash_title.render(
                "LEARN2SLITHER", True, title_color
            )
            self.screen.blit(title, (center_x - title.get_width() // 2, y))

            y += 45
            sub_surf = self.fonts.splash.render(
                "RL Snake AI", True, theme.text_dim
            )
            cx = center_x
            self.screen.blit(sub_surf, (cx - sub_surf.get_width() // 2, y))

            y += 35
            pygame.draw.line(
                self.screen,
                theme.grid_line,
                (center_x - 80, y),
                (center_x + 80, y),
                2,
            )

            y += 25
            cx = center_x
            for text, color in [
                ("Manual Play", theme.apple_green),
                ("Display Panel: C", theme.highlight),
                ("Goal >= Length 10", theme.snake_body),
            ]:
                pygame.draw.circle(self.screen, color, (cx - 90, y + 7), 4)
                txt = self.fonts.splash_small.render(text, True, theme.text)
                self.screen.blit(txt, (cx - 75, y))
                y += 22

            y = height - 60
            if (frame // 30) % 2 == 0:
                prompt_surf = self.fonts.splash.render(
                    "[Press ENTER to start]", True, theme.highlight
                )
                self.screen.blit(
                    prompt_surf,
                    (center_x - prompt_surf.get_width() // 2, y),
                )

            y = height - 25
            foot = self.fonts.splash_small.render(
                "Q/Esc to quit", True, theme.text_dim
            )
            self.screen.blit(foot, (center_x - foot.get_width() // 2, y))

            pygame.display.flip()
            self.clock.tick(60)
            frame += 1

    # ------------------------------------------------------------------
    def render(
        self,
        board: "GameBoard",
        info: Optional[RenderInfo] = None,
    ) -> bool:
        """Render the current board. Return False if user requested quit."""
        if info is None:
            info = RenderInfo()
        fps = info.fps or self.default_fps

        self._apply_panel_flags()
        self._ensure_screen(board.size)

        green_eaten = info.length > self._last_length
        red_eaten = info.length < self._last_length and info.reward < 0
        self._last_length = info.length
        self.stats.update(info, green_eaten, red_eaten)
        if info.done:
            self.stats.end_episode(info)

        self._draw_scene(board, info)

        if self._paused and self.manage_events:
            if not self._wait_for_unpause():
                return False
            self._paused = False
            self._apply_panel_flags()
            self._ensure_screen(board.size)
            self._draw_scene(board, info)

        self.clock.tick(fps)

        if self.manage_events and not self.manual_mode:
            if self.step_mode:
                if not self._wait_for_step():
                    return False
            else:
                if not self._handle_events_run():
                    return False

        return True

    # ------------------------------------------------------------------
    def _wait_for_unpause(self) -> bool:
        while True:
            for event in pygame.event.get():
                if self._handle_panel_event(event):
                    continue
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_q, pygame.K_ESCAPE):
                        return False
                    if event.key == pygame.K_SPACE:
                        return True
            self.clock.tick(30)

    # ------------------------------------------------------------------
    def _handle_events_step(self) -> tuple[bool, bool]:
        for event in pygame.event.get():
            if self._handle_panel_event(event):
                continue
            if event.type == pygame.QUIT:
                return False, True
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_q, pygame.K_ESCAPE):
                    return False, True
                if event.key in (pygame.K_SPACE, pygame.K_RETURN, pygame.K_n):
                    return True, False
        return False, False

    # ------------------------------------------------------------------
    def _wait_for_step(self) -> bool:
        while True:
            advance, quit_requested = self._handle_events_step()
            if quit_requested:
                return False
            if advance:
                return True
            self.clock.tick(30)

    # ------------------------------------------------------------------
    def wait_for_step(self) -> bool:
        """Public wrapper for step-by-step wait (used by unified snake CLI)."""
        return self._wait_for_step()

    # ------------------------------------------------------------------
    def _handle_events_run(self) -> bool:
        for event in pygame.event.get():
            if self._handle_panel_event(event):
                continue
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_q, pygame.K_ESCAPE):
                    return False
        return True

    # ------------------------------------------------------------------
    def get_manual_action(self) -> int:
        key_to_action = {
            pygame.K_UP: 0,
            pygame.K_LEFT: 1,
            pygame.K_DOWN: 2,
            pygame.K_RIGHT: 3,
        }
        while True:
            for event in pygame.event.get():
                if self._handle_panel_event(event):
                    continue
                if event.type == pygame.QUIT:
                    return -1
                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_q, pygame.K_ESCAPE):
                        return -1
                    if self.panel.visible:
                        continue
                    if event.key in key_to_action:
                        return key_to_action[event.key]
            self.clock.tick(30)

    # ------------------------------------------------------------------
    def wait_for_game_over(self) -> bool:
        if self._screen is None:
            return False
        while True:
            for event in pygame.event.get():
                if self._handle_panel_event(event):
                    continue
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_q, pygame.K_ESCAPE):
                        return False
                    if event.key == pygame.K_SPACE:
                        self._paused = False
                        self._last_length = 0
                        return True
            self.clock.tick(30)

    # ------------------------------------------------------------------
    def wait_for_close(self) -> None:
        if self._screen is None:
            return
        print("Press Q or Esc to close viewer...")
        while True:
            for event in pygame.event.get():
                if self._handle_panel_event(event):
                    continue
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_q, pygame.K_ESCAPE):
                        return
            self.clock.tick(30)

    # ------------------------------------------------------------------
    def close(self) -> None:
        if self._screen is not None:
            pygame.display.quit()
        pygame.quit()

    # ------------------------------------------------------------------
    def __repr__(self) -> str:
        if self.manual_mode:
            mode = "manual"
        elif self.step_mode:
            mode = "step"
        else:
            mode = "continuous"
        return (
            f"Viewer(cell={self.settings.cell_size}, fps={self.default_fps}, "
            f"mode={mode}, theme={self.settings.theme_key})"
        )

    # ------------------------------------------------------------------
    @property
    def screen(self) -> pygame.Surface:
        if self._screen is None:
            raise RuntimeError("Screen not initialized. Call render() first.")
        return self._screen


__all__ = ["Viewer", "RenderInfo", "SessionStats"]
