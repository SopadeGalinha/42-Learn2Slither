/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   board_helpers.c                                    :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: jhogonca <jhogonca@student.42porto.com>    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/07 20:14:31 by jhogonca          #+#    #+#             */
/*   Updated: 2026/01/07 20:58:57 by jhogonca         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "board.h"
#include "board_internal.h"

bool	board_is_game_over(const t_board *board)
{
	if (!board)
		return (true);
	return (board->game_over);
}

void	board_init_grid(t_board *board)
{
	int	i;
	int	j;

	i = 0;
	while (i < board->size)
	{
		j = 0;
		while (j < board->size)
			board->grid[i][j++] = EMPTY;
		i++;
	}
}

void	board_init_snake(t_board *board)
{
	int	i;
	int	j;

	i = 1 + rand() % (board->size - 4);
	j = 1 + rand() % (board->size - 4);
	board->snake.x[0] = i;
	board->snake.y[0] = j;
	board->snake.x[1] = i;
	board->snake.y[1] = j + 1;
	board->snake.x[2] = i;
	board->snake.y[2] = j + 2;
	board->grid[j][i] = SNAKE_BODY;
	board->grid[j + 1][i] = SNAKE_BODY;
	board->grid[j + 2][i] = SNAKE_HEAD;
	board->snake.length = 3;
	board->snake.head_idx = 2;
	board->max_length = 3;
	board->game_over = false;
	board->score = 0;
	board->moves = 0;
}

t_board_cell	check_cell(const t_board *board, int x, int y)
{
	if (x < 0 || x >= board->size || y < 0 || y >= board->size)
		return (WALL);
	return (board->grid[y][x]);
}
