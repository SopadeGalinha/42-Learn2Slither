# 42-Learn2Slither
This project is about reinforcement learning. A snake that learns how to behave in an environment through trial and error

## Requirements Analysis

| Req | Description | Status | Details |
|-----|-------------|--------|---------|
| **IV.1** | 10x10 grid environment | ✅ | `BOARD_SIZE 10` in board.h |
| **IV.1** | Snake initial size 3 | ✅ | `INITIAL_LENGTH 3` in board.h |
| **IV.1** | 2 green apples (+1 length) | ✅ | Implemented in board.c |
| **IV.1** | 1 red apple (-1 length, snake dies if len=1) | ✅ | Implemented in board.c |
| **IV.2** | 4 actions: UP/LEFT/DOWN/RIGHT | ✅ | `Direction` enum implemented |
| **IV.2** | Result: state, reward, done | ✅ | `board.step()` returns tuple |
| **IV.3** | State representation (can be 12 bits) | ✅ | `get_state()` returns 12-bit vision |
| **IV.3** | Vision in 4 directions (danger, apple, etc.) | ✅ | 3 bits per direction × 4 = 12 bits |
| **IV.4** | Customizable reward system | ✅ | rewards.py: green +10, red -10, death -50, step -0.1 |
| **IV.5** | Q-learning agent with Q-table | ❌ | **NOT IMPLEMENTED** |
| **IV.5** | ε-greedy exploration | ❌ | **NOT IMPLEMENTED** |
| **IV.5** | Q-learning update | ❌ | **NOT IMPLEMENTED** |
| **IV.5** | Save/Load models | ❌ | **NOT IMPLEMENTED** |
| **IV.6** | Training script `train.py` | ❌ | **Exists but manual mode only, Agent NOT USED** |
| **IV.6** | Flag `--sessions` (episodes) | ⚠️ | Exists as `--episodes`  |
| **IV.6** | Flag `--save` (save model) | ❌ | **NOT IMPLEMENTED** |
| **IV.6** | Flag `--load` (load model) | ❌ | **NOT IMPLEMENTED** |
| **IV.6** | Flag `--dontlearn` (eval mode) | ❌ | **NOT IMPLEMENTED** |
| **IV.6** | `models/` folder with saved models | ❌ | **Folder does not exist** |
| **IV.6** | At least 3 models (1, 10, 100 sessions) | ❌ | **No trained models** |
| **V** | Optional graphics/visualization | ✅ | Pygame Viewer with lobby, stats, game over |
| **V** | Display snake, apples, grid | ✅ | Full rendering |
| **V** | Panel with state/actions | ✅ | HUD with This Episode + Session Best stats |
| **V** | Step-by-step mode | ✅ | `--render step` |
| **V** | Configurable FPS | ✅ | `--fps` flag |
| **VI** | **BONUS:** Variable board size | ❌ | Board fixed 10x10 (hardcoded in C) |
| **VI** | **BONUS:** Advanced config panel | ⚠️ | Stats yes, but no config panel |

### Summary

| Category | Complete | Partial | Missing |
|----------|----------|---------|---------|
| **Mandatory** | 17 | 1 | 6 |
| **Bonus** | 0 | 1 | 1 |


## References

- [YouTube: Introduction to Reinforcement Learning](https://www.youtube.com/watch?v=JgvyzIkgxF0)
- [YouTube: A equação de Bellmann](https://www.youtube.com/watch?v=cOy0sUTouyo)
- [YouTube: Equação de Bellman](https://www.youtube.com/watch?v=cOy0sUTouyo)
- [YouTube: A ideia que tornou a Inteligência Artificial possível](https://www.youtube.com/watch?v=mBqfY_TX_8o)
