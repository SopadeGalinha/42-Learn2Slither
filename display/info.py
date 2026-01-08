"""Common data structures shared by display components."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class RenderInfo:
    """Information exposed to the viewer for a single render step."""

    episode: int = 0
    step: int = 0
    reward: float = 0.0
    length: int = 0
    score: int = 0
    done: bool = False
    fps: int = 10


@dataclass
class SessionStats:
    """Statistics tracked across the current play session."""

    episodes_played: int = 0
    max_length: int = 0
    max_steps: int = 0
    wins: int = 0
    episode_greens: int = 0
    episode_reds: int = 0
    _last_episode: int = 0

    def update(
        self,
        info: RenderInfo,
        green_eaten: bool = False,
        red_eaten: bool = False,
    ) -> None:
        if info.episode != self._last_episode:
            self._last_episode = info.episode
            self.episode_greens = 0
            self.episode_reds = 0

        if green_eaten:
            self.episode_greens += 1
        if red_eaten:
            self.episode_reds += 1

        if info.length > self.max_length:
            self.max_length = info.length

    def end_episode(self, info: RenderInfo) -> None:
        self.episodes_played += 1

        if info.step > self.max_steps:
            self.max_steps = info.step

        if info.length >= 10:
            self.wins += 1


__all__ = ["RenderInfo", "SessionStats"]
