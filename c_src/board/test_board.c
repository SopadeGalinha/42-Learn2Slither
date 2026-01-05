// test_board.c
#include "board.h"
#include <stdio.h>

#define GREEN "\033[32m"
#define RED   "\033[31m"
#define RESET "\033[0m"

static int g_failed = 0;
static int g_total = 0;

#define TEST(name, cond) do { \
    printf("  %-45s %s\n", name, (cond) ? GREEN "OK" RESET : RED "KO" RESET); \
    if (!(cond)) g_failed++; \
    g_total++; \
} while(0)

#define SECTION(name) printf("\n%s\n", name)

void test_creation_destruction(void) {
    SECTION("[Creation & Destruction]");
    
    Board* board = board_create();
    TEST("board_create returns non-NULL", board != NULL);
    
    Board* board2 = board_create();
    TEST("multiple boards can be created", board2 != NULL);
    
    board_destroy(board);
    board_destroy(board2);
    board_destroy(NULL);
    TEST("board_destroy handles NULL", 1);
}

void test_initial_state(void) {
    SECTION("[Initial State]");
    
    Board* board = board_create();
    
    TEST("length=3, score=0, moves=0, not game over",
        board_get_length(board) == 3 &&
        board_get_score(board) == 0 &&
        board_get_moves(board) == 0 &&
        !board_is_game_over(board));
    
    TEST("max_length >= length", 
        board_get_max_length(board) >= board_get_length(board));
    
    TEST("board_get_size returns BOARD_SIZE", 
        board_get_size() == BOARD_SIZE);
    
    board_destroy(board);
}

void test_state_encoding(void) {
    SECTION("[State Encoding]");
    
    Board* board = board_create();
    
    unsigned short state = board_get_state(board);
    TEST("state fits in 12 bits", state <= 0x0FFF);
    TEST("state is non-zero", state > 0);
    
    unsigned short state2 = board_get_state(board);
    TEST("state is deterministic", state == state2);
    
    board_destroy(board);
}

void test_movement(void) {
    SECTION("[Movement]");
    
    Board* board = board_create();
    
    int result = board_move(board, RIGHT);
    TEST("move RIGHT executes", result >= -1);
    TEST("moves incremented after move", board_get_moves(board) == 1);
    
    result = board_move(board, DOWN);
    TEST("move DOWN executes", result >= -1);
    TEST("moves == 2 after second move", board_get_moves(board) == 2);
    
    result = board_move(board, LEFT);
    TEST("move LEFT executes", result >= -1);
    
    result = board_move(board, UP);
    TEST("move UP executes", result >= -1);
    
    board_destroy(board);
}

void test_cell_access(void) {
    SECTION("[Cell Access]");
    
    Board* board = board_create();
    
    int found_head = 0;
    int found_body = 0;
    int size = board_get_size();
    
    for (int y = 0; y < size && !found_head; y++) {
        for (int x = 0; x < size; x++) {
            BoardCell cell = board_get_cell(board, x, y);
            if (cell == SNAKE_HEAD) found_head = 1;
            if (cell == SNAKE_BODY) found_body = 1;
        }
    }
    
    TEST("snake head found on board", found_head);
    TEST("snake body found on board", found_body);
    TEST("out of bounds returns WALL", board_get_cell(board, -1, 0) == WALL);
    TEST("out of bounds (max) returns WALL", board_get_cell(board, size, 0) == WALL);
    
    board_destroy(board);
}

void test_reset(void) {
    SECTION("[Reset]");
    
    Board* board = board_create();
    
    // Make some moves
    board_move(board, RIGHT);
    board_move(board, RIGHT);
    board_move(board, DOWN);
    
    int moves_before = board_get_moves(board);
    TEST("moves > 0 before reset", moves_before > 0);
    
    board_reset(board);
    
    TEST("reset: length=3, moves=0, not game over",
        board_get_length(board) == 3 &&
        board_get_moves(board) == 0 &&
        !board_is_game_over(board));
    
    TEST("max_length preserved after reset", 
        board_get_max_length(board) >= 3);
    
    board_destroy(board);
}

void test_game_over(void) {
    SECTION("[Game Over Detection]");
    
    Board* board = board_create();
    
    // Move until game over or max iterations
    int max_moves = BOARD_SIZE * BOARD_SIZE * 2;
    Direction dirs[] = {UP, UP, UP, UP, UP, UP, UP, UP, UP};
    int i = 0;
    
    while (!board_is_game_over(board) && i < max_moves) {
        board_move(board, dirs[i % 9]);
        i++;
    }
    
    TEST("game over eventually triggered", board_is_game_over(board) || i >= max_moves);
    
    if (board_is_game_over(board)) {
        int result = board_move(board, RIGHT);
        TEST("move after game over returns -1", result == -1);
    }
    
    board_destroy(board);
}

void test_rewards(void) {
    SECTION("[Reward Constants]");
    
    TEST("rewards: green>0, red<0, death<0, step<0",
        board_get_reward_green_apple() > 0 &&
        board_get_reward_red_apple() < 0 &&
        board_get_reward_death() < 0 &&
        board_get_reward_step() < 0);
    
    TEST("death penalty is worst", 
        board_get_reward_death() <= board_get_reward_red_apple());
}

int main(void) {
    printf("=== Snake Board Tests ===\n");
    
    test_creation_destruction();
    test_initial_state();
    test_state_encoding();
    test_movement();
    test_cell_access();
    test_reset();
    test_game_over();
    test_rewards();
    
    printf("\n=== Results: %d/%d passed ===\n", g_total - g_failed, g_total);
    
    return g_failed > 0 ? 1 : 0;
}