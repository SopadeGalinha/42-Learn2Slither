/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   tests.h                                            :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: jhogonca <jhogonca@student.42porto.com>    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/07 00:00:00 by jhogonca          #+#    #+#             */
/*   Updated: 2026/01/07 17:59:23 by jhogonca         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#ifndef TESTS_H
# define TESTS_H

# include <stdio.h>
# include <stdbool.h>
# include "../board/board.h"

/* Color codes */
# define COLOR_GREEN "\033[32m"
# define COLOR_RED "\033[31m"
# define COLOR_RESET "\033[0m"

typedef struct s_test_result
{
	int	passed;
	int	failed;
	int	total;
}	t_test_result;

/* Test runners */
t_test_result	test_board_creation(void);
t_test_result	test_board_edge_cases(void);
t_test_result	test_board_validation(void);
t_test_result	test_board_memory(void);

/* Helper functions */
bool			check_condition(bool cond, const char *msg);
bool			check_equal(int a, int b, const char *msg);
void			run_test(const char *n, bool (*f)(void), t_test_result *r);

#endif
