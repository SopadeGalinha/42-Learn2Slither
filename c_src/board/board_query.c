/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   board_query.c                                      :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: jhogonca <jhogonca@student.42porto.com>    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/07 00:00:00 by jhogonca          #+#    #+#             */
/*   Updated: 2026/01/07 19:48:02 by jhogonca         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "board.h"

int	board_get_score(const t_board *board)
{
	if (!board)
		return (0);
	return (board->score);
}

int	board_get_length(const t_board *board)
{
	if (!board)
		return (0);
	return (board->snake.length);
}

int	board_get_max_length(const t_board *board)
{
	if (!board)
		return (0);
	return (board->max_length);
}

int	board_get_moves(const t_board *board)
{
	if (!board)
		return (0);
	return (board->moves);
}

t_board_cell	board_get_cell(const t_board *board, int x, int y)
{
	if (!board)
		return (EMPTY);
	if (x < 0 || x >= board->size || y < 0 || y >= board->size)
		return (WALL);
	return (board->grid[y][x]);
}
