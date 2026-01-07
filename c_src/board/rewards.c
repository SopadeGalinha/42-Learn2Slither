/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   rewards.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: jhogonca <jhogonca@student.42porto.com>    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/07 18:28:37 by jhogonca          #+#    #+#             */
/*   Updated: 2026/01/07 20:53:17 by jhogonca         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "board.h"

float	board_get_reward_green_apple(void)
{
	return (REWARD_GREEN_APPLE);
}

float	board_get_reward_red_apple(void)
{
	return (REWARD_RED_APPLE);
}

float	board_get_reward_death(void)
{
	return (REWARD_DEATH);
}

float	board_get_reward_step(void)
{
	return (REWARD_STEP);
}
