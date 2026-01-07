/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   board_move.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: jhogonca <jhogonca@student.42porto.com>    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/07 00:00:00 by jhogonca          #+#    #+#             */
/*   Updated: 2026/01/07 20:59:42 by jhogonca         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "board_internal.h"

static int	handle_green_apple(t_board *b, int x, int y);
static int	handle_red_apple(t_board *b, int x, int y);
static int	resolve_move(t_board *board, int new_x, int new_y);

void	move_snake(t_board *board, int new_x, int new_y, bool grow)
{
	int	next_idx;
	int	old_idx;
	int	tail_idx;

	next_idx = (board->snake.head_idx + 1) % board->max_snake_length;
	board->snake.x[next_idx] = new_x;
	board->snake.y[next_idx] = new_y;
	board->snake.head_idx = next_idx;
	board->grid[new_y][new_x] = SNAKE_HEAD;
	old_idx = (next_idx - 1 + board->max_snake_length)
		% board->max_snake_length;
	board->grid[board->snake.y[old_idx]][board->snake.x[old_idx]]
		= SNAKE_BODY;
	if (!grow)
	{
		tail_idx = (next_idx - board->snake.length);
		if (tail_idx < 0)
			tail_idx += board->max_snake_length;
		board->grid[board->snake.y[tail_idx]][board->snake.x[tail_idx]]
			= EMPTY;
	}
}

static int	resolve_move(t_board *board, int new_x, int new_y)
{
	int	target;

	if (new_x < 0 || new_x >= board->size
		|| new_y < 0 || new_y >= board->size)
	{
		board->game_over = true;
		return (HIT_WALL);
	}
	target = board->grid[new_y][new_x];
	if (target == SNAKE_BODY || target == SNAKE_HEAD)
	{
		board->game_over = true;
		return (HIT_SELF);
	}
	if (target == GREEN_APPLE)
		return (handle_green_apple(board, new_x, new_y));
	if (target == RED_APPLE)
		return (handle_red_apple(board, new_x, new_y));
	move_snake(board, new_x, new_y, false);
	return (0);
}

int	board_move(t_board *board, t_direction action)
{
	int	new_x;
	int	new_y;

	if (board == NULL || board->game_over)
		return (-1);
	board->moves++;
	new_x = board->snake.x[board->snake.head_idx];
	new_y = board->snake.y[board->snake.head_idx];
	if (action == UP)
		new_y--;
	else if (action == LEFT)
		new_x--;
	else if (action == DOWN)
		new_y++;
	else if (action == RIGHT)
		new_x++;
	else
		return (-1);
	return (resolve_move(board, new_x, new_y));
}

static int	handle_green_apple(t_board *b, int x, int y)
{
	b->score += 10;
	if (b->snake.length + 1 > b->max_length)
		b->max_length = b->snake.length + 1;
	remove_apple(b, x, y, GREEN_APPLE);
	spawn_apple(b, GREEN_APPLE);
	move_snake(b, x, y, true);
	b->snake.length++;
	return (ATE_GREEN_APPLE);
}

static int	handle_red_apple(t_board *b, int x, int y)
{
	int	tail_idx;

	b->score -= 10;
	if (b->snake.length > 1)
	{
		tail_idx = b->snake.head_idx - b->snake.length + 1;
		if (tail_idx < 0)
			tail_idx += b->max_snake_length;
		b->grid[b->snake.y[tail_idx]][b->snake.x[tail_idx]] = EMPTY;
		b->snake.length--;
	}
	else
		b->game_over = true;
	remove_apple(b, x, y, RED_APPLE);
	spawn_apple(b, RED_APPLE);
	if (b->snake.length > 0)
		move_snake(b, x, y, false);
	if (b->snake.length > 0)
		return (ATE_RED_APPLE);
	return (LENGTH_ZERO);
}
