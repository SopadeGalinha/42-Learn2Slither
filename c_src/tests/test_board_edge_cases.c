/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   test_board_edge_cases.c                            :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: jhogonca <jhogonca@student.42porto.com>    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/07 00:00:00 by jhogonca          #+#    #+#             */
/*   Updated: 2026/01/07 20:30:32 by jhogonca         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "tests.h"

static bool	test_size_too_small(void)
{
	t_board	*board;

	board = board_create(5);
	if (!check_condition(board != NULL,
			"Board should default to 10 when size < 8"))
		return (false);
	if (!check_equal(board->size, 10, "Should default to size 10"))
		return (false);
	board_destroy(board);
	return (true);
}

static bool	test_size_too_large(void)
{
	t_board	*board;

	board = board_create(50);
	if (!check_condition(board != NULL,
			"Board should default to 10 when size > 20"))
		return (false);
	if (!check_equal(board->size, 10, "Should default to size 10"))
		return (false);
	board_destroy(board);
	return (true);
}

static bool	test_size_negative(void)
{
	t_board	*board;

	board = board_create(-5);
	if (!check_condition(board != NULL, "Board should handle negative size"))
		return (false);
	if (!check_equal(board->size, 10, "Should default to size 10"))
		return (false);
	board_destroy(board);
	return (true);
}

static bool	test_size_zero(void)
{
	t_board	*board;

	board = board_create(0);
	if (!check_condition(board != NULL, "Board should handle zero size"))
		return (false);
	if (!check_equal(board->size, 10, "Should default to size 10"))
		return (false);
	board_destroy(board);
	return (true);
}

t_test_result	test_board_edge_cases(void)
{
	t_test_result	result;

	result.passed = 0;
	result.failed = 0;
	result.total = 0;
	run_test("Size too small (5)", test_size_too_small, &result);
	run_test("Size too large (50)", test_size_too_large, &result);
	run_test("Size negative (-5)", test_size_negative, &result);
	run_test("Size zero (0)", test_size_zero, &result);
	return (result);
}
