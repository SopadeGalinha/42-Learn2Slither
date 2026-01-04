#ifndef BOARD_H
# define BOARD_H

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <stdbool.h>

// ============= CONFIGURATION =============
#define BOARD_SIZE 10
#define NUM_GREEN_APPLES 2
#define NUM_RED_APPLES 1
#define NUM_APPLES (NUM_GREEN_APPLES + NUM_RED_APPLES)
#define MAX_SNAKE_LENGTH ((BOARD_SIZE * BOARD_SIZE) - 1)

// ============= REWARDS (for RL) =============
#define REWARD_GREEN_APPLE  (10.0f)
#define REWARD_RED_APPLE    (-10.0f)
#define REWARD_DEATH        (-50.0f)   // wall, self, or length-zero
#define REWARD_STEP         (-0.1f)    // small living/step penalty

// ============= COMPILE-TIME VALIDATION =============
#if BOARD_SIZE < 10
# error "BOARD_SIZE must be at least 10"
#endif

#if NUM_GREEN_APPLES < 1 || NUM_GREEN_APPLES > 5
# error "NUM_GREEN_APPLES must be between 1 and 5"
#endif

#if NUM_RED_APPLES < 1 || NUM_RED_APPLES > 5
# error "NUM_RED_APPLES must be between 1 and 5"
#endif

#if (NUM_APPLES > (BOARD_SIZE * BOARD_SIZE) / 4)
# error "Total apples exceeds 25% of board capacity"
#endif

// ============= TYPES =============
typedef enum {
    EMPTY       = 0b000,  // 0
    WALL        = 0b001,  // 1
    SNAKE_HEAD  = 0b010,  // 2  
    SNAKE_BODY  = 0b011,  // 3
    GREEN_APPLE = 0b100,  // 4
    RED_APPLE   = 0b101   // 5
} BoardCell;

typedef enum {
    UP = 0,    /**< Move up */
    LEFT = 1,  /**< Move left */
    DOWN = 2,  /**< Move down */
    RIGHT = 3  /**< Move right */
} Direction;

typedef enum {
    HIT_WALL = 1,
    HIT_SELF = 2,
    ATE_GREEN_APPLE = 3,
    ATE_RED_APPLE = 4,
    LENGTH_ZERO = 5
} Actions;

typedef struct Board Board;

// ============= PUBLIC API =============

// Creation/Destruction
Board*  board_create(void);
void    board_destroy(Board* board);

// Game control
void    board_reset(Board* board);
int     board_move(Board* board, Direction action);

// State query
bool    board_is_game_over(const Board* board);
int     board_get_score(const Board* board);
int     board_get_length(const Board* board);
int     board_get_max_length(const Board* board);
int     board_get_moves(const Board* board);
unsigned short board_get_state(const Board* board);  // Snake vision (12 bits)

// Rewards accessors (mirrors macros for Python/ctypes)
float   board_get_reward_green_apple(void);
float   board_get_reward_red_apple(void);
float   board_get_reward_death(void);
float   board_get_reward_step(void);

// Debug/display
void    board_print(const Board* board);

#endif
