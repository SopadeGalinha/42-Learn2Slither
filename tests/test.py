"""Quick helper to visualize the current board."""

from __future__ import annotations

from slither import GameBoard


def main() -> None:
    board = GameBoard(size=10)
    board.reset()
    board.print_board()


if __name__ == "__main__":
    main()
