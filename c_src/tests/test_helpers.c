/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   test_helpers.c                                     :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: jhogonca <jhogonca@student.42porto.com>    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/07 00:00:00 by jhogonca          #+#    #+#             */
/*   Updated: 2026/01/07 17:54:31 by jhogonca         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "tests.h"

bool	check_condition(bool cond, const char *msg)
{
	if (!cond)
		printf("  " COLOR_RED "✗" COLOR_RESET " %s\n", msg);
	return (cond);
}

bool	check_equal(int a, int b, const char *msg)
{
	if (a != b)
	{
		printf("  " COLOR_RED "✗" COLOR_RESET " %s (expected %d, got %d)\n",
			msg, b, a);
		return (false);
	}
	return (true);
}

void	run_test(const char *name, bool (*test_fn)(void), t_test_result *result)
{
	printf("  Testing: %s...", name);
	if (test_fn())
	{
		printf(" " COLOR_GREEN "✓" COLOR_RESET "\n");
		result->passed++;
	}
	else
	{
		printf(" " COLOR_RED "✗" COLOR_RESET "\n");
		result->failed++;
	}
	result->total++;
}
