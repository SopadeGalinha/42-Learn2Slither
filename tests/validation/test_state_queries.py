"""State/query validation tests for the board wrapper."""
import unittest

from tests.validation.helpers import (
    Actions,
    BoardCell,
    Direction,
    new_board,
)
from slither.core.rewards import (
    REWARD_DEATH,
    REWARD_GREEN_APPLE,
    REWARD_RED_APPLE,
    REWARD_STEP,
)


class TestStateQueries(unittest.TestCase):
    """Validate getter functions exposed via libc."""

    def test_reset_restores_counters(self) -> None:
        board = new_board()
        board.move(Direction.RIGHT)
        board.move(Direction.RIGHT)
        self.assertGreater(board.moves, 0)
        board.reset()
        self.assertEqual(board.moves, 0)
        self.assertEqual(board.score, 0)
        self.assertEqual(board.length, 3)
        self.assertFalse(board.is_game_over)

    def test_state_encoding_is_12_bit(self) -> None:
        board = new_board()
        state = board.state
        self.assertIsInstance(state, int)
        self.assertGreaterEqual(state, 0)
        self.assertLessEqual(state, 0xFFF)

    def test_get_cell_boundaries(self) -> None:
        board = new_board()
        self.assertEqual(board.get_cell(-1, 0), BoardCell.WALL)
        self.assertEqual(board.get_cell(board.size, 0), BoardCell.WALL)
        center_value = board.get_cell(board.size // 2, board.size // 2)
        self.assertIn(center_value, {
            BoardCell.EMPTY,
            BoardCell.SNAKE_BODY,
            BoardCell.SNAKE_HEAD,
            BoardCell.GREEN_APPLE,
            BoardCell.RED_APPLE,
        })

    def test_print_board_executes_without_error(self) -> None:
        board = new_board()
        board.print_board()

    def test_step_returns_reward_tuple(self) -> None:
        board = new_board()
        state, reward, done = board.step(Direction.RIGHT)
        self.assertIsInstance(state, int)
        self.assertIn(reward, {
            REWARD_GREEN_APPLE,
            REWARD_RED_APPLE,
            REWARD_DEATH,
            REWARD_STEP,
        })
        self.assertIsInstance(done, bool)
        self.assertIn(board.move(Direction.RIGHT), {
            Actions.NORMAL_MOVE,
            Actions.ATE_GREEN_APPLE,
            Actions.ATE_RED_APPLE,
            Actions.HIT_SELF,
            Actions.HIT_WALL,
            Actions.LENGTH_ZERO,
        })


if __name__ == "__main__":
    unittest.main()
