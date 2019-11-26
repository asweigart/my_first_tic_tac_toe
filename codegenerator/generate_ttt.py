# This script is... less than ideal.
# It was cobbled together just to one-off generate the tictactoe.py file.

# This is a Python 3 script which generates a Python 3 script.

# Seriously, this code is not at all polished and I tinkered with it for a couple hours just to get it to output right. That did not improve things, code readability-wise.

import logging
logging.basicConfig(level=logging.DEBUG)
logging.disable(logging.CRITICAL)

import copy
import random

boardTemplate = """print('%s|%s|%s\\n-+-+-\\n%s|%s|%s\\n-+-+-\\n%s|%s|%s\\n')"""

enterMoveMessage = """print('Enter the number of your move:')
print('  789\\n  456\\n  123')"""

'''
boardTemplate = """print('   |   |   ')
print(' %s | %s | %s ')
print('   |   |   ')
print('---+---+---')
print('   |   |   ')
print(' %s | %s | %s ')
print('   |   |   ')
print('---+---+---')
print('   |   |   ')
print(' %s | %s | %s ')
print('   |   |   \\n')
"""

enterMoveMessage = """print('Enter the number of your move:')
print('  7|8|9')
print('  -+-+-')
print('  4|5|6')
print('  -+-+-')
print('  1|2|3')"""
'''

# ===== start of copy-pasted tic tac toe code =======================
def isWinner(bo, le):
    # Given a board and a player's letter, this function returns True if that player has won.
    # We use bo instead of board and le instead of letter so we don't have to type as much.
    return ((bo[7] == le and bo[8] == le and bo[9] == le) or # across the top
    (bo[4] == le and bo[5] == le and bo[6] == le) or # across the middle
    (bo[1] == le and bo[2] == le and bo[3] == le) or # across the bottom
    (bo[7] == le and bo[4] == le and bo[1] == le) or # down the left side
    (bo[8] == le and bo[5] == le and bo[2] == le) or # down the middle
    (bo[9] == le and bo[6] == le and bo[3] == le) or # down the right side
    (bo[7] == le and bo[5] == le and bo[3] == le) or # diagonal
    (bo[9] == le and bo[5] == le and bo[1] == le)) # diagonal


def isSpaceFree(board, move):
    # Return true if the passed move is free on the passed board.
    return board[move] == ' '


def chooseRandomMoveFromList(board, movesList):
    # Returns a valid move from the passed list on the passed board.
    # Returns None if there is no valid move.
    possibleMoves = []
    for i in movesList:
        if isSpaceFree(board, i):
            possibleMoves.append(i)

    if len(possibleMoves) != 0:
        return random.choice(possibleMoves)
    else:
        return None

def getComputerMove(board, computerLetter):
    # Given a board and the computer's letter, determine where to move and return that move.
    if computerLetter == 'X':
        playerLetter = 'O'
    else:
        playerLetter = 'X'

    # Here is our algorithm for our Tic Tac Toe AI:
    # First, check if we can win in the next move
    for i in range(1, 10):
        boardCopy = copy.copy(board)
        if isSpaceFree(boardCopy, i):
            boardCopy[i] = computerLetter
            if isWinner(boardCopy, computerLetter):
                return i

    # Check if the player could win on their next move, and block them.
    for i in range(1, 10):
        boardCopy = copy.copy(board)
        if isSpaceFree(boardCopy, i):
            boardCopy[i] = playerLetter
            if isWinner(boardCopy, playerLetter):
                return i

    # Try to take one of the corners, if they are free.
    move = chooseRandomMoveFromList(board, [1, 3, 7, 9])
    if move != None:
        return move

    # Try to take the center, if it is free.
    if isSpaceFree(board, 5):
        return 5

    # Move on one of the sides.
    return chooseRandomMoveFromList(board, [2, 4, 6, 8])

def isBoardFull(board):
    # Return True if every space on the board has been taken. Otherwise return False.
    for i in range(1, 10):
        if isSpaceFree(board, i):
            return False
    return True

# ===== end of copy-pasted tic tac toe code =======================



allComputerMoveMessages = ['',
"print('O moves on the bottom-left space.')",
"print('O moves on the bottom-center space.')",
"print('O moves on the bottom-right space.')",
"print('O moves on the left space.')",
"print('O moves on the center space.')",
"print('O moves on the right space.')",
"print('O moves on the top-left space.')",
"print('O moves on the top-center space.')",
"print('O moves on the top-right space.')",
]

def getPrintedBoard(board, indent):
    printedBoard = boardTemplate % (board[7], board[8], board[9], board[4], board[5], board[6], board[1], board[2], board[3])
    printedBoard = printedBoard.replace('\n', '\n' + ('    ' * indent))
    printedBoard = ('    ' * indent) + printedBoard # add indent to first line
    return printedBoard

def getPrintedMoveMessage(indent):
    printedMessage = enterMoveMessage .replace('\n', '\n' + ('    ' * indent))
    printedMessage = ('    ' * indent) + printedMessage # add indent to first line
    return printedMessage

def printMove(originalBoard, indent=0):
    for move in range(1, 10):
        board = copy.copy(originalBoard)

        if not isSpaceFree(board, move):
            logging.debug('skipping %s' % (move))
            continue

        print('    ' * indent + "if move == '%s':" % (move))
        #if computerMoveMsg != '':
        #    print('    ' * (indent+1) + computerMoveMsg)
        #import pdb; pdb.set_trace()

        #print(getPrintedBoard(board, indent))

        logging.debug('moving on %s' % (move))
        board[move] = 'X'

        if isWinner(board, 'X'):
            print(getPrintedBoard(board, (indent+1)))
            print('    ' * (indent+1) + "print('You have won!')")
            print('    ' * (indent+1) + "sys.exit()")
            continue

        if isBoardFull(board):
            logging.debug('board full')
            print(getPrintedBoard(board, (indent+1)))
            print('    ' * (indent+1) + "print('It\\'s a tie!')")
            print('    ' * (indent+1) + "sys.exit()")
            continue

        compMove = getComputerMove(board, 'O')
        board[compMove] = 'O'
        if isWinner(board, 'O'):
            print('    ' * (indent+1) + allComputerMoveMessages[compMove])
            print(getPrintedBoard(board, (indent+1)))
            print('    ' * (indent+1) + "print('The computer wins!')")
            print('    ' * (indent+1) + "sys.exit()")
            continue

        print('    ' * (indent+1) + allComputerMoveMessages[compMove])

        print(getPrintedBoard(board, indent + 1))
        print(getPrintedMoveMessage(indent + 1))
        print('    ' * (indent+1) + "move = input()\n")
        #printMove(copy.copy(board), indent + 1, allComputerMoveMessages[compMove])
        printMove(copy.copy(board), indent + 1)


print('''# My first tic-tac-toe program, by Al Sweigart al@inventwithpython.com
# This sure was a lot of typing, but I finally finished it!

# (This is a joke program.)

import sys
if sys.version_info[0] == 2:
    input = raw_input # python 2 compatibility
print('Welcome to Tic Tac Toe!')
print('You are X.\\n')
''')

board = [' '] * 10
print(getPrintedBoard(board, 0))
print(getPrintedMoveMessage(0))
print("move = input()\n")
printMove(board, 0)
