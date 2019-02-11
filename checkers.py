'''
Shawn Nehemiah Chua
CS550-Assignment 3
817662151
checkers.py
'''

import time
import datetime
import ai
import checkerboard
from copy import deepcopy
# tonto - Professor Roch's not too smart strategy
# You are not given source code to this, but compiled .pyc files
# are available for Python 3.5 and 3.6 (fails otherwise).
# This will let you test some of your game logic without having to worry
# about whether or not your AI is working and let you pit your player
# against another computer player.
#
# Decompilation is cheating, don't do it.
#import tonto

# human - human player, prompts for input    
import human
import boardlibrary # might be useful for debuggingimport tontozz
import imp
import sys
major = sys.version_info[0]
minor = sys.version_info[1]
modpath = "__pycache__/tonto.cpython-{}{}.pyc".format(major, minor)
tonto = imp.load_compiled("tonto", modpath)

def elapsed(earlier, later):
    """elapsed - Convert elapsed time.time objects to duration string
    
    Useful for tracking move and game time.  Example pseudocode:
    
    gamestart = time.time()
    
    while game not over:
        movestart = time.time()
        ...  logic ...
        current = time.time() 
        print("Move time: {} Game time: {}".format(
            elapsed(movestart, current), elapsed(gamestart, current))
    
    
    """
    return time.strftime('%H:%M:%S', time.gmtime(later - earlier))
           

def Game(red=human.Strategy, black=ai.Strategy, maxplies=8, init=None, verbose=True, firstmove=0):
    """Game(red, black, maxplies, init, verbose, turn)
    Start a game of checkers
    red,black - Strategy classes (not instances)
    maxplies - # of turns to explore (default 10)
    init - Start with given board (default None uses a brand new game)
    verbose - Show messages (default True)
    firstmove - Player N starts 0 (red) or 1 (black).  Default 0. 
    """
    # Don't forget to create instances of your strategy,
    # e.g. black('b', checkerboard.CheckerBoard, maxplies)

    turns = 0
    if init is None:
        board = checkerboard.CheckerBoard()
    else: 
        board = init
    red_Player = red('r', board, maxplies)
    black_Player = black('b', board, maxplies)
    while not board.is_terminal()[0] and turns < 40:
        board.update_counts()
        #if red is first
        if firstmove == 0:
            board.update_counts()
            [board, red] = red_Player.play(board)    
            print(board)
            if red is None: #Player forfeits
                print("Red player forfeits. Black player WON!!!")
                break
            [board, black] = black_Player.play(board)
            print(board)
            board.update_counts()
            
        elif firstmove == 1:
            [board2, black] = black_Player.play(board)
            print(board2)
            [board1, red] = red_Player.play(board2)    
            print(board1)
            board = board1
        turns += 1
        if board.is_terminal()[0]:
            #game is finish
            print (board.is_terminal()[1],'WINNER')
            break
        if turns == 40:
            print('DRAW!!')
            break

if __name__ == "__main__":
    Game()   
                    
            
        

    
    
