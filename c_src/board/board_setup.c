/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   board_setup.c                                      :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: jhogonca <jhogonca@student.42porto.com>    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/07 21:15:00 by jhogonca          #+#    #+#             */
/*   Updated: 2026/01/07 21:10:58 by jhogonca         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "board_internal.h"

static void	init_rng(void)
{
	static int	seeded;

	if (!seeded)
	{
		srand((unsigned int)time(NULL));
		seeded = 1;
	}
}

static void	spawn_initial_apples(t_board *board,
			int count, t_board_cell type)
{
	int	index;

	index = 0;
	while (index < count)
	{
		spawn_apple(board, type);
		index++;
	}
}

void	board_reset(t_board *board)
{
	if (board == NULL)
		return ;
	init_rng();
	board_init_grid(board);
	init_apples(board);
	board_init_snake(board);
	spawn_initial_apples(board, board->num_green_apples, GREEN_APPLE);
	spawn_initial_apples(board, board->num_red_apples, RED_APPLE);
}
