# Learn2Slither — Technical Documentation

This repository implements the Learn2Slither subject defined in the official specification file en.subject.pdf at the project root. The implementation follows the mandatory parts and provides several optional/bonus features. This document describes the system precisely, mapping requirements to the actual C and Python code.

---

## 1. Project Overview

- Goal: Train a snake agent via reinforcement learning (Q-learning) to navigate a board, grow to length ≥ 10, and survive as long as possible.
- RL approach: Tabular Q-learning with an ε-greedy exploration strategy. The agent updates Q-values from rewards returned by the environment.
- Technologies:
    - C: Core environment/board engine, compiled as a shared library (libboard.so).
    - Python: Agent, CLI, training loop, optional visualization.
    - Optional visualization: Pygame-based viewer and display helpers.
- Subject compliance: The board rules, snake vision constraints, actions, rewards, Q-learning model, and CLI behaviors align with en.subject.pdf. The agent only consumes state derived from the snake’s head vision; training can run headless; models can be saved/loaded and evaluated with learning disabled.

---

## 2. Project Architecture

- High-level components:
    - Environment/Board: Implemented in C under [c_src/board](c_src/board). Exposed to Python via ctypes.
    - Agent: Tabular Q-learning in [slither/agent.py](slither/agent.py).
    - CLI: Unified runner in [snake.py](snake.py); headless trainer in [train.py](train.py); manual play in [scripts/manual.py](scripts/manual.py).
    - Visualization: Pygame viewer in [slither/viewer.py](slither/viewer.py) using helpers in [display](display).
- C↔Python interaction:
    - The C library is built to [lib/libboard.so](lib/libboard.so) by [c_src/Makefile](c_src/Makefile).
    - Python loads it via [slither/core/_library.py](slither/core/_library.py) and exposes a wrapper [slither/core/board.py](slither/core/board.py) with methods like `reset()`, `move()`, `state`, `step()`.
    - Python reads reward constants directly from the C library ([slither/core/rewards.py](slither/core/rewards.py)) to ensure synchronization.
- Data flow:
    - Training loop: Board `reset()` → read `state` → Agent selects action → Board `step()` returns `(next_state, reward, done)` → Agent `update()` → until `done` or max steps.
    - Runtime visualization: Viewer renders board state each step, shows HUD/legend, and optionally waits for user input in step mode.

---

## 3. Detailed Mandatory Parts Documentation

### Part 1: Environment / Board

- Environment rules (per subject):
    - Board size: 10×10 cells.
    - Apples: Two green apples, one red apple placed randomly.
    - Snake: Starts length 3, placed randomly and contiguously.
    - Collisions: Hitting a wall or the snake’s own body → Game over. Length dropping to 0 → Game over.
    - Display: A graphical interface must show the board over time; speed must be configurable; step-by-step mode must exist.

- Implementation:
    - Board API and data types: [c_src/board/board.h](c_src/board/board.h)
        - Cell types: `EMPTY`, `WALL`, `SNAKE_HEAD`, `SNAKE_BODY`, `GREEN_APPLE`, `RED_APPLE`.
        - Directions: `UP`, `LEFT`, `DOWN`, `RIGHT`.
        - Actions (outcomes): `HIT_WALL`, `HIT_SELF`, `ATE_GREEN_APPLE`, `ATE_RED_APPLE`, `LENGTH_ZERO`.
        - Public functions: `board_create()`, `board_destroy()`, `board_reset()`, `board_move()`, query getters, `board_get_state()`, `board_print()`.
    - Board creation and reset: [c_src/board/board.c](c_src/board/board.c), [c_src/board/board_setup.c](c_src/board/board_setup.c)
        - `board_create(size)`: Validates size ∈ [8, 20]; otherwise defaults to 10. Allocates grid/snake buffers/apple storage.
        - `board_reset()`: Initializes an empty grid, resets counters, initializes the snake (length 3, contiguous, random placement), spawns apples.
    - Snake initialization: [c_src/board/board_helpers.c](c_src/board/board_helpers.c)
        - Places three contiguous segments; marks head (`SNAKE_HEAD`) and body (`SNAKE_BODY`). Sets length=3, head index, max length, score/moves=0.
    - Apples: [c_src/board/board_apples.c](c_src/board/board_apples.c)
        - Spawns apples on random empty cells; updates apple arrays and counts; removes and respawns apples upon consumption.
    - Movement and collisions: [c_src/board/board_move.c](c_src/board/board_move.c)
        - Resolves moves; detects wall/self collisions; applies growth/shrink on apples; enforces `LENGTH_ZERO` if snake shrinks below 1.
    - Board queries and printing: [c_src/board/board_query.c](c_src/board/board_query.c), [c_src/board/board_state.c](c_src/board/board_state.c)
        - `board_get_cell()` returns `WALL` for out-of-bounds queries.
        - `board_print()` outputs a text vision around the head (see Part 2).
    - Python wrapper: [slither/core/board.py](slither/core/board.py)
        - Provides high-level `GameBoard` with `reset()`, `move()`, `print_board()`, `state`, `step()`.
        - `step(direction)` returns `(next_state, reward, done)`, mapping `board_move()` results to rewards.

