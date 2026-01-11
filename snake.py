#!/usr/bin/env python3
"""
Unified CLI for Learn2Slither - Snake Reinforcement Learning.

Usage examples from the subject:
    ./snake -sessions 10 -save models/10sess.txt -visual off
    ./snake -visual on -load models/100sess.txt -dontlearn
    ./snake -visual on -load models/1000sess.txt
"""

from __future__ import annotations

import argparse
import random
import sys
from pathlib import Path
from statistics import mean

from slither import GameBoard
from slither.agent import QLearningAgent
from slither.utils import get_direction, print_vision

# Runtime imports for optional viewer (pygame may not be available)
Viewer = None
RenderInfo = None


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments matching the subject specification."""
    parser = argparse.ArgumentParser(
        description="Learn2Slither - Snake Reinforcement Learning",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s -sessions 10 -save models/10sess.txt -visual off
  %(prog)s -visual on -load models/100sess.txt -dontlearn
  %(prog)s -visual on -load models/1000sess.txt
        """,
    )

    # Core flags from subject
    parser.add_argument(
        "-sessions",
        type=int,
        default=1,
        help="Number of training sessions/episodes to run",
    )
    parser.add_argument(
        "-save",
        type=Path,
        default=None,
        help="Path to save the trained model",
    )
    parser.add_argument(
        "-load",
        type=Path,
        default=None,
        help="Path to load an existing model",
    )
    parser.add_argument(
        "-visual",
        type=str,
        choices=["on", "off"],
        default="on",
        help="Enable or disable graphical display (on/off)",
    )
    parser.add_argument(
        "-dontlearn",
        action="store_true",
        help="Run without updating the Q-table (evaluation mode)",
    )
    parser.add_argument(
        "-step-by-step",
        action="store_true",
        dest="step_by_step",
        help="Enable step-by-step mode (wait for input between moves)",
    )

    # Additional useful flags
    parser.add_argument(
        "-size",
        type=int,
        default=10,
        help="Board size (8-20, default: 10)",
    )
    parser.add_argument(
        "-fps",
        type=int,
        default=10,
        help="Frames per second for visual mode (default: 10)",
    )
    parser.add_argument(
        "-max-steps",
        type=int,
        default=500,
        dest="max_steps",
        help="Maximum steps per episode (default: 500)",
    )
    parser.add_argument(
        "-seed",
        type=int,
        default=None,
        help="Random seed for reproducibility",
    )
    parser.add_argument(
        "-verbose",
        "-v",
        action="store_true",
        help="Print snake vision to terminal",
    )

    parser.add_argument(
        "-evaluation",
        action="store_true",
        help="Force subject-compliant defaults for evaluation (size=10, verbose on)",
    )

    # Q-learning hyperparameters
    parser.add_argument(
        "-alpha",
        type=float,
        default=0.1,
        help="Learning rate (default: 0.1)",
    )
    parser.add_argument(
        "-gamma",
        type=float,
        default=0.95,
        help="Discount factor (default: 0.95)",
    )
    parser.add_argument(
        "-epsilon",
        type=float,
        default=1.0,
        help="Initial exploration rate (default: 1.0)",
    )
    parser.add_argument(
        "-min-epsilon",
        type=float,
        default=0.1,
        dest="min_epsilon",
        help="Minimum exploration rate (default: 0.05)",
    )
    parser.add_argument(
        "-epsilon-decay",
        type=float,
        default=0.999,
        dest="epsilon_decay",
        help="Epsilon decay rate per episode (default: 0.995)",
    )

    return parser.parse_args()


def create_viewer(args: argparse.Namespace):
    """Create viewer if visual mode is enabled."""
    global Viewer, RenderInfo
    if args.visual == "off":
        return None

    try:
        from slither import Viewer, RenderInfo
    except ImportError:
        print("Warning: pygame not available, running without visualization")
        return None

    # If optional viewer failed to import earlier, bail out gracefully
    if Viewer is None:
        print("Warning: viewer unavailable (pygame missing), running without visualization\n")
        return None

    return Viewer(
        cell_size=32,
        fps=args.fps,
        step_mode=args.step_by_step,
        manual_mode=False,
    )


def run_episode_headless(
    board: GameBoard,
    agent: QLearningAgent,
    max_steps: int,
    learn: bool,
    verbose: bool = False,
) -> dict:
    """Run a single episode without visualization."""
    board.reset()
    state = board.state
    total_reward = 0.0
    steps = 0

    while steps < max_steps:
        action = agent.select_action(state, explore=learn)

        if verbose:
            print_vision(board, action, 0.0)

        next_state, reward, done = board.step(get_direction(action))

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


