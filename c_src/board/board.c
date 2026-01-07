/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   board.c                                            :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: jhogonca <jhogonca@student.42porto.com>    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/04 13:34:43 by jhogonca          #+#    #+#             */
/*   Updated: 2026/01/07 21:13:44 by jhogonca         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "board_internal.h"

static bool	allocate_grid(t_board *board);
static bool	allocate_snake_buffers(t_board *board);
static bool	allocate_apples(t_board *board);

t_board	*board_create(int size)
{
	t_board	*board;

	board = (t_board *)malloc(sizeof(t_board));
	if (board == NULL)
		return (NULL);
	if (size < 8 || size > 20)
		size = 10;
	board->size = size;
	board->max_snake_length = (size * size) - 1;
	board->num_green_apples = 2 + (size - 10) / 3;
	board->num_red_apples = 1 + (size - 10) / 5;
	board->num_apples = board->num_green_apples + board->num_red_apples;
	board->grid = NULL;
	board->snake.x = NULL;
	board->snake.y = NULL;
	board->apples = NULL;
	if (!allocate_grid(board)
		|| !allocate_snake_buffers(board)
		|| !allocate_apples(board))
	{
		board_destroy(board);
		return (NULL);
	}
	board_reset(board);
	return (board);
}

void	board_destroy(t_board *board)
{
	int	i;

	if (board == NULL)
		return ;
	if (board->grid != NULL)
	{
		i = 0;
		while (i < board->size)
		{
			free(board->grid[i]);
			i++;
		}
		free(board->grid);
	}
	free(board->snake.x);
	free(board->snake.y);
	free(board->apples);
	free(board);
}

static bool	allocate_grid(t_board *board)
{
	int		row;
	size_t	row_bytes;

	board->grid = (t_board_cell **)malloc(board->size * sizeof(t_board_cell *));
	if (board->grid == NULL)
		return (false);
	row = 0;
	while (row < board->size)
		board->grid[row++] = NULL;
	row = 0;
	row_bytes = board->size * sizeof(t_board_cell);
	while (row < board->size)
	{
		board->grid[row] = (t_board_cell *)malloc(row_bytes);
		if (board->grid[row] == NULL)
			return (false);
		row++;
	}
	return (true);
}

static bool	allocate_snake_buffers(t_board *board)
{
	board->snake.x = (int *)malloc(board->max_snake_length * sizeof(int));
	if (board->snake.x == NULL)
		return (false);
	board->snake.y = (int *)malloc(board->max_snake_length * sizeof(int));
	if (board->snake.y == NULL)
		return (false);
	return (true);
}

static bool	allocate_apples(t_board *board)
{
	board->apples = (t_apple *)malloc(board->num_apples * sizeof(t_apple));
	if (board->apples == NULL)
		return (false);
	return (true);
}
