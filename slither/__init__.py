"""
Snake Game - Python/C Binding Module

This module provides Python bindings for the Snake game's C board engine,
enabling Python to interface with high-performance C code while maintaining
a Pythonic API.

It includes:
- Loading the C library
- Defining C function signatures
- A Python wrapper class for the C Board structure
"""

from .core import GameBoard, BoardCell, Direction, Actions

__version__ = "0.1.0"
__author__ = "Jhonata Pereira"
__all__ = ["GameBoard", "BoardCell", "Direction", "Actions"]

# Viewer is optional (requires pygame)
try:  # pragma: no cover - optional dependency
    from .viewer import Viewer, RenderInfo

    __all__.extend(["Viewer", "RenderInfo"])
except ImportError:
    Viewer = None  # type: ignore
    RenderInfo = None  # type: ignore
