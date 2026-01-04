// test_board.c
#include "board.h"
#include <stdio.h>

int main(void) {
    printf("=== Snake Board Test ===\n");
    
    Board* board = board_create();
    if (!board) {
        printf("Failed to create board!\n");
        return 1;
    }
    
    printf("\nInitial board:");
    board_print(board);
    
    // Test sequence
    Direction test_actions[] = {RIGHT, RIGHT, DOWN, DOWN, LEFT, LEFT};
    int num_tests = sizeof(test_actions) / sizeof(test_actions[0]);
    
    for (int i = 0; i < num_tests; i++) {
        if (board_is_game_over(board)) {
            printf("\nGame over at move %d!\n", i);
            break;
        }
        
        printf("\n--- Move %d: ", i + 1);
        switch (test_actions[i]) {
            case UP: printf("UP"); break;
            case LEFT: printf("LEFT"); break;
            case DOWN: printf("DOWN"); break;
            case RIGHT: printf("RIGHT"); break;
        }
        printf(" ---\n");
        
        int result = board_move(board, test_actions[i]);
        printf("Result code: %d\n", result);
        
        board_print(board);
    }
    
    printf("\n=== Final Statistics ===\n");
    printf("Score: %d\n", board_get_score(board));
    printf("Length: %d (Max: %d)\n", board_get_length(board), board_get_max_length(board));
    printf("Total moves: %d\n", board_get_moves(board));
    printf("Game over: %s\n", board_is_game_over(board) ? "YES" : "NO");
    
    board_destroy(board);
    printf("\nTest completed!\n");
    
    return 0;
}