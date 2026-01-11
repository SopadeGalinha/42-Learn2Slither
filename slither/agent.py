"""Tabular Q-learning agent tailored for the Learn2Slither board."""

from __future__ import annotations

import json
import random
from pathlib import Path
from typing import Dict, List, MutableMapping

__all__ = ["QLearningAgent"]


class QLearningAgent:
    """Simple tabular Q-learning agent with JSON persistence."""

    def __init__(
        self,
        alpha: float = 0.1,
        gamma: float = 0.95,
        epsilon: float = 1.0,
        min_epsilon: float = 0.1,
        epsilon_decay: float = 0.999,
        num_actions: int = 4,
    ) -> None:
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.min_epsilon = min_epsilon
        self.epsilon_decay = epsilon_decay
        self.num_actions = num_actions
        self.learning_enabled = True
        self.q_table: Dict[int, List[float]] = {}

    # ------------------------------------------------------------------
    def _ensure_state(self, state: int) -> None:
        if state not in self.q_table:
            self.q_table[state] = [0.0 for _ in range(self.num_actions)]

    # ------------------------------------------------------------------
    def select_action(self, state: int, explore: bool = True) -> int:
        self._ensure_state(state)
        if (
            explore
            and self.learning_enabled
            and random.random() < self.epsilon
        ):
            return random.randrange(self.num_actions)
        return self.best_action(state)

    # ------------------------------------------------------------------
    def best_action(self, state: int) -> int:
        self._ensure_state(state)
        values = self.q_table[state]
        max_value = max(values)
        best = [i for i, v in enumerate(values) if v == max_value]
        return random.choice(best)

    # ------------------------------------------------------------------
    def update(
        self,
        state: int,
        action: int,
        reward: float,
        next_state: int,
        done: bool,
    ) -> None:
        if not self.learning_enabled:
            return
        self._ensure_state(state)
        target = reward
        if not done:
            self._ensure_state(next_state)
            target += self.gamma * max(self.q_table[next_state])
        current = self.q_table[state][action]
        self.q_table[state][action] = current + self.alpha * (target - current)

    # ------------------------------------------------------------------
    def decay_epsilon(self) -> None:
        if not self.learning_enabled:
            return
        self.epsilon = max(self.min_epsilon, self.epsilon * self.epsilon_decay)

    # ------------------------------------------------------------------
    def set_learning(self, enabled: bool) -> None:
        self.learning_enabled = enabled
        if not enabled:
            self.epsilon = 0.0

    # ------------------------------------------------------------------
    def save_model(
        self,
        path: str | Path,
        metadata: MutableMapping[str, object] | None = None,
    ) -> Path:
        file_path = Path(path)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "alpha": self.alpha,
            "gamma": self.gamma,
            "epsilon": self.epsilon,
            "min_epsilon": self.min_epsilon,
            "epsilon_decay": self.epsilon_decay,
            "num_actions": self.num_actions,
            "learning_enabled": self.learning_enabled,
            "q_table": {
                str(s): v for s, v in self.q_table.items()
            },
            "metadata": dict(metadata or {}),
        }
        file_path.write_text(json.dumps(payload, indent=2))
        return file_path

    # ------------------------------------------------------------------
    def load_model(self, path: str | Path) -> None:
        file_path = Path(path)
        data = json.loads(file_path.read_text())
        self.alpha = float(data.get("alpha", self.alpha))
        self.gamma = float(data.get("gamma", self.gamma))
        self.epsilon = float(data.get("epsilon", self.epsilon))
        self.min_epsilon = float(data.get("min_epsilon", self.min_epsilon))
        decay = data.get("epsilon_decay", self.epsilon_decay)
        self.epsilon_decay = float(decay)
        self.num_actions = int(data.get("num_actions", self.num_actions))
        self.learning_enabled = bool(data.get("learning_enabled", True))
        raw_table = data.get("q_table", {})
        self.q_table = {
            int(state): [float(value) for value in values]
            for state, values in raw_table.items()
        }

    # ------------------------------------------------------------------
    def load_or_initialize(self, path: str | Path | None) -> None:
        if path is None:
            return
        file_path = Path(path)
        if file_path.exists():
            self.load_model(file_path)

    # ------------------------------------------------------------------
    def summary(self) -> dict[str, object]:
        return {
            "states": len(self.q_table),
            "epsilon": round(self.epsilon, 4),
            "alpha": self.alpha,
            "gamma": self.gamma,
        }
