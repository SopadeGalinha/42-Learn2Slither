"""Output flow validation tests."""
import unittest

from tests.validation.helpers import Direction, new_board

DECISION_LABELS = {
    Direction.UP: "UP",
    Direction.DOWN: "DOWN",
    Direction.LEFT: "LEFT",
    Direction.RIGHT: "RIGHT",
}


class TestOutputFlow(unittest.TestCase):
    """Ensure we can show board snapshots around agent decisions."""

    def test_print_sequence_for_two_moves(self) -> None:
        board = new_board()
        board.reset()
        decisions = [Direction.RIGHT, Direction.DOWN]
        initial_moves = board.moves

        print()
        board.print_board()

        for decision in decisions:
            label = DECISION_LABELS[decision]
            print()
            print(label)
            move_result = board.move(decision)
            self.assertNotEqual(move_result, -1, "Move should be valid")
            board.print_board()

        self.assertEqual(board.moves, initial_moves + len(decisions))


if __name__ == "__main__":
    unittest.main()
