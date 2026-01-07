/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   test_board_validation.c                            :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: jhogonca <jhogonca@student.42porto.com>    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/07 00:00:00 by jhogonca          #+#    #+#             */
/*   Updated: 2026/01/07 20:31:07 by jhogonca         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "tests.h"

static bool	test_board_snake_initialized(void)
{
	t_board	*board;
	int		x;
	int		y;

	board = board_create(10);
	x = board->snake.x[board->snake.head_idx];
	y = board->snake.y[board->snake.head_idx];
	if (!check_condition(x >= 0 && x < 10, "Snake head X out of bounds"))
		return (false);
	if (!check_condition(y >= 0 && y < 10, "Snake head Y out of bounds"))
		return (false);
	board_destroy(board);
	return (true);
}

static bool	test_board_apples_count(void)
{
	t_board	*board;

	board = board_create(10);
	if (!check_equal(board->num_green_apples, 2, "Green apples count wrong"))
		return (false);
	if (!check_equal(board->num_red_apples, 1, "Red apples count wrong"))
		return (false);
	board_destroy(board);
	return (true);
}

static bool	test_board_reset(void)
{
	t_board	*board;

	board = board_create(10);
	board_reset(board);
	if (!check_equal(board->score, 0, "Score not reset"))
		return (false);
	if (!check_equal(board->moves, 0, "Moves not reset"))
		return (false);
	board_destroy(board);
	return (true);
}

static bool	test_board_game_not_over_initially(void)
{
	t_board	*board;

	board = board_create(10);
	if (!check_condition(board_is_game_over(board) == false,
			"Game should not be over"))
		return (false);
	board_destroy(board);
	return (true);
}

t_test_result	test_board_validation(void)
{
	t_test_result	result;

	result.passed = 0;
	result.failed = 0;
	result.total = 0;
	run_test("Snake initialized", test_board_snake_initialized, &result);
	run_test("Apples count correct", test_board_apples_count, &result);
	run_test("Board reset", test_board_reset, &result);
	run_test("Game not over initially", test_board_game_not_over_initially,
		&result);
	return (result);
}
