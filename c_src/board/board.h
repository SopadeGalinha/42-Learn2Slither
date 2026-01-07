/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   board.h                                            :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: jhogonca <jhogonca@student.42porto.com>    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/07 18:28:16 by jhogonca          #+#    #+#             */
/*   Updated: 2026/01/07 20:52:37 by jhogonca         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#ifndef BOARD_H
# define BOARD_H

# include <stdio.h>
# include <stdlib.h>
# include <string.h>
# include <time.h>
# include <stdbool.h>

# define BOARD_SIZE 10
# define NUM_GREEN_APPLES 2
# define NUM_RED_APPLES 1
# define NUM_APPLES 3
# define MAX_SNAKE_LENGTH 99

# define REWARD_GREEN_APPLE 10.0f
# define REWARD_RED_APPLE -10.0f
# define REWARD_DEATH -50.0f
# define REWARD_STEP -0.1f

typedef enum e_direction
{
	UP = 0,
	LEFT = 1,
	DOWN = 2,
	RIGHT = 3
}	t_direction;

typedef enum e_board_cell
{
	EMPTY = 0,
	WALL = 1,
	SNAKE_HEAD = 2,
	SNAKE_BODY = 3,
	GREEN_APPLE = 4,
	RED_APPLE = 5
}	t_board_cell;

typedef enum e_actions
{
	HIT_WALL = 1,
	HIT_SELF = 2,
	ATE_GREEN_APPLE = 3,
	ATE_RED_APPLE = 4,
	LENGTH_ZERO = 5
}	t_actions;

typedef struct s_apple
{
	int	x;
	int	y;
}	t_apple;

typedef struct s_snake
{
	int	*x;
	int	*y;
	int	head_idx;
	int	length;
}	t_snake;

typedef struct s_board
{
	t_board_cell	**grid;
	t_snake			snake;
	int				size;
	int				max_snake_length;
	int				num_apples;
	int				num_green_apples;
	int				num_red_apples;
	bool			game_over;
	int				score;
	int				moves;
	int				max_length;
	int				green_apples_count;
	int				red_apples_count;
	t_apple			*apples;
}	t_board;

t_board				*board_create(int size);
void				board_destroy(t_board *board);
void				board_reset(t_board *board);
int					board_move(t_board *board, t_direction action);
bool				board_is_game_over(const t_board *board);
int					board_get_score(const t_board *board);
int					board_get_length(const t_board *board);
int					board_get_max_length(const t_board *board);
int					board_get_moves(const t_board *board);
unsigned short		board_get_state(const t_board *board);
t_board_cell		board_get_cell(const t_board *board, int x, int y);
int					board_get_size(const t_board *board);
float				board_get_reward_green_apple(void);
float				board_get_reward_red_apple(void);
float				board_get_reward_death(void);
float				board_get_reward_step(void);
void				board_print(const t_board *board);

#endif
