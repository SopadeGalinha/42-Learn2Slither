"""Run validation tests.

Use ``python -m tests.validation``.
"""
import unittest
from pathlib import Path


def main() -> None:
    test_root = Path(__file__).resolve().parent
    suite = unittest.defaultTestLoader.discover(str(test_root))
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    if not result.wasSuccessful():
        raise SystemExit(1)


if __name__ == "__main__":
    main()
