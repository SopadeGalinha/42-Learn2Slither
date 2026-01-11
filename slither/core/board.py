"""
GameBoard Python Wrapper

Provides a high-level Python interface to the C board engine,
handling memory management and type conversions.
"""

from ctypes import c_void_p, c_int, c_bool

from ._library import board_lib
from ._types import Actions
from .rewards import (
    REWARD_DEATH,
    REWARD_GREEN_APPLE,
    REWARD_RED_APPLE,
    REWARD_STEP,
)


# Define C function signatures
def _setup_c_functions() -> None:
    """Configure C function signatures and return types."""

    # Board* board_create(int size)
    board_lib.board_create.argtypes = [c_int]
    board_lib.board_create.restype = c_void_p

    # void board_destroy(Board* board)
    board_lib.board_destroy.argtypes = [c_void_p]
    board_lib.board_destroy.restype = None

    # void board_reset(Board* board)
    board_lib.board_reset.argtypes = [c_void_p]
    board_lib.board_reset.restype = None

    # int board_move(Board* board, Direction action)
    board_lib.board_move.argtypes = [c_void_p, c_int]
    board_lib.board_move.restype = c_int

    # bool board_is_game_over(const Board* board)
    board_lib.board_is_game_over.argtypes = [c_void_p]
    board_lib.board_is_game_over.restype = c_bool

    # int board_get_score(const Board* board)
    board_lib.board_get_score.argtypes = [c_void_p]
    board_lib.board_get_score.restype = c_int

    # int board_get_length(const Board* board)
    board_lib.board_get_length.argtypes = [c_void_p]
    board_lib.board_get_length.restype = c_int

    # int board_get_max_length(const Board* board)
    board_lib.board_get_max_length.argtypes = [c_void_p]
    board_lib.board_get_max_length.restype = c_int

    # int board_get_moves(const Board* board)
    board_lib.board_get_moves.argtypes = [c_void_p]
    board_lib.board_get_moves.restype = c_int

    # unsigned short board_get_state(const Board* board)
    board_lib.board_get_state.argtypes = [c_void_p]
    board_lib.board_get_state.restype = c_int

    # BoardCell board_get_cell(const Board* board, int x, int y)
    board_lib.board_get_cell.argtypes = [c_void_p, c_int, c_int]
    board_lib.board_get_cell.restype = c_int

    # int board_get_size(const Board* board)
    board_lib.board_get_size.argtypes = [c_void_p]
    board_lib.board_get_size.restype = c_int

    # void board_print(const Board* board)
    board_lib.board_print.argtypes = [c_void_p]
    board_lib.board_print.restype = None


_setup_c_functions()


class GameBoard:
    """
    Python wrapper for the C Board structure.

    Provides a Pythonic interface to the C board engine while maintaining
    proper memory management and error handling.

    Attributes:
        _board: Opaque pointer to C Board struct

    Example:
        >>> board = GameBoard()
        >>> board.print_board()
        >>> board.move(Direction.RIGHT)
        >>> del board  # Automatic cleanup
    """

    __slots__ = ("_board",)

    def __init__(self, size: int = 10) -> None:
        """
        Create a new game board.

        Initializes a board with:
        - Configurable size (8-20, default 10)
        - Dynamic apple count based on size
        - Snake with 3 segments
        - Empty game state

        Args:
            size: Board size (8-20, defaults to 10 if invalid)

        Raises:
            MemoryError: If board allocation fails
        """
        self._board = board_lib.board_create(size)
        if not self._board:
            raise MemoryError("Failed to allocate memory for board")

    def __del__(self) -> None:
        """Free memory when board is destroyed."""
        if hasattr(self, "_board") and self._board:
            board_lib.board_destroy(self._board)
            self._board = None

    def __repr__(self) -> str:
        """Return string representation of GameBoard."""
        ptr_value = self._board or 0
        return f"<GameBoard at {hex(ptr_value)}>"

    def __enter__(self) -> "GameBoard":
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Context manager exit with automatic cleanup."""
        self.__del__()

    def reset(self) -> None:
        """Reset the board to initial state."""
        board_lib.board_reset(self._board)

    def move(self, direction: int) -> int:
        """
        Move the snake in the given direction.

        Args:
            direction: Direction enum value (UP, LEFT, DOWN, RIGHT)

        Returns:
            int: Action result code (see Actions enum)
        """
        return board_lib.board_move(self._board, direction)

    def print_board(self) -> None:
        """
        Display the board to stdout.

        Shows the game board using box drawing characters.
        Prints current game statistics (score, length, moves).
        """
        board_lib.board_print(self._board)

    @property
    def is_game_over(self) -> bool:
        """Check if the game is over."""
        return board_lib.board_is_game_over(self._board)

    @property
    def score(self) -> int:
        """Get the current score."""
        return board_lib.board_get_score(self._board)

    @property
    def length(self) -> int:
        """Get the current snake length."""
        return board_lib.board_get_length(self._board)

    @property
    def max_length(self) -> int:
        """Get the maximum length reached."""
        return board_lib.board_get_max_length(self._board)

    @property
    def moves(self) -> int:
        """Get the number of moves made."""
        return board_lib.board_get_moves(self._board)

    @property
    def state(self) -> int:
        """
        Get the current board state (12-bit encoding).

        Returns:
            int: 12-bit state representing neighboring cells
        """
        return board_lib.board_get_state(self._board)

    @property
    def size(self) -> int:
        """Get board dimension (actual size)."""
        size = board_lib.board_get_size(self._board)
        if size < 0:
            raise RuntimeError("Board pointer is null; size unavailable")
        return size

    def get_cell(self, x: int, y: int) -> int:
        """Get the cell value at (x, y)."""
        return board_lib.board_get_cell(self._board, x, y)

    def step(self, direction: int) -> tuple[int, float, bool]:
        """
        Perform one action in the environment.

        Args:
            direction: Direction enum value (UP, LEFT, DOWN, RIGHT)

        Returns:
            tuple[int, float, bool]: (next_state, reward, done)
        """
        result = board_lib.board_move(self._board, direction)

        if result == Actions.ATE_GREEN_APPLE:
            reward = REWARD_GREEN_APPLE
        elif result == Actions.ATE_RED_APPLE:
            reward = REWARD_RED_APPLE
        elif result in (
            Actions.HIT_WALL,
            Actions.HIT_SELF,
            Actions.LENGTH_ZERO,
        ):
            reward = REWARD_DEATH
        else:
            reward = REWARD_STEP

        done = bool(board_lib.board_is_game_over(self._board))
        state = board_lib.board_get_state(self._board)
        return state, reward, done
