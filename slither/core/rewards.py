"""
Reward constants mirrored from the C board engine.
Values are fetched via ctypes from the compiled library.
This keeps the Python and C implementations in sync.
"""

from ctypes import c_float

from ._library import board_lib

# Configure C function signatures for reward accessors
board_lib.board_get_reward_green_apple.argtypes = []
board_lib.board_get_reward_green_apple.restype = c_float

board_lib.board_get_reward_red_apple.argtypes = []
board_lib.board_get_reward_red_apple.restype = c_float

board_lib.board_get_reward_death.argtypes = []
board_lib.board_get_reward_death.restype = c_float

board_lib.board_get_reward_step.argtypes = []
board_lib.board_get_reward_step.restype = c_float

# Load constants once from the C library
REWARD_GREEN_APPLE: float = float(board_lib.board_get_reward_green_apple())
REWARD_RED_APPLE: float = float(board_lib.board_get_reward_red_apple())
REWARD_DEATH: float = float(board_lib.board_get_reward_death())
REWARD_STEP: float = float(board_lib.board_get_reward_step())

__all__ = [
    "REWARD_GREEN_APPLE",
    "REWARD_RED_APPLE",
    "REWARD_DEATH",
    "REWARD_STEP",
]
