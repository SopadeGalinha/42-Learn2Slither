/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   test_board_creation.c                              :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: jhogonca <jhogonca@student.42porto.com>    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/07 00:00:00 by jhogonca          #+#    #+#             */
/*   Updated: 2026/01/07 20:30:32 by jhogonca         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "tests.h"

static bool	test_board_create_default(void)
{
	t_board	*board;

	board = board_create(10);
	if (!check_condition(board != NULL, "Board allocation failed"))
		return (false);
	if (!check_equal(board->size, 10, "Board size mismatch"))
		return (false);
	if (!check_equal(board->snake.length, 3, "Snake length not 3"))
		return (false);
	board_destroy(board);
	return (true);
}

static bool	test_board_destroy_valid(void)
{
	t_board	*board;

	board = board_create(10);
	if (!check_condition(board != NULL, "Board allocation failed"))
		return (false);
	board_destroy(board);
	return (true);
}

static bool	test_board_create_max_size(void)
{
	t_board	*board;

	board = board_create(20);
	if (!check_condition(board != NULL, "Board allocation failed"))
		return (false);
	if (!check_equal(board->size, 20, "Max size not set correctly"))
		return (false);
	board_destroy(board);
	return (true);
}

static bool	test_board_create_min_size(void)
{
	t_board	*board;

	board = board_create(8);
	if (!check_condition(board != NULL, "Board allocation failed"))
		return (false);
	if (!check_equal(board->size, 8, "Min size not set correctly"))
		return (false);
	board_destroy(board);
	return (true);
}

t_test_result	test_board_creation(void)
{
	t_test_result	result;

	result.passed = 0;
	result.failed = 0;
	result.total = 0;
	run_test("Create board size 10", test_board_create_default, &result);
	run_test("Destroy board", test_board_destroy_valid, &result);
	run_test("Create max size (20)", test_board_create_max_size, &result);
	run_test("Create min size (8)", test_board_create_min_size, &result);
	return (result);
}
