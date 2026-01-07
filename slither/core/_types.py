"""
Type Definitions and Constants

Defines all enums and type mappings for the Snake game engine.
"""


class BoardCell:
    """Board cell type constants."""

    EMPTY: int = 0
    WALL: int = 1
    SNAKE_HEAD: int = 2
    SNAKE_BODY: int = 3
    GREEN_APPLE: int = 4
    RED_APPLE: int = 5

    __slots__ = ()


class Direction:
    """Movement direction constants."""

    UP: int = 0
    LEFT: int = 1
    DOWN: int = 2
    RIGHT: int = 3

    __slots__ = ()


class Actions:
    """Action result constants from board_move()."""

    NORMAL_MOVE: int = 0
    HIT_WALL: int = 1
    HIT_SELF: int = 2
    ATE_GREEN_APPLE: int = 3
    ATE_RED_APPLE: int = 4
    LENGTH_ZERO: int = 5

    __slots__ = ()
