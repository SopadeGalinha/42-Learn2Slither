# Tooling and Packaging Notes

This document summarizes the developer-facing tooling that complements the Learn2Slither project.

## Editable installs and CLI entry point
- The project now declares a console script named `learn2slither-manual` (see `pyproject.toml`).
- After creating a virtual environment, run `pip install -e .[dev]` to install the `slither` package and register the CLI entry point.
- You can now launch the manual viewer with `learn2slither-manual --render step --size 12` without relying on `PYTHONPATH` tricks or Poetry.

## Pre-commit automation
- `.pre-commit-config.yaml` wires common quality gates:
  - `pre-commit-hooks` for whitespace and large-file protection.
  - `flake8` for Python linting.
  - `clang-format` (LLVM style) for the C sources under `c_src/`.
  - Two local hooks that run `pytest tests/validation` and `make test`.
- Install hooks once per clone: `pre-commit install` (after the editable install above).
- From then on, `pre-commit run --all-files` mirrors the CI gates locally, catching style or test failures before pushing.

These steps keep both the Python package and the native board implementation aligned, making it easier to integrate future agents or additional tooling.
