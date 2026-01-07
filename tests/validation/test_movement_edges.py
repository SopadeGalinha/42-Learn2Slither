"""Movement edge-case validation tests."""
import unittest

from tests.validation.helpers import (
    Actions,
    Direction,
    new_board,
    trigger_self_collision,
    move_until_wall,
)


class TestMovementEdges(unittest.TestCase):
    """Ensure board_move handles all edge conditions."""

    def test_move_increments_counter(self) -> None:
        board = new_board()
        initial_moves = board.moves
        result = board.move(Direction.RIGHT)
        self.assertNotEqual(result, -1)
        self.assertEqual(board.moves, initial_moves + 1)

    def test_invalid_direction_returns_minus_one(self) -> None:
        board = new_board()
        self.assertEqual(board.move(99), -1)

    def test_wall_collision_sets_game_over(self) -> None:
        board = new_board()
        result = move_until_wall(board, Direction.DOWN)
        self.assertEqual(result, Actions.HIT_WALL)
        self.assertTrue(board.is_game_over)

    def test_self_collision_sets_game_over(self) -> None:
        board = new_board()
        result = trigger_self_collision(board)
        self.assertEqual(result, Actions.HIT_SELF)
        self.assertTrue(board.is_game_over)


if __name__ == "__main__":
    unittest.main()