- Configurable parameters:
    - Board size argument via CLI (`-size`, default 10). In C, invalid sizes default to 10, and apple counts scale automatically with size.
    - Viewer FPS and step mode toggles; agent view overlay; HUD/legend visibility via panel.

### Part 2: State

- Subject constraint: The agent may only receive information visible from the snake head along four directions (UP, LEFT, DOWN, RIGHT). Providing more information incurs a penalty per subject (not used here).

- State definition and encoding:
    - The C engine encodes vision into a 12-bit integer via `board_get_state()` ([c_src/board/board_state.c](c_src/board/board_state.c)).
    - Each direction contributes 3 bits (encoded categories):
        - 0: Clear path to the wall (no immediate findings before danger).
        - 1: Danger adjacent (wall or body next cell).
        - 2: Danger nearby (distance 2–3).
        - 3: Green apple visible before any danger.
        - 4: Red apple visible before any danger.
        - 5: Body visible (not adjacent).
    - Bits layout: `state = (UP << 9) | (LEFT << 6) | (DOWN << 3) | (RIGHT << 0)`.

- Terminal output of vision:
    - `board_print()` prints vertical/horizontal lines of symbols from the head until the wall: `S` (body), `G` (green), `R` (red), `0` (empty), `W` (wall). See [c_src/board/board_state.c](c_src/board/board_state.c).
    - The Python CLI can also print immediate neighborhood and the chosen action via `-verbose`, using [slither/utils.py](slither/utils.py).

- Design decisions:
    - The encoded state strictly reflects line-of-sight categories relative to the head, satisfying the visibility constraint.
    - The representation is compact (12-bit) and agnostic to absolute board size; this supports model portability across sizes.

### Part 3: Action

- Allowed actions (subject): `UP`, `LEFT`, `DOWN`, `RIGHT` only.
- Representation:
    - C enum `t_direction` in [c_src/board/board.h](c_src/board/board.h).
    - Python indices 0..3 mapped via `ACTION_TO_DIRECTION` ([slither/utils.py](slither/utils.py)).
- Constraints:
    - No reverse or invalid actions beyond the four allowed directions. Invalid inputs to `board_move()` return `-1` and do not advance.
- Effects:
    - The move updates the environment (snake position, apples, collisions) and returns an action outcome that is later mapped to rewards.
- Action selection:
    - The agent calls `select_action(state, explore=learn)` with ε-greedy policy ([slither/agent.py](slither/agent.py)). No extra board information is used.

### Part 4: Rewards

- Reward function values (from [c_src/board/board.h](c_src/board/board.h)):
    - Eat green apple: `+10.0` → grow by 1 and respawn a green apple.
    - Eat red apple: `-10.0` → shrink by 1 (may cause `LENGTH_ZERO`).
    - Death (hit wall/self or zero length): `-50.0`.
    - Normal step: `-0.1` (encourages efficiency and discourages wandering).
- Reward usage:
    - Python imports these constants from the C library ([slither/core/rewards.py](slither/core/rewards.py)).
    - `GameBoard.step()` performs a move, converts the C outcome to the appropriate reward, returns `(next_state, reward, done)` ([slither/core/board.py](slither/core/board.py)).

