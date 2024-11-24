import numpy as np
import copy
import sys

INFINITY = 1000


def evaluate_local_board(board, X, O):
    score_line_X = 0
    score_line_O = 0
    score_cell_X = 0
    score_cell_O = 0
    # Check rows and columns
    for i in range(3):
        row_sum = np.sum(board[i, :])
        col_sum = np.sum(board[:, i])

        score_line_X += evaluate_line(row_sum, X)
        score_line_O += evaluate_line(row_sum, O)

        score_line_X += evaluate_line(col_sum, X)
        score_line_O += evaluate_line(col_sum, O)

    # Check diagonals
    diag_sum_topleft = board.trace()
    diag_sum_topright = board[::-1].trace()

    score_line_X += evaluate_line(diag_sum_topleft, X)
    score_line_X += evaluate_line(diag_sum_topright, X)

    score_line_O += evaluate_line(diag_sum_topleft, O)
    score_line_O += evaluate_line(diag_sum_topright, O)

    for i in range(3):
        for j in range(3):
            if board[i, j] == X and i == 1 and j == 1:
                score_cell_X += 2
            if board[i, j] == O and i == 1 and j == 1:
                score_cell_O += 2

            if board[i, j] == X and ((i == 0 and j == 0) or (i == 0 and j == 2) or (i == 2 and j == 0) or (i == 2 and j == 2)):
                score_cell_X += 1.5
            if board[i, j] == O and ((i == 0 and j == 0) or (i == 0 and j == 2) or (i == 2 and j == 0) or (i == 2 and j == 2)):
                score_cell_O += 1.5

            if board[i, j] == X and ((i == 0 and j == 1) or (i == 1 and j == 0) or (i == 1 and j == 2) or (i == 2 and j == 1)):
                score_cell_X += 1
            if board[i, j] == O and ((i == 0 and j == 1) or (i == 1 and j == 0) or (i == 1 and j == 2) or (i == 2 and j == 1)):
                score_cell_O += 1

    score_X = 5 * min(2, score_line_X) + score_cell_X
    score_O = 5 * min(2, score_line_O) + score_cell_O
    return score_X - score_O


def evaluate_line(line_sum, type):
    if line_sum == 2 * type:
        return 1
    return 0


def evaluate(state, prev_state):
    # Heuristic evaluation of the state
    score_micro_current = 0
    score_micro_previous = 0

    score_macro_current = 0
    score_macro_previous = 0
    # print ("------------    ---------------")
    # print(state.blocks)

    # print ("------------    ---------------")
    # print(prev_state.blocks)
    # print ("------------    ---------------")
    # return 0

    local_board_check = state.previous_move.index_local_board
    score_micro_current = evaluate_local_board(
        state.blocks[local_board_check], state.X, state.O)
    score_micro_previous = evaluate_local_board(
        prev_state.blocks[local_board_check], state.X, state.O)

    # print("Delta", score_micro_current - score_micro_previous)
    # exit()
    score_macro_current = evaluate_local_board(
        state.global_cells.reshape(3, 3), state.X, state.O)
    score_macro_previous = evaluate_local_board(
        prev_state.global_cells.reshape(3, 3), state.X, state.O)

    # print("Current", state.blocks[local_board_check])
    # print("Prev", prev_state.blocks[local_board_check])
    # print ("Micro curent", score_micro_current)
    # print ("Micro previous", score_micro_previous)
    # print ("Macro curent", score_macro_current)
    # print ("Macro previous", score_macro_previous)
    # exit()

    Rt = 0
    if state.game_result(state.global_cells.reshape(3, 3)) == state.X:
        Rt = 400
    elif state.game_result(state.global_cells.reshape(3, 3)) == state.O:
        Rt = -400
    elif np.any(state.global_cells != prev_state.global_cells):
        Rt = score_macro_current - score_macro_previous
    else:
        Rt = (score_micro_current - score_micro_previous) * \
            (score_macro_current - score_macro_previous)
    # print(Rt)

    for cell in state.global_cells:
        if cell == state.X:
            Rt += 10
        elif cell == state.O:
            Rt -= 10
    return Rt


def minimax(state, prev_state, depth, cumulated_reward=0, maximize_player=True):
    if depth == 0 or state.game_over:
        # print (state, prev_state)

        # exit()
        return cumulated_reward, None
    
    moves = state.get_valid_moves
    # print("DEBUG---------------------------------------")
    # for debug in moves:
    #     print(debug)
    # # print("depth", depth)
    # print("state previous move", state.previous_move)
    # print("DEBUG---------------------------------------\n")

    if (len(moves) == 0):
        return cumulated_reward, None

    if (len(moves) > 9):
        newDepth = max(0, depth - 2)
    else:
        newDepth = depth - 1

    if maximize_player:
        best_score = -INFINITY
        best_move = None
        for move in moves:
            state_copy = copy.deepcopy(state)
            prev_state = state
            state_copy.act_move(move)
            reward = evaluate(state_copy, prev_state)
            eval, _ = minimax(state_copy, prev_state, newDepth,
                              cumulated_reward + reward, False)
            if eval > best_score:
                best_score = eval
                best_move = move
        return best_score, best_move
    else:
        best_score = INFINITY
        best_move = None
        for move in moves:
            state_copy = copy.deepcopy(state)
            prev_state = state
            state_copy.act_move(move)
            reward = evaluate(state_copy, prev_state)
            eval, _ = minimax(state_copy, prev_state, newDepth,
                              cumulated_reward + reward, True)
            if eval < best_score:
                best_score = eval
                best_move = move
        return best_score, best_move


cnt = 0
go_first = True


def select_move(cur_state, remain_time):
    global cnt, go_first
    if cnt == 0:
        cnt += 1
        if cur_state.player_to_move == cur_state.X:
            go_first = True
        else:
            go_first = False
    depth = 4
    eval, best_move = minimax(cur_state, cur_state,
                              depth, maximize_player=go_first)

    return best_move
