/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   board_internal.h                                   :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: jhogonca <jhogonca@student.42porto.com>    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/07 18:28:27 by jhogonca          #+#    #+#             */
/*   Updated: 2026/01/07 20:45:27 by jhogonca         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#ifndef BOARD_INTERNAL_H
# define BOARD_INTERNAL_H

# include "board.h"

void			spawn_apple(t_board *board, t_board_cell type);
void			init_apples(t_board *board);
void			remove_apple(t_board *board, int x, int y, t_board_cell type);
int				board_get_size(const t_board *board);
t_board_cell	check_cell(const t_board *board, int x, int y);
void			move_snake(t_board *board, int new_x, int new_y, bool grow);
void			board_init_grid(t_board *board);
void			board_init_snake(t_board *board);

#endif
