"""Interactive configuration panel for the viewer."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List

try:  # pragma: no cover - optional dependency
    import pygame
except ImportError:  # pragma: no cover
    pygame = None  # type: ignore

from .fonts import FontSet
from .theme import DisplayTheme, get_theme, list_themes
from .settings import DisplaySettings, CELL_STEP, LEGEND_STEP


@dataclass
class PanelFlags:
    """Flags describing what changed while the panel was open."""

    theme_changed: bool = False
    layout_changed: bool = False


class ConfigPanel:
    """Keyboard-driven overlay for tweaking display settings."""

    def __init__(self, settings: DisplaySettings) -> None:
        self.settings = settings
        self.visible = False
        self.selected = 0
        self._flags = PanelFlags()
        self._theme_keys: List[str] = list(list_themes())

    # ------------------------------------------------------------------
    def toggle(self) -> None:
        self.visible = not self.visible
        self._flags = PanelFlags()

    # ------------------------------------------------------------------
    def handle_event(self, event) -> bool:
        if event.type == pygame.KEYDOWN and event.key == pygame.K_c:
            self.toggle()
            return True

        if not self.visible:
            return False

        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_ESCAPE, pygame.K_TAB):
                self.toggle()
                return True
            if event.key == pygame.K_UP:
                self.selected = (self.selected - 1) % len(self._options())
                return True
            if event.key == pygame.K_DOWN:
                self.selected = (self.selected + 1) % len(self._options())
                return True
            if event.key in (pygame.K_LEFT, pygame.K_h):
                self._adjust_selected(-1)
                return True
            if event.key in (pygame.K_RIGHT, pygame.K_l):
                self._adjust_selected(1)
                return True
            if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                self._adjust_selected(1)
                return True
        return False

    # ------------------------------------------------------------------
    def consume_flags(self) -> PanelFlags:
        flags, self._flags = self._flags, PanelFlags()
        return flags

    # ------------------------------------------------------------------
    def render(
        self,
        screen: "pygame.Surface",
        fonts: FontSet,
        theme: DisplayTheme,
    ) -> None:
        if not self.visible:
            return

        overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        overlay.fill((10, 10, 16, 180))
        screen.blit(overlay, (0, 0))

        width = 360
        height = 280
        rect = pygame.Rect(
            screen.get_width() // 2 - width // 2,
            screen.get_height() // 2 - height // 2,
            width,
            height,
        )
        pygame.draw.rect(screen, theme.hud_background, rect, border_radius=10)
        pygame.draw.rect(screen, theme.grid_line, rect, width=2, border_radius=10)

        title = fonts.title.render("Display Settings", True, theme.text)
        screen.blit(title, (rect.x + 20, rect.y + 15))

        subtitle = fonts.small.render("[C] Close | Arrows Adjust", True, theme.text_dim)
        screen.blit(subtitle, (rect.x + 20, rect.y + 40))

        y = rect.y + 70
        for idx, option in enumerate(self._options()):
            is_selected = idx == self.selected
            label_surf = fonts.hud.render(option.label, True, theme.text)
            value_surf = fonts.hud.render(option.value, True, theme.highlight)
            if is_selected:
                highlight_rect = pygame.Rect(rect.x + 12, y - 4, rect.width - 24, 30)
                pygame.draw.rect(
                    screen,
                    theme.grid_line,
                    highlight_rect,
                    border_radius=6,
                )
            screen.blit(label_surf, (rect.x + 20, y))
            screen.blit(value_surf, (rect.right - value_surf.get_width() - 20, y))
            y += 32

    # ------------------------------------------------------------------
    class _Option:
        def __init__(self, label: str, value: str) -> None:
            self.label = label
            self.value = value

    # ------------------------------------------------------------------
    def _options(self) -> list["ConfigPanel._Option"]:
        theme_name = get_theme(self.settings.theme_key).name
        return [
            self._Option("Theme", theme_name),
            self._Option("Cell Size", f"{self.settings.cell_size}px"),
            self._Option("Legend Width", f"{self.settings.legend_width}px"),
            self._Option("Show HUD", "On" if self.settings.show_hud else "Off"),
            self._Option(
                "Show Legend",
                "On" if self.settings.show_legend else "Off",
            ),
            self._Option(
                "Grid Lines",
                "On" if self.settings.show_grid_lines else "Off",
            ),
            self._Option(
                "Agent View",
                "On" if self.settings.agent_view else "Off",
            ),
        ]

    # ------------------------------------------------------------------
    def _adjust_selected(self, direction: int) -> None:
        idx = self.selected
        if idx == 0:
            self._cycle_theme(direction)
        elif idx == 1:
            if self.settings.adjust_cell_size(CELL_STEP * direction):
                self._flags.layout_changed = True
        elif idx == 2:
            if self.settings.adjust_legend_width(LEGEND_STEP * direction):
                self._flags.layout_changed = True
        elif idx == 3:
            self.settings.show_hud = not self.settings.show_hud
            self._flags.layout_changed = True
        elif idx == 4:
            self.settings.show_legend = not self.settings.show_legend
            self._flags.layout_changed = True
        elif idx == 5:
            self.settings.show_grid_lines = not self.settings.show_grid_lines
        elif idx == 6:
            self.settings.agent_view = not self.settings.agent_view

    # ------------------------------------------------------------------
    def _cycle_theme(self, direction: int) -> None:
        if not self._theme_keys:
            return
        current = self._theme_keys.index(self.settings.theme_key)
        new_index = (current + direction) % len(self._theme_keys)
        if new_index != current:
            self.settings.theme_key = self._theme_keys[new_index]
            self._flags.theme_changed = True


__all__ = ["ConfigPanel", "PanelFlags"]
