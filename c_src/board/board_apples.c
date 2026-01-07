/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   board_apples.c                                     :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: jhogonca <jhogonca@student.42porto.com>    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/07 16:21:22 by jhogonca          #+#    #+#             */
/*   Updated: 2026/01/07 18:26:57 by jhogonca         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "board_internal.h"

static void	find_empty_cells(t_board *board, int (*positions)[2], int *count)
{
	int	y;
	int	x;

	y = 0;
	while (y < board->size)
	{
		x = 0;
		while (x < board->size)
		{
			if (board->grid[y][x] == EMPTY)
			{
				positions[*count][0] = x;
				positions[*count][1] = y;
				(*count)++;
			}
			x++;
		}
		y++;
	}
}

static void	place_apple_on_grid(t_board *board, int x, int y, t_board_cell type)
{
	int	idx;

	board->grid[y][x] = type;
	if (type == GREEN_APPLE
		&& board->green_apples_count < board->num_green_apples)
	{
		idx = board->green_apples_count;
		board->apples[idx].x = x;
		board->apples[idx].y = y;
		board->green_apples_count++;
	}
	else if (type == RED_APPLE
		&& board->red_apples_count < board->num_red_apples)
	{
		idx = board->num_green_apples;
		board->apples[idx].x = x;
		board->apples[idx].y = y;
		board->red_apples_count++;
	}
}

void	spawn_apple(t_board *board, t_board_cell type)
{
	int		empty_count;
	int		total_cells;
	int		(*positions)[2];
	int		idx;

	empty_count = 0;
	total_cells = board->size * board->size;
	positions = malloc(total_cells * sizeof(*positions));
	if (positions == NULL)
		return ;
	find_empty_cells(board, positions, &empty_count);
	if (empty_count > 0)
	{
		idx = rand() % empty_count;
		place_apple_on_grid(board, positions[idx][0], positions[idx][1], type);
	}
	free(positions);
}

void	init_apples(t_board *board)
{
	int	i;

	i = 0;
	while (i < board->num_apples)
	{
		board->apples[i].x = -1;
		board->apples[i].y = -1;
		i++;
	}
	board->green_apples_count = 0;
	board->red_apples_count = 0;
}

void	remove_apple(t_board *board, int x, int y, t_board_cell type)
{
	int	i;

	board->grid[y][x] = EMPTY;
	if (type == GREEN_APPLE)
	{
		board->green_apples_count--;
		i = 0;
		while (i < board->num_green_apples)
		{
			if (board->apples[i].x == x && board->apples[i].y == y)
			{
				board->apples[i].x = -1;
				board->apples[i].y = -1;
				break ;
			}
			i++;
		}
	}
	else if (type == RED_APPLE)
	{
		board->red_apples_count--;
		board->apples[board->num_green_apples].x = -1;
		board->apples[board->num_green_apples].y = -1;
	}
}
