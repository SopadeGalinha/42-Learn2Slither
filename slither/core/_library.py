"""
C Library Loading Module

Handles loading the compiled C board engine library (libboard.so) with
proper error handling and path resolution.
"""

import ctypes
from pathlib import Path


def load_board_library() -> ctypes.CDLL:
    """
    Load the compiled C board library.

    Returns:
        ctypes.CDLL: Loaded library object

    Raises:
        RuntimeError: If libboard.so is not found
    """
    lib_path = Path(__file__).parent.parent.parent / "lib" / "libboard.so"

    if not lib_path.exists():
        raise RuntimeError(
            f"libboard.so not found at {lib_path}\n"
            "Execute 'make lib' first to compile the C library"
        )

    return ctypes.CDLL(str(lib_path))


# Load library once at module import
board_lib = load_board_library()
