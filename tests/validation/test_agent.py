"""Tests for the QLearningAgent helper."""

from __future__ import annotations

from pathlib import Path

from slither.agent import QLearningAgent


def test_best_action_prefers_highest_value() -> None:
    agent = QLearningAgent(epsilon=0.0)
    agent.q_table[0] = [1.0, 2.0, 1.5, 2.0]
    # With epsilon=0, greedy choice should hit one of the maxima.
    for _ in range(10):
        action = agent.select_action(0, explore=False)
        assert action in {1, 3}


def test_update_matches_bellman_target() -> None:
    agent = QLearningAgent(alpha=0.5, gamma=0.9, epsilon=0.0)
    state = 5
    next_state = 7
    agent.q_table[state] = [0.0, 0.0, 0.0, 0.0]
    agent.q_table[next_state] = [1.0, 2.0, 3.0, 4.0]
    agent.update(state, 2, reward=1.0, next_state=next_state, done=False)
    expected = 0.0 + 0.5 * (1.0 + 0.9 * 4.0 - 0.0)
    assert agent.q_table[state][2] == expected


def test_save_and_load_roundtrip(tmp_path: Path) -> None:
    agent = QLearningAgent(epsilon=0.5)
    agent.q_table = {1: [0.1, 0.2, 0.3, 0.4]}
    path = tmp_path / "checkpoint.json"
    agent.save_model(path, metadata={"episodes": 42})

    restored = QLearningAgent()
    restored.load_model(path)
    assert restored.q_table == agent.q_table
    assert restored.epsilon == agent.epsilon
