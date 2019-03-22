"""
Mini-max Tic-Tac-Toe Player
"""

import poc_ttt_gui
import poc_ttt_provided as provided

# Set timeout, as mini-max can take a long time
#import codeskulptor
#codeskulptor.set_timeout(60)

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
    print board, "player=", player
    check_res = board.check_win()  
    if check_res != None:  
        print check_res, "wins"
        return SCORES[check_res] , (-1,-1)  
    else:  
        empty_list = board.get_empty_squares() 
        print "empty_list=", empty_list 
        if player == provided.PLAYERX: 
            print "player x"
            max_score = -2;  
            max_each = (-1,-1)  
            changed_player = provided.switch_player(player)  
            for each in empty_list:  
                cur_board= board.clone()  
                cur_board.move(each[0], each[1], player)  
                cur_score_tuple = mm_move(cur_board, changed_player) 
                print
                print "cur_score_tuple=", cur_score_tuple
                cur_score = cur_score_tuple[0]  
                if cur_score > max_score:  
                    print "cur_score > max_score", cur_score, max_score
                    max_score = cur_score  
                    max_each = each  
                    print "max_each=", max_each
                if max_score == SCORES[provided.PLAYERX]:  
                    print "cur_score == max_score", cur_score, max_score
                    print 
                    return max_score, max_each  
            return max_score, max_each      
        elif player == provided.PLAYERO:  
            print "player o"
            min_score = 2;  
            min_each = (-1,-1)  
            changed_player = provided.switch_player(player)  
            for each in empty_list:  
                cur_board= board.clone()  
                cur_board.move(each[0], each[1], player)               
                cur_score_tuple = mm_move(cur_board, changed_player)  
                print "cur_score_tuple=", cur_score_tuple
                cur_score = cur_score_tuple[0]  
                if cur_score < min_score:  
                    print "cur_score < min_score", cur_score, min_score
                    min_score = cur_score  
                    min_each = each  
                    print "min_each=", min_each
                if min_score == SCORES[provided.PLAYERO]:  
                    print "cur_score == min_score", cur_score, min_score
                    print
                    return min_score, min_each  
            return min_score, min_each  
            

def move_wrapper(board, player, trials):
    """
    Wrapper to allow the use of the same infrastructure that was used
    for Monte Carlo Tic-Tac-Toe.
    """
    move = mm_move(board, player)
    assert move[1] != (-1, -1), "returned illegal move (-1, -1)"
    return move[1]

# Test game with the console or the GUI.
# Uncomment whichever you prefer.
# Both should be commented out when you submit for
# testing to save time.

# provided.play_game(move_wrapper, 1, False)        
# poc_ttt_gui.run_gui(3, provided.PLAYERO, move_wrapper, 1, False)
print mm_move(provided.TTTBoard(3, False, [[provided.PLAYERO, provided.PLAYERX, provided.EMPTY], [provided.PLAYERO, provided.PLAYERX, provided.EMPTY], [provided.EMPTY, provided.PLAYERO, provided.PLAYERX]]), provided.PLAYERX), "ans"
