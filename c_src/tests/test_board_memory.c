/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   test_board_memory.c                                :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: jhogonca <jhogonca@student.42porto.com>    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/07 00:00:00 by jhogonca          #+#    #+#             */
/*   Updated: 2026/01/07 20:31:00 by jhogonca         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "tests.h"

static bool	test_multiple_create_destroy(void)
{
	t_board	*board;
	int		i;

	i = 0;
	while (i < 100)
	{
		board = board_create(10 + (i % 11));
		if (board == NULL)
			return (false);
		board_destroy(board);
		i++;
	}
	return (true);
}

static bool	test_board_null_destroy(void)
{
	board_destroy(NULL);
	return (true);
}

static bool	test_board_allocation_sizes(void)
{
	t_board	*board;
	int		sizes[4];

	sizes[0] = 8;
	sizes[1] = 10;
	sizes[2] = 15;
	sizes[3] = 20;
	board = board_create(sizes[0]);
	if (board == NULL)
		return (false);
	board_destroy(board);
	return (true);
}

static bool	test_board_state_consistency(void)
{
	t_board	*board;

	board = board_create(15);
	if (!check_condition(board != NULL, "Board creation failed"))
		return (false);
	if (!check_equal(board->size, 15, "Size mismatch"))
		return (false);
	board_destroy(board);
	return (true);
}

t_test_result	test_board_memory(void)
{
	t_test_result	result;

	result.passed = 0;
	result.failed = 0;
	result.total = 0;
	run_test("Multiple create/destroy", test_multiple_create_destroy, &result);
	run_test("Null destroy", test_board_null_destroy, &result);
	run_test("Allocation sizes", test_board_allocation_sizes, &result);
	run_test("State consistency", test_board_state_consistency, &result);
	return (result);
}
