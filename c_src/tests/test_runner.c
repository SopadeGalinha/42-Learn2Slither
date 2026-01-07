/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   test_runner.c                                      :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: jhogonca <jhogonca@student.42porto.com>    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/07 00:00:00 by jhogonca          #+#    #+#             */
/*   Updated: 2026/01/07 18:02:38 by jhogonca         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "tests.h"

static void	print_section(const char *name)
{
	printf("\n╔════════════════════════════════════════╗\n");
	printf("║ %-38s ║\n", name);
	printf("╚════════════════════════════════════════╝\n");
}

static void	print_summary(t_test_result res)
{
	printf("  Total: %d | Passed: %d | Failed: %d\n",
		res.total, res.passed, res.failed);
}

static void	run_section(t_test_result (*fn)(void), const char *name,
		t_test_result *all)
{
	t_test_result	res;

	print_section(name);
	res = fn();
	print_summary(res);
	all->passed += res.passed;
	all->failed += res.failed;
	all->total += res.total;
}

static void	run_all_tests(t_test_result *all)
{
	run_section(test_board_creation, "Test: Board Creation", all);
	run_section(test_board_edge_cases, "Test: Edge Cases", all);
	run_section(test_board_validation, "Test: Board Validation", all);
	run_section(test_board_memory, "Test: Memory & Stress", all);
}

int	main(void)
{
	t_test_result	all;

	all.passed = 0;
	all.failed = 0;
	all.total = 0;
	printf("╔════════════════════════════════════════╗\n");
	printf("║   LEARN2SLITHER - C TEST SUITE        ║\n");
	printf("╚════════════════════════════════════════╝\n");
	run_all_tests(&all);
	printf("\n╔════════════════════════════════════════╗\n");
	printf("║   FINAL RESULTS                       ║\n");
	printf("║   Total: %d | Passed: %d | Failed: %d ║\n",
		all.total, all.passed, all.failed);
	printf("╚════════════════════════════════════════╝\n\n");
	if (all.failed != 0)
		return (1);
	return (0);
}
