# Learn2Slither

A reinforcement learning project where a snake learns to navigate a 10×10 grid, eat apples, and survive through trial and error using Q-learning.

---

## Table of Contents

1. [Overview](#overview)
2. [Quick Start](#quick-start)
3. [Project Structure](#project-structure)
4. [Mandatory Parts](#mandatory-parts)
   - [Part 1: Environment/Board](#part-1-environmentboard)
   - [Part 2: State (Snake Vision)](#part-2-state-snake-vision)
   - [Part 3: Action](#part-3-action)
   - [Part 4: Rewards](#part-4-rewards)
   - [Part 5: Q-Learning](#part-5-q-learning)
   - [Part 6: Technical Structure](#part-6-technical-structure)
5. [Bonus Features](#bonus-features)
6. [CLI Reference](#cli-reference)
7. [Setup & Installation](#setup--installation)
8. [Training Guide](#training-guide)
9. [Development & Testing](#development--testing)

---

## Overview

Learn2Slither implements a classic snake game where an AI agent learns optimal behavior through **reinforcement learning**. The snake starts with no knowledge and, through thousands of training episodes, learns to:

- Avoid walls and its own body
- Seek out green apples (which increase its length)
- Avoid red apples (which decrease its length)
- Survive as long as possible while maximizing its score

The project uses **Q-learning**, a model-free reinforcement learning algorithm that learns the value of actions in different states without needing a model of the environment.

### Key Results

After training for 10,000 episodes, the agent achieves:
- **Maximum length: 35+** (goal is ≥10)
- **Average reward: +138** per episode
- **Survival: 300-400+ steps** per episode

---

## Quick Start

```bash
# 1. Build the C library
make lib

# 2. Set up Python environment
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]

# 3. Train for 100 sessions
./snake -sessions 100 -save models/my-model.json -visual off

# 4. Watch the trained agent play
./snake -load models/qtable-10000.json -visual on -dontlearn

# 5. Step-by-step evaluation
./snake -load models/qtable-10000.json -visual on -dontlearn -step-by-step
```

---

## Project Structure

```
learn2Slither/
├── snake.py              # Unified CLI entry point
├── snake                  # Shell wrapper for ./snake execution
├── train.py              # Headless training script
├── Makefile              # Build automation
│
├── c_src/                # C implementation of the game engine
│   └── board/
│       ├── board.c       # Main board logic
│       ├── board_state.c # State encoding (snake vision)
│       ├── board_move.c  # Movement and collision detection
│       ├── rewards.c     # Reward constants
│       └── board.h       # Public API header
│
├── slither/              # Python package
│   ├── agent.py          # Q-learning agent implementation
│   ├── viewer.py         # Pygame visualization
│   ├── utils.py          # Helper functions
│   └── core/
│       ├── board.py      # Python wrapper for C board
│       ├── rewards.py    # Reward constants (from C)
│       └── _library.py   # ctypes bindings
│
├── display/              # Rendering components
│   ├── grid.py           # Board rendering
│   ├── hud.py            # Head-up display
│   ├── overlays.py       # Game over, pause screens
│   └── panel.py          # Configuration panel
│
├── models/               # Saved Q-tables
│   ├── qtable-001.json   # 1 training session
│   ├── qtable-010.json   # 10 training sessions
│   ├── qtable-100.json   # 100 training sessions
│   └── qtable-10000.json # 10,000 sessions (best model)
│
└── tests/                # Validation tests
    └── validation/       # pytest test suites
```

---

## Mandatory Parts

### Part 1: Environment/Board

The environment is a 10×10 grid where the snake moves and interacts with apples.

#### Rules

| Rule | Description |
|------|-------------|
| **Board Size** | 10×10 cells (configurable 8-20 for bonus) |
| **Snake Start** | 3 cells, placed randomly and contiguously |
| **Green Apples** | 2 on the board; eating one adds +1 length |
| **Red Apple** | 1 on the board; eating one removes -1 length |
| **Wall Collision** | Game over |
| **Self Collision** | Game over (snake hits its own body) |
| **Zero Length** | Game over (ate too many red apples) |

#### Implementation

The board is implemented in C for performance ([c_src/board/board.c](c_src/board/board.c)):

```c
// Board structure (simplified)
typedef struct s_board {
    t_board_cell **grid;    // 2D array of cells
    t_snake       snake;    // Snake position and length
    int           size;     // Board dimension (10)
    bool          game_over;
    int           score;
    t_apple      *apples;   // Apple positions
} t_board;

// Cell types
typedef enum e_board_cell {
    EMPTY = 0,
    WALL = 1,
    SNAKE_HEAD = 2,
    SNAKE_BODY = 3,
    GREEN_APPLE = 4,
    RED_APPLE = 5
} t_board_cell;
```

Python accesses the board through ctypes bindings ([slither/core/board.py](slither/core/board.py)):

```python
class GameBoard:
    def __init__(self, size: int = 10):
        self._board = board_lib.board_create(size)

    def step(self, direction: int) -> tuple[int, float, bool]:
        """Execute one move, return (next_state, reward, done)"""
        result = board_lib.board_move(self._board, direction)
        # ... compute reward based on result
        return state, reward, done
```

#### Graphical Interface

The viewer ([slither/viewer.py](slither/viewer.py)) displays the board using Pygame:

- **Real-time rendering** at configurable FPS
- **Step-by-step mode** for debugging
- **HUD** showing episode stats (length, score, steps)
- **Configuration panel** (press `C`) for themes and settings

---

### Part 2: State (Snake Vision)

The snake can only "see" in 4 directions from its head. This limited vision is what makes the learning problem challenging.

#### How Vision Works

From the snake's head, we scan in each direction (UP, LEFT, DOWN, RIGHT) until we hit a wall. For each direction, we encode what the snake "sees first" into 3 bits:

```
        UP
        |
  LEFT--H--RIGHT
        |
       DOWN
```

#### State Encoding (12 bits total)

Each direction is encoded as 3 bits (values 0-7), giving us 12 bits total:

```
State = (UP << 9) | (LEFT << 6) | (DOWN << 3) | (RIGHT << 0)
```

The 3-bit values represent:

| Value | Meaning |
|-------|---------|
| 0 | Clear path to distant wall |
| 1 | **Danger adjacent** (wall or body in next cell) |
| 2 | Danger nearby (2-3 cells away) |
| 3 | **Green apple visible** (before any danger) |
| 4 | **Red apple visible** (before any danger) |
| 5 | Body visible (not adjacent) |

#### Implementation

The `scan_direction` function in [c_src/board/board_state.c](c_src/board/board_state.c):

```c
static unsigned short scan_direction(const t_board *board,
    int x, int y, int dx, int dy)
{
    int dist = 0;
    int first_danger = -1, first_green = -1, first_red = -1;

    while (1) {
        x += dx;  // Move in direction
        y += dy;
        dist++;

        t_board_cell cell = check_cell(board, x, y);

        if (cell == WALL) {
            if (first_danger < 0) first_danger = dist;
            break;
        }
        if (cell == SNAKE_BODY && first_danger < 0)
            first_danger = dist;
        if (cell == GREEN_APPLE && first_green < 0)
            first_green = dist;
        if (cell == RED_APPLE && first_red < 0)
            first_red = dist;
    }

    // Priority: immediate danger > apple > distant danger
    if (first_danger == 1) return 1;  // Adjacent danger!
    if (first_green > 0 && first_green < first_danger) return 3;
    if (first_red > 0 && first_red < first_danger) return 4;
    if (first_danger <= 3) return 2;  // Nearby danger
    return 0;  // Clear
}
```

#### Terminal Output

When running with `-verbose`, the vision is displayed:

```
      W          <- Wall visible above
      |
  0 - H - G      <- Empty left, Green apple right
      |
      S          <- Snake body below

Action: RIGHT  Reward: +10.0
```

---

### Part 3: Action

The agent can perform exactly 4 actions:

| Action | Value | Direction |
|--------|-------|-----------|
| UP | 0 | Move head up (y - 1) |
| LEFT | 1 | Move head left (x - 1) |
| DOWN | 2 | Move head down (y + 1) |
| RIGHT | 3 | Move head right (x + 1) |

#### Implementation

Actions are defined as an enum in C ([c_src/board/board.h](c_src/board/board.h)):

```c
typedef enum e_direction {
    UP = 0,
    LEFT = 1,
    DOWN = 2,
    RIGHT = 3
} t_direction;
```

The agent selects actions based solely on the current state (12-bit vision). It has no knowledge of:
- Absolute position on the board
- Apple positions beyond line-of-sight
- Previous moves or history

#### Action Selection

In [slither/agent.py](slither/agent.py), the agent selects actions using ε-greedy policy:

```python
def select_action(self, state: int, explore: bool = True) -> int:
    # During training, sometimes pick random action (exploration)
    if explore and random.random() < self.epsilon:
        return random.randrange(4)  # Random action

    # Otherwise, pick the best known action (exploitation)
    return self.best_action(state)

def best_action(self, state: int) -> int:
    values = self.q_table[state]  # [Q_up, Q_left, Q_down, Q_right]
    return values.index(max(values))
```

---

### Part 4: Rewards

Rewards provide feedback to the agent after each action. The agent's goal is to maximize cumulative reward over time.

#### Reward Values

| Event | Reward | Rationale |
|-------|--------|-----------|
| Eat green apple | **+10.0** | Strong positive signal for growth |
| Eat red apple | **-10.0** | Negative signal to avoid |
| Game over (death) | **-50.0** | Strong penalty for dying |
| Normal step | **-0.1** | Small penalty to encourage efficiency |

#### Implementation

Rewards are defined in C ([c_src/board/board.h](c_src/board/board.h)):

```c
#define REWARD_GREEN_APPLE  10.0f
#define REWARD_RED_APPLE   -10.0f
#define REWARD_DEATH       -50.0f
#define REWARD_STEP        -0.1f
```

Python fetches these values via ctypes to stay synchronized ([slither/core/rewards.py](slither/core/rewards.py)):

```python
REWARD_GREEN_APPLE = float(board_lib.board_get_reward_green_apple())
REWARD_RED_APPLE = float(board_lib.board_get_reward_red_apple())
REWARD_DEATH = float(board_lib.board_get_reward_death())
REWARD_STEP = float(board_lib.board_get_reward_step())
```

#### Why These Values?

- **+10 for green**: Large enough to overcome many -0.1 step penalties
- **-10 for red**: Equal magnitude to green, making them opposite goals
- **-50 for death**: Very strong penalty (5x apple value) to prioritize survival
- **-0.1 per step**: Prevents infinite loops; encourages finding apples quickly

---

### Part 5: Q-Learning

Q-learning is the algorithm that enables the snake to learn from experience without any pre-programmed knowledge.

#### What is Q-Learning?

Q-learning maintains a table of **Q-values** that estimate "how good" each action is in each state:

```
Q(state, action) = Expected total future reward if we take this action
```

The agent always tries to pick the action with the highest Q-value.

#### The Q-Table

The Q-table is a dictionary mapping states to action values:

```python
q_table = {
    state_1: [Q_up, Q_left, Q_down, Q_right],
    state_2: [Q_up, Q_left, Q_down, Q_right],
    ...
}
```

With 12-bit states, there are up to 4,096 possible states, each with 4 action values.

#### Learning Process (Bellman Update)

After each action, we update the Q-value using the **Bellman equation**:

```
Q(s, a) ← Q(s, a) + α × [reward + γ × max(Q(s')) - Q(s, a)]
```

Where:
- **s** = current state
- **a** = action taken
- **s'** = next state after action
- **α (alpha)** = learning rate (0.1) - how fast to update
- **γ (gamma)** = discount factor (0.95) - importance of future rewards
- **reward** = immediate reward received

#### Implementation

In [slither/agent.py](slither/agent.py):

```python
def update(self, state, action, reward, next_state, done):
    if not self.learning_enabled:
        return

    # Current Q-value estimate
    current = self.q_table[state][action]

    # Target: reward + discounted future value
    if done:
        target = reward  # No future if game over
    else:
        target = reward + self.gamma * max(self.q_table[next_state])

    # Update Q-value towards target
    self.q_table[state][action] = current + self.alpha * (target - current)
```

#### Exploration vs Exploitation

The agent must balance:
- **Exploitation**: Using what it already knows (picking best action)
- **Exploration**: Trying new things (random actions)

We use **ε-greedy** policy:
- With probability ε: pick random action
- With probability 1-ε: pick best action

ε starts at 1.0 (100% random) and decays over time:

```python
def decay_epsilon(self):
    self.epsilon = max(self.min_epsilon, self.epsilon * self.epsilon_decay)
```

After 10,000 episodes with decay=0.9995, ε reaches ~0.01 (1% random).

#### Model Persistence

Models are saved as JSON files:

```json
{
  "alpha": 0.1,
  "gamma": 0.95,
  "epsilon": 0.01,
  "q_table": {
    "1536": [-48.6, -0.1, -0.1, -0.2],
    "192": [-0.1, -38.5, -0.08, -0.1],
    ...
  }
}
```

---

### Part 6: Technical Structure

The project follows a modular architecture separating concerns:

```
┌─────────────────────────────────────────────────────────┐
│                    snake.py (CLI)                       │
│         Unified entry point with all flags              │
└─────────────────────────────────────────────────────────┘
                           │
          ┌────────────────┼────────────────┐
          ▼                ▼                ▼
┌────────────────┐ ┌──────────────┐ ┌─────────────────┐
│ QLearningAgent │ │  GameBoard   │ │     Viewer      │
│ (slither/agent)│ │(slither/core)│ │ (slither/viewer)│
│                │ │              │ │                 │
│• Q-table       │ │ • State      │ │ • Pygame render │
│• ε-greedy      │ │ • Actions    │ │ • HUD/overlays  │
│• Bellman update│ │ • Rewards    │ │ • Config panel  │
│• JSON save/load│ │              │ │                 │
└────────────────┘ └──────────────┘ └─────────────────┘
                           │
                           ▼
              ┌─────────────────────────┐
              │    C Board Engine       │
              │    (c_src/board/)       │
              │                         │
              │ • Grid management       │
              │ • Snake movement        │
              │ • Collision detection   │
              │ • State encoding        │
              │ • Apple spawning        │
              └─────────────────────────┘
```

#### Module Communication

1. **CLI → Agent**: Creates agent with hyperparameters, loads/saves models
2. **CLI → Board**: Creates board, calls `step()` for each action
3. **Agent → Board**: Agent receives state from board, selects action
4. **Board → Agent**: Board returns (next_state, reward, done) after each step
5. **CLI → Viewer**: Passes board state for rendering
6. **Viewer → CLI**: Returns user input (keyboard) in visual mode

#### Key Files

| File | Purpose |
|------|---------|
| `snake.py` | Main CLI matching subject specification |
| `slither/agent.py` | Q-learning implementation |
| `slither/core/board.py` | Python wrapper for C board |
| `c_src/board/board_state.c` | State encoding (12-bit vision) |
| `c_src/board/board_move.c` | Movement and collision logic |
| `slither/viewer.py` | Pygame visualization |

---

## Bonus Features

### Variable Board Size

The board size can be changed from 8×8 to 20×20:

```bash
./snake -size 15 -sessions 100 -visual on
```

The same trained model works on any board size because the state encoding is relative to the snake's head, not absolute positions.

### Advanced Visual Display

- **Theme cycling**: Press `C` to open config panel
- **HUD**: Episode number, score, length, steps
- **Legend**: Color key for all cell types
- **Splash screen**: Title and instructions on launch
- **Game over overlay**: Final stats with restart option

### High Length Achievement

The trained model consistently achieves:
- Length 15+ in most episodes
- Length 25+ frequently
- Length 35+ occasionally (record: 42)

---

## CLI Reference

### Main Entry Point (`./snake`)

```bash
./snake [options]
```

| Flag | Default | Description |
|------|---------|-------------|
| `-sessions N` | 1 | Number of training episodes |
| `-visual on/off` | on | Enable/disable graphical display |
| `-load PATH` | None | Load model from file |
| `-save PATH` | None | Save model to file |
| `-dontlearn` | False | Disable Q-table updates (evaluation mode) |
| `-step-by-step` | False | Wait for keypress between moves |
| `-size N` | 10 | Board dimension (8-20) |
| `-fps N` | 10 | Frames per second |
| `-max-steps N` | 500 | Maximum steps per episode |
| `-verbose` | False | Print vision to terminal |
| `-alpha F` | 0.1 | Learning rate |
| `-gamma F` | 0.95 | Discount factor |
| `-epsilon F` | 1.0 | Initial exploration rate |
| `-min-epsilon F` | 0.05 | Minimum exploration rate |
| `-epsilon-decay F` | 0.995 | Exploration decay rate |

### Examples

```bash
# Train new model
./snake -sessions 10000 -visual off -save models/trained.json

# Evaluate existing model
./snake -load models/qtable-10000.json -sessions 20 -dontlearn -visual off

# Watch trained agent
./snake -load models/qtable-10000.json -visual on -dontlearn -fps 15

# Debug step-by-step with vision output
./snake -load models/qtable-10000.json -visual on -dontlearn -step-by-step -verbose
```

---

## Setup & Installation

### Requirements

- Python 3.13+
- C compiler (gcc/clang)
- pygame 2.5+

### Build Steps

```bash
# Clone repository
git clone <repository-url>
cd learn2Slither

# Build C library
make lib

# Create virtual environment
python -m venv .venv
source .venv/bin/activate

# Install Python package
pip install -e .[dev]

# Verify installation
./snake -sessions 1 -visual off
```

---

## Training Guide

### Recommended Training Procedure

```bash
# Start with 10,000 episodes (takes ~2 minutes)
./snake -sessions 10000 \
        -visual off \
        -epsilon-decay 0.9995 \
        -min-epsilon 0.01 \
        -alpha 0.2 \
        -save models/qtable-10000.json

# Evaluate the result
./snake -load models/qtable-10000.json \
        -sessions 20 \
        -dontlearn \
        -visual off
```

### Expected Output

```
Episode 9998 - steps=235 reward=108.3 length=21 max_length=21 epsilon=0.010
Episode 9999 - steps=289 reward=143.8 length=25 max_length=25 epsilon=0.010
Episode 10000 - steps=143 reward=107.9 length=20 max_length=20 epsilon=0.010

Game over, max length = 42, max duration = 500
Average reward: 138.58
Sessions completed: 10000
Save learning state in models/qtable-10000.json
```

### Hyperparameter Tuning

| Parameter | Effect of Increasing |
|-----------|---------------------|
| `alpha` (0.1-0.3) | Faster learning, but less stable |
| `gamma` (0.9-0.99) | More weight on future rewards |
| `epsilon-decay` (0.999-0.9999) | Slower exploration decay |
| `min-epsilon` (0.01-0.1) | More random actions after training |

---

## Development & Testing

### Run Tests

```bash
# Python tests
pytest tests/validation/ -v

# C tests with memory check
make test
```

### Code Style

```bash
# Python (flake8)
flake8 slither/ scripts/ snake.py --max-line-length=100

# C (clang-format)
make format
```

### Pre-commit Hooks

```bash
pre-commit install
pre-commit run --all-files
```

---

## References

- [Q-Learning Algorithm](https://en.wikipedia.org/wiki/Q-learning)
- [Bellman Equation](https://en.wikipedia.org/wiki/Bellman_equation)
- [ε-Greedy Policy](https://en.wikipedia.org/wiki/Multi-armed_bandit#Semi-uniform_strategies)

---

## License

MIT License - see [LICENSE](LICENSE) for details.

Subject — see [en.subject.pdf](en.subject.pdf).
