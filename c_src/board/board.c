#include "board.h"

struct Board {
	BoardCell grid[BOARD_SIZE][BOARD_SIZE];

	struct {
		int x[MAX_SNAKE_LENGTH];
		int y[MAX_SNAKE_LENGTH];
		int head_idx;
		int length;
	} snake;

	bool game_over;
	int score;
	int moves;
	int max_length;

	int green_apples_count;
	int red_apples_count;

	struct {
		int x;
		int y;
	} apples[NUM_APPLES];
};

// ============= INTERNAL FUNCTIONS =============

// Helper function to check cell (outside of board_get_state!)
static BoardCell check_cell(const Board *board, int x, int y) {
	if (x < 0 || x >= BOARD_SIZE || y < 0 || y >= BOARD_SIZE)
		return WALL;
	return board->grid[y][x];
}

static void spawn_apple(Board *board, BoardCell type) {

	int empty_count = 0;
	int empty_positions[BOARD_SIZE * BOARD_SIZE][2];
	for (int y = 0; y < BOARD_SIZE; y++) {
		for (int x = 0; x < BOARD_SIZE; x++) {
			if (board->grid[y][x] == EMPTY) {
				empty_positions[empty_count][0] = x;
				empty_positions[empty_count][1] = y;
				empty_count++;
			}
		}
	}

	if (empty_count > 0) {
		int idx = rand() % empty_count;
		int x = empty_positions[idx][0];
		int y = empty_positions[idx][1];

		board->grid[y][x] = type;

		if (type == GREEN_APPLE) {
			board->green_apples_count++;
			for (int i = 0; i < NUM_GREEN_APPLES; i++) {
				if (board->apples[i].x == -1) {
					board->apples[i].x = x;
					board->apples[i].y = y;
					break;
				}
			}
		}
		else if (type == RED_APPLE) {
			board->red_apples_count++;
			board->apples[NUM_GREEN_APPLES].x = x;
			board->apples[NUM_GREEN_APPLES].y = y;
		}
	}
}

// Initialize apples array with invalid positions
static void init_apples(Board *board)
{
	for (int i = 0; i < NUM_APPLES; i++) {
		board->apples[i].x = -1;
		board->apples[i].y = -1;
	}
	board->green_apples_count = 0;
	board->red_apples_count = 0;
}

// Internal function: remove apple from grid and counters
static void remove_apple(Board *board, int x, int y, BoardCell type) {
	board->grid[y][x] = EMPTY;

	if (type == GREEN_APPLE) {
		board->green_apples_count--;
		for (int i = 0; i < NUM_GREEN_APPLES; i++) {
			if (board->apples[i].x == x && board->apples[i].y == y) {
				board->apples[i].x = -1;
				board->apples[i].y = -1;
				break;
			}
		}
	} else if (type == RED_APPLE) {
		board->red_apples_count--;
		board->apples[NUM_GREEN_APPLES].x = -1;
		board->apples[NUM_GREEN_APPLES].y = -1;
	}
}

// random number generator
static void init_rng(void) {
	static int seeded = 0;
	if (!seeded) {
		srand((unsigned int)time(NULL));
		seeded = 1;
	}
}

static void init_board(Board *board) {
	if (board == NULL)
		return;

	init_rng();

	for (int y = 0; y < BOARD_SIZE; y++) {
		for (int x = 0; x < BOARD_SIZE; x++) {
			board->grid[y][x] = EMPTY;
		}
	}

	init_apples(board);

	board->snake.length = 3;
	board->snake.head_idx = 2;

	// Position that doesn't collide with borders
	int start_x = 1 + rand() % (BOARD_SIZE - 2);
	int start_y = 1 + rand() % (BOARD_SIZE - 2);

	// Vertical snake (head at bottom, body above)
	for (int i = 0; i < 3; i++) {
		board->snake.x[i] = start_x;
		board->snake.y[i] = start_y + i;
		board->grid[start_y + i][start_x] = (i == 2) ? SNAKE_HEAD : SNAKE_BODY;
	}

	// Spawn initial apples
	for (int i = 0; i < NUM_GREEN_APPLES; i++)
		spawn_apple(board, GREEN_APPLE);
	for (int i = 0; i < NUM_RED_APPLES; i++)
		spawn_apple(board, RED_APPLE);

	// Game state
	board->game_over = false;
	board->score = 0;
	board->moves = 0;
	board->max_length = board->snake.length;
}

// ============= PUBLIC FUNCTIONS =============

Board *board_create(void) {
	Board *board = (Board *)malloc(sizeof(Board));
	if (board == NULL)
		return NULL;
	init_board(board);
	return board;
}

void board_destroy(Board *board) {
	if (board != NULL)
		free(board);
}

void board_reset(Board *board) {
	if (board == NULL)
		return;
	init_board(board);
}

// Internal function: move snake in circular array
static void move_snake(Board *board, int new_x, int new_y, bool grow) {
	// Calculate next head position in circular buffer
	int next_head_idx = (board->snake.head_idx + 1) % MAX_SNAKE_LENGTH;

	// Place head at new position
	board->snake.x[next_head_idx] = new_x;
	board->snake.y[next_head_idx] = new_y;
	board->snake.head_idx = next_head_idx;

	// Draw head on grid
	board->grid[new_y][new_x] = SNAKE_HEAD;

	// Convert old head position to body
	int old_head_idx = (next_head_idx - 1 + MAX_SNAKE_LENGTH) % MAX_SNAKE_LENGTH;
	board->grid[board->snake.y[old_head_idx]][board->snake.x[old_head_idx]] = SNAKE_BODY;

	// If didn't grow, remove tail from grid
	if (!grow) {
		int tail_removal_idx = (next_head_idx - board->snake.length + MAX_SNAKE_LENGTH) % MAX_SNAKE_LENGTH;
		board->grid[board->snake.y[tail_removal_idx]][board->snake.x[tail_removal_idx]] = EMPTY;
	}
}

