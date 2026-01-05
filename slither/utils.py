"""Utility functions and constants for snake visualization."""

from __future__ import annotations
from enum import Enum

from ._types import BoardCell, Direction

ACTION_TO_DIRECTION = {
    0: Direction.UP,
    1: Direction.LEFT,
    2: Direction.DOWN,
    3: Direction.RIGHT,
}

ACTION_NAMES = {0: "UP", 1: "LEFT", 2: "DOWN", 3: "RIGHT"}

CELL_SYMBOLS = {
    BoardCell.EMPTY: "0",
    BoardCell.WALL: "W",
    BoardCell.SNAKE_HEAD: "H",
    BoardCell.SNAKE_BODY: "S",
    BoardCell.GREEN_APPLE: "G",
    BoardCell.RED_APPLE: "R",
}

class RenderMode(Enum):
    NONE = "none"
    SLOW = "slow"
    FAST = "fast"
    STEP = "step"


def get_direction(action_idx: int) -> int:
    return ACTION_TO_DIRECTION.get(action_idx, Direction.RIGHT)


def get_vision_cells(board) -> dict[str, int]:
    size = board.size
    head_x, head_y = -1, -1

    for y in range(size):
        for x in range(size):
            if board.get_cell(x, y) == BoardCell.SNAKE_HEAD:
                head_x, head_y = x, y
                break
        if head_x >= 0:
            break

    def get_cell_safe(x: int, y: int) -> int:
        if x < 0 or x >= size or y < 0 or y >= size:
            return BoardCell.WALL
        return board.get_cell(x, y)

    return {
        "up": get_cell_safe(head_x, head_y - 1),
        "left": get_cell_safe(head_x - 1, head_y),
        "down": get_cell_safe(head_x, head_y + 1),
        "right": get_cell_safe(head_x + 1, head_y),
    }


def print_vision(board, action_idx: int, reward: float = 0.0) -> None:
    vision = get_vision_cells(board)

    up = CELL_SYMBOLS.get(vision["up"], "?")
    left = CELL_SYMBOLS.get(vision["left"], "?")
    down = CELL_SYMBOLS.get(vision["down"], "?")
    right = CELL_SYMBOLS.get(vision["right"], "?")
    action = ACTION_NAMES.get(action_idx, "?")

    print(f"""
      {up}
      |
  {left} - H - {right}
      |
      {down}
Action: {action}  Reward: {reward:+.1f}
""")


def print_summary(episodes: int, max_length: int, max_duration: int) -> None:
    separator = "=" * 50
    print(f"\n{separator}")
    print(f"Game complete: {episodes} episode(s)")
    print(f"Max length achieved: {max_length}")
    print(f"Max duration (steps): {max_duration}")
    print(separator)


__all__ = [
    "ACTION_TO_DIRECTION",
    "ACTION_NAMES",
    "CELL_SYMBOLS",
    "RenderMode",
    "get_direction",
    "get_vision_cells",
    "print_vision",
    "print_summary",
]
