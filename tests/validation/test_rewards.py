"""Apple consumption and reward accessor validation tests."""
import unittest

from slither.core._library import board_lib
from slither.core.rewards import (
    REWARD_DEATH,
    REWARD_GREEN_APPLE,
    REWARD_RED_APPLE,
    REWARD_STEP,
)

from tests.validation.helpers import (
    Actions,
    BoardCell,
    consume_row_aligned_cell,
    new_board,
)


class TestAppleInteractions(unittest.TestCase):
    """Ensure apple events and reward accessors are stable."""

    def test_green_apple_increases_score_and_length(self) -> None:
        board = new_board()
        result = consume_row_aligned_cell(board, BoardCell.GREEN_APPLE)
        self.assertEqual(result, Actions.ATE_GREEN_APPLE)
        self.assertEqual(board.score, 10)
        self.assertEqual(board.length, 4)
        self.assertGreaterEqual(board.max_length, 4)

    def test_red_apple_decreases_score_and_length(self) -> None:
        board = new_board()
        result = consume_row_aligned_cell(board, BoardCell.RED_APPLE)
        self.assertEqual(result, Actions.ATE_RED_APPLE)
        self.assertEqual(board.score, -10)
        self.assertEqual(board.length, 2)
        self.assertGreaterEqual(board.moves, 1)

    def test_reward_accessors_match_python_constants(self) -> None:
        self.assertAlmostEqual(
            REWARD_GREEN_APPLE,
            board_lib.board_get_reward_green_apple(),
            places=5,
        )
        self.assertAlmostEqual(
            REWARD_RED_APPLE,
            board_lib.board_get_reward_red_apple(),
            places=5,
        )
        self.assertAlmostEqual(
            REWARD_DEATH,
            board_lib.board_get_reward_death(),
            places=5,
        )
        self.assertAlmostEqual(
            REWARD_STEP,
            board_lib.board_get_reward_step(),
            places=5,
        )


if __name__ == "__main__":
    unittest.main()
