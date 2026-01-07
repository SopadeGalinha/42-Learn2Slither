/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   board_state.c                                      :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: jhogonca <jhogonca@student.42porto.com>    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/07 00:00:00 by jhogonca          #+#    #+#             */
/*   Updated: 2026/01/07 21:56:10 by jhogonca         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "board_internal.h"

#define VISION_BUFFER_SIZE 32

static char	cell_to_symbol(t_board_cell cell);
static void	build_line(char *buffer, int buf_size, const t_board *board,
			int x, int y, int step_x, int step_y, bool reverse);

int	board_get_size(const t_board *board)
{
	if (!board)
		return (BOARD_SIZE);
	return (board->size);
}

unsigned short	board_get_state(const t_board *board)
{
	int			head_idx;
	int			head_x;
	int			head_y;
	unsigned short	state;

	if (!board)
		return (0);
	head_idx = board->snake.head_idx;
	head_x = board->snake.x[head_idx];
	head_y = board->snake.y[head_idx];
	state = 0;
	state |= (check_cell(board, head_x, head_y - 1) << 9);
	state |= (check_cell(board, head_x - 1, head_y) << 6);
	state |= (check_cell(board, head_x, head_y + 1) << 3);
	state |= (check_cell(board, head_x + 1, head_y) << 0);
	return (state);
}

void	board_print(const t_board *board)
{
	char	up[VISION_BUFFER_SIZE];
	char	down[VISION_BUFFER_SIZE];
	char	left[VISION_BUFFER_SIZE];
	char	right[VISION_BUFFER_SIZE];
	int		head_idx;
	int		head_x;
	int		head_y;
	int		indent;
	int		i;

	if (board == NULL)
		return ;
	head_idx = board->snake.head_idx;
	head_x = board->snake.x[head_idx];
	head_y = board->snake.y[head_idx];
	build_line(up, VISION_BUFFER_SIZE, board, head_x, head_y - 1, 0, -1, true);
	build_line(down, VISION_BUFFER_SIZE, board, head_x, head_y + 1, 0, 1, false);
	build_line(left, VISION_BUFFER_SIZE, board, head_x - 1, head_y, -1, 0, true);
	build_line(right, VISION_BUFFER_SIZE, board, head_x + 1, head_y, 1, 0, false);
	indent = (int)strlen(left);
	i = 0;
	while (up[i] != '\0')
	{
		printf("%*s%c\n", indent, "", up[i]);
		i++;
	}
	printf("%sH%s\n", left, right);
	i = 0;
	while (down[i] != '\0')
	{
		printf("%*s%c\n", indent, "", down[i]);
		i++;
	}
}

static char	cell_to_symbol(t_board_cell cell)
{
	if (cell == SNAKE_BODY)
		return ('S');
	if (cell == GREEN_APPLE)
		return ('G');
	if (cell == RED_APPLE)
		return ('R');
	return ('0');
}

static void	build_line(char *buffer, int buf_size, const t_board *board,
			int x, int y, int step_x, int step_y, bool reverse)
{
	int	len;
	int	limit;
	int	i;
	char	tmp;

	len = 0;
	limit = buf_size - 2;
	while (x >= 0 && x < board->size && y >= 0 && y < board->size)
	{
		if (len == limit)
			break ;
		buffer[len++] = cell_to_symbol(board->grid[y][x]);
		x += step_x;
		y += step_y;
	}
	if (len < buf_size - 1)
		buffer[len++] = 'W';
	buffer[len] = '\0';
	if (!reverse)
		return ;
	i = 0;
	while (i < len / 2)
	{
		tmp = buffer[i];
		buffer[i] = buffer[len - 1 - i];
		buffer[len - 1 - i] = tmp;
		i++;
	}
}
