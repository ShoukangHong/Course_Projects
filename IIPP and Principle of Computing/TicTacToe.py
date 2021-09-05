"""
Mini-max Tic-Tac-Toe Player
"""

import poc_ttt_gui
import poc_ttt_provided as provided

# Set timeout, as mini-max can take a long time
import codeskulptor
codeskulptor.set_timeout(60)

# SCORING VALUES - DO NOT MODIFY
SCORES = {provided.PLAYERX: 1,
          provided.DRAW: 0,
          provided.PLAYERO: -1}

def mm_move(board, player):
    """
    Make a move on the board.
    Returns a tuple with two elements.  The first element is the score
    of the given board and the second element is the desired move as a
    tuple, (row, col).
    """
    state = board.check_win()
    if state != None:
        return SCORES[state], (-1, -1)
    moves = board.get_empty_squares()
    new_boards = []
    switch = provided.switch_player(player)
    for move in moves:
        new_board = board.clone()
        new_board.move(move[0], move[1], player)
        score_pos = mm_move(new_board, switch)
        #print score_pos[0], move
        #print str(new_board)
        if player == provided.PLAYERX and score_pos[0] == SCORES[provided.PLAYERX]:
            return score_pos[0], move
        elif player == provided.PLAYERO and score_pos[0] == SCORES[provided.PLAYERO]:
            return score_pos[0], move  
        new_boards.append((score_pos[0], move))
    new_boards = sorted(new_boards, key = lambda item: item[0])
#    print new_boards
    if player == provided.PLAYERX:
        return new_boards[-1]
    else:
        return new_boards[0]

def move_wrapper(board, player, trials):
    """
    Wrapper to allow the use of the same infrastructure that was used
    for Monte Carlo Tic-Tac-Toe.
    """
#    board._board =[[provided.PLAYERX, provided.PLAYERX, provided.PLAYERO],
#                   [provided.PLAYERO, provided.PLAYERX, provided.EMPTY],
#                   [provided.EMPTY, provided.PLAYERO, provided.EMPTY]]
    move = mm_move(board, player)
    assert move[1] != (-1, -1), "returned illegal move (-1, -1)"
    return move[1]

# Test game with the console or the GUI.
# Uncomment whichever you prefer.
# Both should be commented out when you submit for
# testing to save time.

#provided.play_game(move_wrapper, 1, False)
#poc_ttt_gui.run_gui(3, provided.PLAYERO, move_wrapper, 1, False)
#test = provided.TTTBoard(3)
#test._board =[[provided.PLAYERX, provided.EMPTY, provided.PLAYERO],
#               [provided.EMPTY, provided.PLAYERX, provided.EMPTY],
#               [provided.EMPTY, provided.EMPTY, provided.EMPTY]]
#print str(test)
#print 'result' + str(mm_move(test, provided.PLAYERO))