def run_episode_visual(
    board: GameBoard,
    agent: QLearningAgent,
    viewer,
    args: argparse.Namespace,
    episode: int,
    learn: bool,
) -> dict:
    """Run a single episode with visualization."""
    board.reset()
    state = board.state
    total_reward = 0.0
    steps = 0

    # Show initial state
    info = RenderInfo(
        episode=episode,
        step=0,
        reward=0.0,
        length=board.length,
        score=board.score,
        done=False,
        fps=args.fps,
    )
    if not viewer.render(board, info):
        return {"steps": 0, "reward": 0.0, "length": 0, "max_length": 0}

    while steps < args.max_steps:
        steps += 1

        # Agent selects action
        action = agent.select_action(state, explore=learn)

        if args.verbose:
            print_vision(board, action, 0.0)

        # Execute action
        next_state, reward, done = board.step(get_direction(action))

        if learn:
            agent.update(state, action, reward, next_state, done)

        total_reward += reward
        state = next_state

        # Render
        info = RenderInfo(
            episode=episode,
            step=steps,
            reward=reward,
            length=board.length,
            score=board.score,
            done=done,
            fps=args.fps,
        )
        if not viewer.render(board, info):
            break

        if done:
            viewer.wait_for_game_over()
            break

        # In step-by-step mode, wait for user input
        if args.step_by_step:
            if not viewer.wait_for_step():
                break

    return {
        "steps": steps,
        "reward": total_reward,
        "length": board.length,
        "max_length": board.max_length,
    }


def main() -> int:
    """Main entry point for the unified snake CLI."""
    args = parse_args()

    # Evaluation preset: enforce subject defaults regardless of user inputs
    if getattr(args, "evaluation", False):
        args.size = 10
        args.verbose = True
        args.visual = "on"
        args.step_by_step = False

    # Set random seed if provided
    if args.seed is not None:
        random.seed(args.seed)

    # Validate board size
    if not 8 <= args.size <= 20:
        print(f"Error: Board size must be between 8 and 20, got {args.size}")
        return 1

    # Initialize agent
    agent = QLearningAgent(
        alpha=args.alpha,
        gamma=args.gamma,
        epsilon=args.epsilon,
        min_epsilon=args.min_epsilon,
        epsilon_decay=args.epsilon_decay,
    )

    # Load existing model if specified
    if args.load is not None:
        if args.load.exists():
            agent.load_model(args.load)
            print(f"Load trained model from {args.load}")
        else:
            print(f"Warning: Model file {args.load} not found, starting fresh")

    # Set learning mode
    learn = not args.dontlearn
    if args.dontlearn:
        agent.set_learning(False)

    # Create board and viewer
    board = GameBoard(size=args.size)
    viewer = create_viewer(args)

    # Show splash screen if visual
    if viewer is not None:
        if not viewer.show_splash(board.size):
            viewer.close()
            return 0

    # Run training/evaluation sessions
    history: list[dict] = []
    max_length_overall = 0
    max_duration_overall = 0

    try:
        for episode in range(1, args.sessions + 1):
            if viewer is not None:
                stats = run_episode_visual(
                    board, agent, viewer, args, episode, learn
                )
            else:
                stats = run_episode_headless(
                    board, agent, args.max_steps, learn, args.verbose
                )

            history.append(stats)

            # Track best metrics
            max_length_overall = max(max_length_overall, stats["max_length"])
            max_duration_overall = max(max_duration_overall, stats["steps"])

            # Decay epsilon after each episode
            if learn:
                agent.decay_epsilon()

            # Print episode summary
            print(
                f"Episode {episode:04d} - "
                f"steps={stats['steps']:.0f} "
                f"reward={stats['reward']:.2f} "
                f"length={stats['length']} "
                f"max_length={stats['max_length']} "
                f"epsilon={agent.epsilon:.3f}"
            )

    except KeyboardInterrupt:
        print("\nTraining interrupted by user")

    finally:
        if viewer is not None:
            viewer.close()

    # Print final summary
    print(f"\nGame over, max length = {max_length_overall}, "
          f"max duration = {max_duration_overall}")

    if history:
        avg_reward = mean(item["reward"] for item in history)
        print(f"Average reward: {avg_reward:.2f}")
        print(f"Sessions completed: {len(history)}")

    # Save model if requested
    if args.save is not None:
        metadata = {
            "episodes": len(history),
            "max_length": max_length_overall,
            "avg_reward": mean(h["reward"] for h in history) if history else 0,
        }
        path = agent.save_model(args.save, metadata=metadata)
        print(f"Save learning state in {path}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
