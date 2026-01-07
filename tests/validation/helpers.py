"""Shared helpers for validation tests."""
from __future__ import annotations

import contextlib
import io
from typing import Iterable, List, Tuple

from slither.core.board import GameBoard
from slither.core._types import Actions, BoardCell, Direction

CELL_TO_ACTION = {
    BoardCell.GREEN_APPLE: Actions.ATE_GREEN_APPLE,
    BoardCell.RED_APPLE: Actions.ATE_RED_APPLE,
}


def new_board(size: int = 10) -> GameBoard:
    """Create a new board instance for tests."""
    return GameBoard(size=size)


def get_head_position(board: GameBoard) -> Tuple[int, int]:
    """Return the (x, y) coordinates of the snake head."""
    for y in range(board.size):
        for x in range(board.size):
            if board.get_cell(x, y) == BoardCell.SNAKE_HEAD:
                return x, y
    raise RuntimeError("Head position not found on board")


def capture_board_print(board: GameBoard) -> str:
    """Capture output from board.print_board()."""
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        board.print_board()
    return buffer.getvalue()


def move_until_wall(
    board: GameBoard,
    direction: int,
    limit: int | None = None,
) -> int:
    """Move in a direction until a wall collision occurs."""
    board.reset()
    limit = limit or (board.size + 2)
    for _ in range(limit):
        outcome = board.move(direction)
        if outcome == Actions.HIT_WALL:
            return outcome
    raise RuntimeError("Failed to collide with wall within step limit")


def trigger_self_collision(board: GameBoard) -> int:
    """Force the snake to collide with itself by moving upward immediately."""
    board.reset()
    return board.move(Direction.UP)


def consume_row_aligned_cell(
    board: GameBoard,
    cell_type: int,
    *,
    max_attempts: int = 128,
    reset_between_attempts: bool = True,
) -> int:
    """Consume an apple aligned with the head on the same row."""
    if cell_type not in CELL_TO_ACTION:
        raise ValueError("Only apple cells are supported")
    expected_action = CELL_TO_ACTION[cell_type]
    attempts = 0
    if reset_between_attempts:
        board.reset()
    while attempts < max_attempts:
        head_x, head_y = get_head_position(board)
        targets: List[int] = [
            x for x in range(board.size)
            if x != head_x and board.get_cell(x, head_y) == cell_type
        ]
        for target_x in targets:
            if target_x > head_x:
                direction = Direction.RIGHT
            else:
                direction = Direction.LEFT
            steps = abs(target_x - head_x)
            result = None
            for _ in range(steps):
                result = board.move(direction)
                if result == expected_action:
                    return result
        attempts += 1
        if reset_between_attempts:
            board.reset()
    raise RuntimeError(
        f"Unable to align cell type {cell_type} after {max_attempts} attempts"
    )


def make_moves(board: GameBoard, directions: Iterable[int]) -> List[int]:
    """Execute a sequence of moves and return their outcomes."""
    results: List[int] = []
    for direction in directions:
        results.append(board.move(direction))
    return results


__all__ = [
    "Actions",
    "BoardCell",
    "Direction",
    "CELL_TO_ACTION",
    "capture_board_print",
    "consume_row_aligned_cell",
    "get_head_position",
    "make_moves",
    "move_until_wall",
    "new_board",
    "trigger_self_collision",
]