### Part 5: Q-learning

- Algorithm:
    - Tabular Q-learning with Bellman updates ([slither/agent.py](slither/agent.py)).
    - Q-table keyed by state (int) with 4 action values (floats).
    - Update rule: $Q(s,a) \leftarrow Q(s,a) + \alpha \,[r + \gamma\,\max_a Q(s',a) - Q(s,a)]$.
- Parameters:
    - Learning rate `alpha` (default 0.1), discount `gamma` (0.95).
    - Exploration: ε-greedy (`epsilon`, `min_epsilon`, `epsilon_decay`).
    - Learning enable/disable: `-dontlearn` sets `learning_enabled=False`, also forces `epsilon=0.0` to evaluate without altering the model.
- Training loop:
    - Headless training in [train.py](train.py) and in [snake.py](snake.py) when `-visual off`.
    - Steps until game over or `--max-steps` limit, with per-episode epsilon decay.
- Model persistence:
    - JSON save/load via `save_model()/load_model()` ([slither/agent.py](slither/agent.py)). Models placed under [models](models). Example models provided: `qtable-001.json`, `qtable-010.json`, `qtable-100.json`, `qtable-10000.json`.
- Theory vs implementation:
    - Pure tabular Q-learning (as required); no neural networks or other models.

### Part 6: Technical Structure

- Codebase layout and responsibilities:
    - C engine: Board core in [c_src/board](c_src/board) (grid management, snake movement, collisions, apple spawning, state encoding, reward accessors).
    - Python core wrapper: [slither/core](slither/core) — loads `libboard.so`, defines types/constants ([slither/core/_types.py](slither/core/_types.py)), exposes `GameBoard` ([slither/core/board.py](slither/core/board.py)), retrieves rewards ([slither/core/rewards.py](slither/core/rewards.py)).
    - Agent: Q-learning in [slither/agent.py](slither/agent.py).
    - CLI: Unified runner [snake.py](snake.py) (subject-flags), headless trainer [train.py](train.py), manual play [scripts/manual.py](scripts/manual.py).
    - Visualization: Pygame viewer [slither/viewer.py](slither/viewer.py) with display helpers in [display](display) (HUD, grid, overlays, config panel, themes, fonts).
    - Tests: Python validation tests under [tests/validation](tests/validation) and a C test suite under [c_src/tests](c_src/tests).
- Build system and execution flow:
    - Build C library: `make lib` (calls [c_src/Makefile](c_src/Makefile)) → builds [lib/libboard.so](lib/libboard.so).
    - Python scripts assume libboard.so exists at import time (see [slither/core/_library.py](slither/core/_library.py)).
    - Entry points (via pyproject): `snake` (unified), `learn2slither-train` (train), `learn2slither-manual` (manual). The top-level [snake.py](snake.py) can also be run directly.
    - Dependencies: Optional `pygame` for visualization; `pytest` for Python tests.

---

## 4. Bonus Features

Implemented (and testable) bonuses from the subject:

- Variable board size:
    - Enabled via CLI `-size N` with validation in [snake.py](snake.py) and [scripts/manual.py](scripts/manual.py); C defaults to 10 when invalid ([c_src/board/board.c](c_src/board/board.c)).
    - Apple counts scale with size: `num_green_apples = 2 + (size - 10)/3`, `num_red_apples = 1 + (size - 10)/5` (see [c_src/board/board.c](c_src/board/board.c)).
    - Model compatibility: The 12-bit state encodes relative visibility, not absolute positions, so Q-tables remain usable across sizes.

- Advanced visualization:
    - Viewer with HUD, legend, pause/game-over overlays, splash screen, and a configuration panel ([slither/viewer.py](slither/viewer.py), [display](display)).
    - Step-by-step mode and agent-view overlay (visible cells along the head’s lines of sight) can be toggled.

- Headless training for speed:
    - `-visual off` or using [train.py](train.py) runs without display and suppresses terminal rendering; aligns with subject allowance to remove display during training.

---

## 5. How to Build and Run

### Build C library

```bash
make lib
```

### Create a Python environment and install optional tools

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
```

### Run unified CLI (subject examples)

```bash
# Train for 10 sessions and save a model, without visualization
./snake -sessions 10 -save models/10sess.json -visual off

# Evaluate a trained model with visualization and no learning
./snake -visual on -load models/qtable-100.json -dontlearn

# Run with visualization and defaults (size=10)
./snake -visual on -load models/qtable-1000.json
```

Additional options:

- Size: `-size 10` (default; accepts 8–20).
- FPS: `-fps 10`.
- Max steps per episode: `-max-steps 500`.
- Verbose vision output: `-verbose` (prints immediate head-neighbor vision and action to terminal).
- Step-by-step: `-step-by-step` (waits for input between moves).
- Disable learning: `-dontlearn`.

### Headless training

```bash
./snake -sessions 100 -visual off -save models/qtable-0100.json

# Alternatively
python train.py --sessions 100 --size 10 --save models/qtable-0100.json
```

### Manual play (optional)

```bash
learn2slither-manual --episodes 1 --size 10 --render step --verbose
# or run directly
python scripts/manual.py --episodes 1 --size 10 --render step --verbose
```

---

## 6. Results and Observations

- Training behavior:
    - With ε-greedy exploration and step penalty, the agent learns to prefer moves that lead to green apples and avoid immediate danger states.
    - Epsilon decay drives the policy from exploration to exploitation over episodes.
- Provided models:
    - Models in [models](models) demonstrate progressive training durations (e.g., 1, 10, 100, 10000 sessions). Load with `-dontlearn` to evaluate without altering Q-values.
- Visualization:
    - HUD and overlays help track length, steps, and episode progression; step mode supports interactive inspection.

Note: Exact performance (length/duration) depends on training time, random initialization, and hyperparameters; this repository avoids hardcoding specific outcome claims beyond the subject’s target (length ≥ 10).

---

## 7. Limitations and Possible Improvements

- Limitations:
    - Tabular Q-learning with a 12-bit state limits representation capacity; no memory of past decisions beyond the immediate state.
    - Apple counts scale with board size; while models remain compatible, strategy may need more episodes for larger boards.
    - Visualization depends on Pygame; headless mode is available for environments without GUI support.
- Possible improvements:
    - Reward shaping (e.g., small positive reward for moving toward green apples by heuristic) while respecting the visibility constraint.
    - Alternate exploration schedules or annealing strategies for faster convergence.
    - Logging and analytics (episode returns, length histograms) for deeper evaluation.
    - Optional integration tests to validate cross-size model portability quantitatively.

---

## Appendix: References and Files

- Subject: en.subject.pdf (mandatory requirements, constraints, and bonuses).
- Core C files:
    - [c_src/board/board.h](c_src/board/board.h) — public API, enums, rewards.
    - [c_src/board/board.c](c_src/board/board.c) — allocation and setup.
    - [c_src/board/board_move.c](c_src/board/board_move.c) — movement and collisions.
    - [c_src/board/board_state.c](c_src/board/board_state.c) — vision encoding, printing.
    - [c_src/board/board_apples.c](c_src/board/board_apples.c) — apple placement and management.
    - [c_src/board/board_helpers.c](c_src/board/board_helpers.c) — grid/snake initialization helpers.
    - [c_src/board/board_query.c](c_src/board/board_query.c) — getters.
    - [c_src/board/rewards.c](c_src/board/rewards.c) — reward accessors.
- Python core and CLI:
    - [slither/core/_library.py](slither/core/_library.py) — lib loader.
    - [slither/core/_types.py](slither/core/_types.py) — type constants.
    - [slither/core/board.py](slither/core/board.py) — Python wrapper, `step()`.
    - [slither/core/rewards.py](slither/core/rewards.py) — reward constants.
    - [slither/agent.py](slither/agent.py) — Q-learning.
    - [snake.py](snake.py) — unified CLI.
    - [train.py](train.py) — headless trainer.
    - [scripts/manual.py](scripts/manual.py) — manual controls.
- Visualization helpers: [display](display) (HUD, grid, overlays, panel, theme, fonts).
- Tests:
    - Python: [tests/validation](tests/validation).
    - C: [c_src/tests](c_src/tests).

---

## License

MIT License — see [LICENSE](LICENSE).

Subject — see [en.subject.pdf](en.subject.pdf).
