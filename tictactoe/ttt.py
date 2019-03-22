"""
Monte Carlo Tic-Tac-Toe Player
"""

import random
import poc_ttt_gui
import poc_ttt_provided as provided


# Constants for Monte Carlo simulator
# You may change the values of these constants as desired, but
#  do not change their names.

NTRIALS = 10  # Number of trials to run
SCORE_CURRENT = 1.0  # Score for squares played by the current player
SCORE_OTHER = 1.0  # Score for squares played by the other player
SCORE_EMPTY = 0.0


# Add your functions here.

def mc_trial(board, player):
    """
    Monte Carlo trial by random move and player switch.
    """
    while board.check_win() == None:
        next_square = random.choice(board.get_empty_squares())
        board.move(next_square[0], next_square[1], player)
        player = provided.switch_player(player)
    print board


# board = provided.TTTBoard(3, False, None)

def mc_update_scores(scores, board, player):
    """
    Square score calculation.
    """
    player_score, com_score = 0, 0
    if board.check_win() == provided.DRAW:
        print "tie"
    elif board.check_win() == player:
        print "x win"
        player_score = SCORE_CURRENT
        com_score = -SCORE_OTHER
    else:
        print "o win"
        player_score = -SCORE_CURRENT
        com_score = SCORE_OTHER
    for _row in range(board.get_dim()):
        for _col in range(board.get_dim()):
            if board.square(_row, _col) == provided.EMPTY:
                scores[_row][_col] += SCORE_EMPTY
            elif board.square(_row, _col) == player:
                scores[_row][_col] += player_score
            else:
                scores[_row][_col] += com_score

    print "update_score=", scores


def get_best_move(board, scores):
    """
    Define best next move by max score.
    """
    empty_square, best_square, best_move = [], [], ()
    # Find the max score of all board
    for _row in range(board.get_dim()):
        for _col in range(board.get_dim()):
            if board.square(_row, _col) == provided.EMPTY:
                empty_square.append(scores[_row][_col])
                max_score = max(empty_square)
    # Decide collection of best square
    for _row in range(board.get_dim()):
        for _col in range(board.get_dim()):
            if board.square(_row, _col) == provided.EMPTY and max_score == scores[_row][_col]:
                best_square.append([_row, _col])
    print "best_square=", best_square
    best_square = random.choice(best_square)
    best_move = (best_square[0], best_square[1])
    print "best_move=", best_move
    return best_move


def mc_move(board, player, trials):
    """
    AI plays best next move based on number of Monte Carlo trials.
    """
    scores = [[0 for dummy_col in range(board.get_dim())] for dummy_row in range(board.get_dim())]
    print "current board"
    print board
    for dummy in range(trials):
        print "num of iter=", dummy + 1
        board1 = board.clone()
        mc_trial(board1, player)
        mc_update_scores(scores, board1, player)
    return get_best_move(board, scores)


# Test game with the console or the GUI.  Uncomment whichever
# you prefer.  Both should be commented out when you submit
# for testing to save time.

# provided.play_game(mc_move, NTRIALS, False)
# mc_move(provided.TTTBoard(2, False, [[provided.EMPTY, provided.EMPTY], [provided.EMPTY, provided.EMPTY]]), provided.PLAYERX, provided.NTRIALS)
# get_best_move(provided.TTTBoard(2, False, [[provided.EMPTY, provided.EMPTY], [provided.EMPTY, provided.EMPTY]]), [[0, 0], [3, 0]])
# Player X always starts first
poc_ttt_gui.run_gui(3, provided.PLAYERX, mc_move, NTRIALS, False)
# mc_move(provided.TTTBoard(3, False, [[provided.PLAYERX, provided.EMPTY, provided.EMPTY], [provided.PLAYERO, provided.PLAYERO, provided.EMPTY], [provided.EMPTY, provided.PLAYERX, provided.EMPTY]]), provided.PLAYERX, NTRIALS)