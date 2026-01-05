"""Manual snake game using Learn2Slither."""

from __future__ import annotations

import argparse
import random
from dataclasses import dataclass
from typing import TYPE_CHECKING, Optional

from slither import GameBoard
from slither.utils import RenderMode, get_direction, print_vision, print_summary

if TYPE_CHECKING:
    from slither import Viewer, RenderInfo

# Runtime import for optional viewer
try:
    from slither import Viewer as _Viewer, RenderInfo as _RenderInfo
except Exception:  # viewer is optional
    _Viewer = None
    _RenderInfo = None


@dataclass
class EpisodeResult:
    """Result of a single game episode."""
    steps: int
    score: int
    total_reward: float


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Play snake manually")
    parser.add_argument(
        "--episodes", type=int, default=1, help="Number of episodes to run"
    )
    parser.add_argument(
        "--max-steps", type=int, default=500, help="Max steps per episode"
    )
    parser.add_argument(
        "--render",
        type=RenderMode,
        choices=list(RenderMode),
        default=RenderMode.STEP,
        help="Render mode",
    )
    parser.add_argument("--fps", type=int, default=10, help="FPS when rendering")
    parser.add_argument("--seed", type=int, default=None, help="Random seed")
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Show snake vision in terminal"
    )
    parser.add_argument(
        "--keep-open", action="store_true", help="Keep viewer open after training"
    )
    return parser.parse_args()


def create_viewer(render_mode: RenderMode, fps: int) -> Optional[Viewer]:
    if render_mode == RenderMode.NONE:
        return None
    if _Viewer is None or _RenderInfo is None:
        raise RuntimeError("Viewer not available; install pygame or set --render none")

    is_step_mode = render_mode == RenderMode.STEP
    effective_fps = 60 if render_mode == RenderMode.FAST else fps
    return _Viewer(cell_size=32, fps=effective_fps, step_mode=is_step_mode, manual_mode=True)


def run_episode(
    board: GameBoard,
    args: argparse.Namespace,
    viewer: Optional[Viewer] = None,
    episode: int = 1,
) -> EpisodeResult:
    board.reset()
    total_reward = 0.0
    steps = 0

    # Show initial state (step 0) with pause
    if viewer is not None and _RenderInfo is not None:
        info = _RenderInfo(
            episode=episode,
            step=0,
            reward=0.0,
            length=board.length,
            score=board.score,
            done=False,
            fps=args.fps,
        )
        if not viewer.render(board, info):
            return EpisodeResult(steps=0, score=0, total_reward=0.0)

    while steps < args.max_steps:
        steps += 1
        # Manual mode: get action from keyboard
        if viewer is not None:
            action_idx = viewer.get_manual_action()
            if action_idx < 0:  # User quit
                break
        else:
            # No viewer, pick random action
            action_idx = random.randrange(4)
        direction = get_direction(action_idx)
        _, reward, done = board.step(direction)

        total_reward += reward

        if args.verbose:
            print_vision(board, action_idx, reward)

        if viewer is not None and _RenderInfo is not None:
            info = _RenderInfo(
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

            # Wait for input on game over screen
            if done:
                if not viewer.wait_for_game_over():
                    break  # User chose to quit

        if done:
            break

    return EpisodeResult(steps=steps, score=board.score, total_reward=total_reward)


def main() -> None:
    args = parse_args()

    if args.seed is not None:
        random.seed(args.seed)

    board = GameBoard()
    viewer = create_viewer(args.render, args.fps)

    # Show splash screen if viewer is enabled
    if viewer is not None:
        if not viewer.show_splash(board.size):
            viewer.close()
            return

    max_length = 0
    max_duration = 0

    try:
        for ep in range(1, args.episodes + 1):
            result = run_episode(board, args, viewer, ep)
            max_length = max(max_length, board.max_length)
            max_duration = max(max_duration, result.steps)
            print(
                f"Episode {ep:04d}: steps={result.steps} score={result.score} "
                f"return={result.total_reward:.2f} length={board.length} max_length={board.max_length}"
            )
    finally:
        if viewer is not None:
            if args.keep_open:
                viewer.wait_for_close()
            viewer.close()

        print_summary(args.episodes, max_length, max_duration)


if __name__ == "__main__":
    main()
