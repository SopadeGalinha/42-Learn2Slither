"""CLI entry point for training the Learn2Slither Q-learning agent."""

from __future__ import annotations

import argparse
import random
from pathlib import Path
from statistics import mean

from slither import GameBoard
from slither.agent import QLearningAgent


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Train Q-learning agent")
    add = parser.add_argument
    add("--sessions", type=int, default=100, help="Episodes")
    add("--max-steps", type=int, default=500, help="Max steps")
    add("--size", type=int, default=10, help="Board size")
    add("--alpha", type=float, default=0.1, help="Learning rate")
    add("--gamma", type=float, default=0.95, help="Discount factor")
    add("--epsilon", type=float, default=1.0, help="Initial epsilon")
    add("--min-epsilon", type=float, default=0.05, help="Min epsilon")
    add("--epsilon-decay", type=float, default=0.995, help="Decay")
    add("--seed", type=int, default=None, help="RNG seed")
    add("--save", type=Path, default=None, help="Save path")
    add("--load", type=Path, default=None, help="Load path")
    add("--dontlearn", action="store_true", help="Skip updates")
    return parser.parse_args()


def run_episode(
    board: GameBoard,
    agent: QLearningAgent,
    max_steps: int,
    learn: bool,
) -> dict[str, float]:
    board.reset()
    state = board.state
    total_reward = 0.0
    steps = 0

    while steps < max_steps:
        action = agent.select_action(state, explore=learn)
        next_state, reward, done = board.step(action)
        if learn:
            agent.update(state, action, reward, next_state, done)
        total_reward += reward
        state = next_state
        steps += 1
        if done:
            break

    return {
        "steps": steps,
        "reward": total_reward,
        "length": board.length,
        "max_length": board.max_length,
    }


def main() -> None:
    args = parse_args()

    if args.seed is not None:
        random.seed(args.seed)

    agent = QLearningAgent(
        alpha=args.alpha,
        gamma=args.gamma,
        epsilon=args.epsilon,
        min_epsilon=args.min_epsilon,
        epsilon_decay=args.epsilon_decay,
    )
    agent.load_or_initialize(args.load)
    if args.dontlearn:
        agent.set_learning(False)

    board = GameBoard(size=args.size)

    history: list[dict[str, float]] = []
    for episode in range(1, args.sessions + 1):
        learn = not args.dontlearn
        stats = run_episode(board, agent, args.max_steps, learn)
        history.append(stats)
        if not args.dontlearn:
            agent.decay_epsilon()
        print(
            f"Episode {episode:04d} - steps={stats['steps']:.0f} "
            f"reward={stats['reward']:.2f} length={stats['length']} "
            f"max_length={stats['max_length']} epsilon={agent.epsilon:.3f}"
        )

    avg_reward = mean(item["reward"] for item in history)
    best_length = max(item["max_length"] for item in history)
    print("\nTraining complete")
    print(f"Episodes: {args.sessions}")
    print(f"Average reward: {avg_reward:.2f}")
    print(f"Best length: {best_length}")

    if args.save is not None:
        metadata = {
            "episodes": args.sessions,
            "max_length": best_length,
            "avg_reward": avg_reward,
        }
        path = agent.save_model(args.save, metadata=metadata)
        print(f"Model saved to {path}")


if __name__ == "__main__":
    main()
