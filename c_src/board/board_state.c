/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   board_state.c                                      :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: jhogonca <jhogonca@student.42porto.com>    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/07 00:00:00 by jhogonca          #+#    #+#             */
/*   Updated: 2026/01/11 20:05:45 by jhogonca         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "board_internal.h"

#define VISION_BUFFER_SIZE 32

static char	cell_to_symbol(t_board_cell cell);
static void	build_line(char *buffer, int buf_size, const t_board *board, int x,
				int y, int step_x, int step_y, bool reverse);

int	board_get_size(const t_board *board)
{
	if (!board)
		return (-1);
	return (board->size);
}

/*
** Scan a direction and return encoded value (3 bits):
** 0 = empty path to wall
** 1 = danger (wall/body) adjacent
** 2 = danger nearby (2-3 cells)
** 3 = green apple visible
** 4 = red apple visible
** 5 = body visible (not adjacent)
*/
static unsigned short	scan_direction(const t_board *board,
									int x, int y, int dx, int dy)
{
	t_board_cell	cell;
	int				dist;
	int				first_danger;
	int				first_green;
	int				first_red;

	dist = 0;
	first_danger = -1;
	first_green = -1;
	first_red = -1;
	while (1)
	{
		x += dx;
		y += dy;
		dist++;
		cell = check_cell(board, x, y);
		if (cell == WALL)
		{
			if (first_danger < 0)
				first_danger = dist;
			break ;
		}
		if (cell == SNAKE_BODY && first_danger < 0)
			first_danger = dist;
		if (cell == GREEN_APPLE && first_green < 0)
			first_green = dist;
		if (cell == RED_APPLE && first_red < 0)
			first_red = dist;
	}
	if (first_danger == 1)
		return (1);
	if (first_green > 0 && (first_danger < 0 || first_green < first_danger))
		return (3);
	if (first_red > 0 && (first_danger < 0 || first_red < first_danger))
		return (4);
	if (first_danger > 0 && first_danger <= 3)
		return (2);
	if (first_danger > 0)
		return (5);
	return (0);
}

unsigned short	board_get_state(const t_board *board)
{
	int				head_idx;
	int				head_x;
	int				head_y;
	unsigned short	state;

	if (!board)
		return (0);
	head_idx = board->snake.head_idx;
	head_x = board->snake.x[head_idx];
	head_y = board->snake.y[head_idx];
	state = 0;
	state |= (scan_direction(board, head_x, head_y, 0, -1) << 9);
	state |= (scan_direction(board, head_x, head_y, -1, 0) << 6);
	state |= (scan_direction(board, head_x, head_y, 0, 1) << 3);
	state |= (scan_direction(board, head_x, head_y, 1, 0) << 0);
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
	build_line(down, VISION_BUFFER_SIZE,
		board, head_x, head_y + 1, 0, 1, false);
	build_line(left, VISION_BUFFER_SIZE,
		board, head_x - 1, head_y, -1, 0, true);
	build_line(right, VISION_BUFFER_SIZE, board,
		head_x + 1, head_y, 1, 0, false);
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

static void	build_line(char *buffer, int buf_size, const t_board *board, int x,
					int y, int step_x, int step_y, bool reverse)
{
	int		len;
	int		limit;
	int		i;
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
