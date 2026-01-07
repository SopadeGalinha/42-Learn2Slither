"""
Core module: C library wrapper and board interface.

Provides low-level access to the C board engine through ctypes.
"""

from ._library import board_lib
from ._types import Actions, BoardCell, Direction
from .board import GameBoard
from .rewards import (
    REWARD_DEATH,
    REWARD_GREEN_APPLE,
    REWARD_RED_APPLE,
    REWARD_STEP,
)

__all__ = [
    "board_lib",
    "Actions",
    "BoardCell",
    "Direction",
    "GameBoard",
    "REWARD_DEATH",
    "REWARD_GREEN_APPLE",
    "REWARD_RED_APPLE",
    "REWARD_STEP",
]