int board_move(Board *board, Direction action) {
	if (board == NULL || board->game_over)
		return -1;

	board->moves++;

	// 1. Current head position
	int head_idx = board->snake.head_idx;
	int head_x = board->snake.x[head_idx];
	int head_y = board->snake.y[head_idx];

	// 2. New position
	int new_x = head_x;
	int new_y = head_y;

	switch (action)
	{
	case UP:
		new_y--;
		break;
	case LEFT:
		new_x--;
		break;
	case DOWN:
		new_y++;
		break;
	case RIGHT:
		new_x++;
		break;
	default:
		return -1;
	}

	// 3. Check collision with walls
	if (new_x < 0 || new_x >= BOARD_SIZE || new_y < 0 || new_y >= BOARD_SIZE) {
		board->game_over = true;
		return HIT_WALL;
	}

	// 4. Check collision with body
	BoardCell target = board->grid[new_y][new_x];
	if (target == SNAKE_BODY || target == SNAKE_HEAD) {
		board->game_over = true;
		return HIT_SELF;
	}

	// 5. Process target cell
	int result = 0; // Nnormal movement
	bool grow = false;

	if (target == GREEN_APPLE) {
		result = ATE_GREEN_APPLE;
		board->score += 10;
		grow = true; // Snake grows

		if (board->snake.length + 1 > board->max_length) {
			board->max_length = board->snake.length + 1;
		}

		// Remove eaten apple
		remove_apple(board, new_x, new_y, GREEN_APPLE);
		// Spawn new green apple
		spawn_apple(board, GREEN_APPLE);
	} else if (target == RED_APPLE) {
		result = ATE_RED_APPLE;
		board->score -= 10;

		if (board->snake.length > 1) {
			// Snake shrinks
			int tail_idx = (head_idx - board->snake.length + 1 + MAX_SNAKE_LENGTH) % MAX_SNAKE_LENGTH;
			board->grid[board->snake.y[tail_idx]][board->snake.x[tail_idx]] = EMPTY;
			board->snake.length--;
		} else {
			// Length 1 eats red apple = game over
			board->game_over = true;
			remove_apple(board, new_x, new_y, RED_APPLE);
			spawn_apple(board, RED_APPLE);
			return LENGTH_ZERO;
		}

		// Remove eaten apple
		remove_apple(board, new_x, new_y, RED_APPLE);
		spawn_apple(board, RED_APPLE);
	}
	move_snake(board, new_x, new_y, grow);

	if (grow)
		board->snake.length++;
	return result;
}

bool board_is_game_over(const Board *board) {
	return board ? board->game_over : true;
}

int board_get_score(const Board *board) {
	return board ? board->score : 0;
}

int board_get_length(const Board *board) {
	return board ? board->snake.length : 0;
}

int board_get_max_length(const Board *board) {
	return board ? board->max_length : 0;
}

int board_get_moves(const Board *board) {
	return board ? board->moves : 0;
}

unsigned short board_get_state(const Board *board) {
	if (!board)
		return 0;

	int head_idx = board->snake.head_idx;
	int head_x = board->snake.x[head_idx];
	int head_y = board->snake.y[head_idx];

	unsigned short state = 0;

	// Up, Left, Down, Right (3 bits each)
	state |= (check_cell(board, head_x, head_y - 1) << 9);
	state |= (check_cell(board, head_x - 1, head_y) << 6);
	state |= (check_cell(board, head_x, head_y + 1) << 3);
	state |= (check_cell(board, head_x + 1, head_y) << 0);

	return state;
}

void board_print(const Board *board) {
	if (board == NULL)
		return;

	printf("\n╔");
	for (int j = 0; j < BOARD_SIZE; j++)
		printf("══");
	printf("╗\n");

	for (int i = 0; i < BOARD_SIZE; i++) {
		printf("║");
		for (int j = 0; j < BOARD_SIZE; j++) {
			switch (board->grid[i][j]) {
			case EMPTY:
				printf("  ");
				break;
			case WALL:
				printf("██");
				break;
			case SNAKE_HEAD:
				printf("██");
				break;
			case SNAKE_BODY:
				printf("░░");
				break;
			case GREEN_APPLE:
				printf("🟢");
				break;
			case RED_APPLE:
				printf("🔴");
				break;
			default:
				printf("??");
				break;
			}
		}
		printf("║\n");
	}

	printf("╚");
	for (int j = 0; j < BOARD_SIZE; j++)
		printf("══");
	printf("╝\n");

	// Game statistics
	printf("\nScore: %d | Length: %d | Moves: %d | Max Length: %d\n",
		board->score, board->snake.length, board->moves, board->max_length);
	printf("Green Apples: %d | Red Apples: %d | Game Over: %s\n",
		board->green_apples_count, board->red_apples_count,
		board->game_over ? "YES" : "NO");

	// Compacted state
	unsigned short state = board_get_state(board);
	printf("State: 0x%03X (", state);
	for (int i = 11; i >= 0; i--) {
		printf("%d", (state >> i) & 1);
		if (i > 0 && i % 3 == 0)
			printf(" ");
	}
	printf(")\n");
}

float board_get_reward_green_apple(void) {
	return REWARD_GREEN_APPLE;
}

float board_get_reward_red_apple(void) {
	return REWARD_RED_APPLE;
}

float board_get_reward_death(void) {
	return REWARD_DEATH;
}

float board_get_reward_step(void) {
	return REWARD_STEP;
}
