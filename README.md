# 42-Learn2Slither
A 10x10 snake environment backed by a C board engine with Python bindings, a pygame viewer, and a manual gameplay loop suited for reinforcement-learning experiments.

## Overview
Learn2Slither combines a deterministic C implementation of the classic snake rules with a thin Python layer that exposes the board, rewards, and rendering helpers. The repository currently focuses on manual play so you can explore the environment, debug the engine, or plug in your own training workflow.

## Features
- Deterministic 10x10 board with two green apples (+1 length) and one red apple (-1 length) powered by the native sources in [c_src](c_src).
- Python bindings in [slither/core](slither/core) that expose `GameBoard`, `Direction`, `Actions`, and reward constants for scripting or experimentation.
- Configurable reward and console helpers in [slither/utils.py](slither/utils.py) for inspecting the snake vision grid and summarizing episodes.
- Modular rendering helpers under [display](display) covering themes, fonts, HUD, overlays, and the runtime config panel.
- Pygame viewer in [slither/viewer.py](slither/viewer.py) with splash screen, HUD, legend, manual keyboard controls (arrows to move, `Q`/`Esc` to quit), and an in-game display panel (`C`) for tweaking themes and layout.
- Manual gameplay CLI in [scripts/manual.py](scripts/manual.py) that wires the board, viewer, and console helpers together for one or many episodes.
- Validation tests under [tests/validation](tests/validation) to exercise board creation, movement edges, rewards, and printed output sequences.

## Project Layout
- [Makefile](Makefile): wraps the `c_src` build, clean, and test targets.
- [c_src](c_src): C implementation of the board state, apple placement, and movement rules.
- [slither](slither): Python package containing the ctypes bridge, rewards, viewer, and utilities.
- [display](display): pure-Python rendering helpers (themes, HUD, config panel) consumed by the viewer.
- [scripts](scripts): entry points such as the manual gameplay loop.
- [tests](tests): Python validation tests (pytest-compatible) for the exposed API.
- [project-requirements.md](project-requirements.md): up-to-date compliance checklist for the original project brief.

## Setup
Requirements: Python 3.13+, a C compiler that can build the shared library, and pygame for visualization.

### 1. Build the native board
```bash
make lib
```
This compiles the shared library and drops it into [lib](lib) for the Python bindings to load.

### 2. Install Python dependencies
```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
```
The `dev` extra installs `pygame`, `pytest`, and `numpy`. If you prefer pip without extras, make sure `pygame>=2.5` is installed manually before launching the viewer.

## Manual Gameplay
Run the manual loop from the repository root after building the library and installing dependencies:
```bash
python -m scripts.manual --episodes 3 --render slow --fps 12
```
- Arrow keys select directions, `Q`/`Esc` exits, `C` toggles the display panel, and you can request random moves by running without the viewer (`--render none`).
- The HUD shows per-episode stats (length, score, apples eaten) while the console can display the snake "vision" grid via `--verbose`.
- The display panel lets you cycle themes, resize cells/legend, and toggle HUD/legend/grid lines on the fly.

### CLI options
| Flag | Default | Purpose |
|------|---------|---------|
| `--episodes` | `1` | Number of episodes to run before exiting.
| `--max-steps` | `500` | Upper bound on steps per episode.
| `--render` | `step` | Viewer mode: `none`, `slow`, `fast`, or `step`.
| `--fps` | `10` | Target FPS in slow/fast modes (step mode waits for input).
| `--seed` | `None` | Optional RNG seed for reproducible apple placement.
| `--verbose` / `-v` | `False` | Print the snake vision grid and rewards to stdout.
| `--keep-open` | `False` | Leave the viewer window up after the last episode.
| `--size` | `10` | Board dimension (8–20) for larger or smaller arenas.

### Common run recipes
| Command | Purpose |
|---------|---------|
| `python -m scripts.manual --render step --episodes 1` | Interactive play with step-by-step confirmation (default board size).
| `python -m scripts.manual --render slow --fps 15 --episodes 3` | Smooth real-time playback at 15 FPS for multiple episodes.
| `python -m scripts.manual --render fast --fps 45 --episodes 20` | High-speed autoplay useful for burn-in tests.
| `python -m scripts.manual --render none --episodes 5 --verbose` | Headless run that logs the agent’s 12-bit vision and rewards to the console.
| `python -m scripts.manual --size 15 --render step --episodes 2` | Larger 15×15 arena to demonstrate the variable board-size bonus in step mode.
| `python -m scripts.manual --size 8 --render slow --keep-open` | Compact grid for quick demos; keeps the viewer open after finishing.

## Development
### C-side validation
```bash
make test      # run the C unit tests
make valgrind  # run them under Valgrind for leak checking
```
### Python validation tests
```bash
pytest tests/validation
```
These tests cover board initialization, reward assignments, and representative move sequences to ensure the bindings stay in sync with the C behavior.

## References
- [YouTube: Introduction to Reinforcement Learning](https://www.youtube.com/watch?v=JgvyzIkgxF0)
- [YouTube: A equação de Bellmann](https://www.youtube.com/watch?v=cOy0sUTouyo)
- [YouTube: Equa%C3%A7%C3%A3o de Bellman](https://www.youtube.com/watch?v=cOy0sUTouyo)
- [YouTube: A ideia que tornou a Inteligência Artificial possível](https://www.youtube.com/watch?v=mBqfY_TX_8o)
