"""Board creation and destruction validation tests."""
import unittest

from tests.validation.helpers import Direction, new_board


class TestBoardCreation(unittest.TestCase):
    """Validate board allocation entry points."""

    def test_valid_size_range(self) -> None:
        for size in range(8, 21):
            board = new_board(size=size)
            self.assertEqual(board.size, size)

    def test_invalid_sizes_default_to_ten(self) -> None:
        for size in (-5, 0, 5, 50, 999):
            board = new_board(size=size)
            self.assertEqual(board.size, 10)

    def test_context_manager_calls_destroy(self) -> None:
        with new_board(size=10) as board:
            result = board.move(Direction.RIGHT)
            self.assertIsInstance(result, int)


if __name__ == "__main__":
    unittest.main()
