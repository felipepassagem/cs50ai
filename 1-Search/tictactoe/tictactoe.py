"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None

se_x_ganhar = []
se_o_ganhar = []
se_empate = []

def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]




def OWins(board):
    #diagonal esq-dir
    OWin = False
    if board[0][0] == "O" and board[1][1] == "O" and board[2][2] == "O":
        OWin = True
    #diag dir -esq
    elif board[0][2] == "O" and board[1][1] == "O" and board[2][0] == "O":
        OWin = True
    #linha cima
    elif board[0][0] == "O" and board[0][1] == "O" and board[0][2] == "O":
        OWin = True
    #linha meio
    elif board[1][0] == "O" and board[1][1] == "O" and board[1][2] == "O":
        OWin = True
    #linha baixo
    elif board[2][0] == "O" and board[2][1] == "O" and board[2][2] == "O":
        OWin = True
    #coluna 0
    elif board[0][0] == "O" and board[1][0] == "O" and board[2][0] == "O":
        OWin = True
    #col 1
    elif board[0][1] == "O" and board[1][1] == "O" and board[2][1] == "O":
        OWin = True
    #col2
    elif board[0][2] == "O" and board[1][2] == "O" and board[2][2] == "O":
        OWin = True
    return OWin

def XWins(board):
    Xwin = False
    #diagonal esq-dir
    if board[0][0] == "X" and board[1][1] == "X" and board[2][2] == "X":
        Xwin = True
    #diag dir -esq
    elif board[0][2] == "X" and board[1][1] == "X" and board[2][0] == "X":
        Xwin = True
    #linha cima
    elif board[0][0] == "X" and board[0][1] == "X" and board[0][2] == "X":
        Xwin = True
    #linha meio
    elif board[1][0] == "X" and board[1][1] == "X" and board[1][2] == "X":
        Xwin = True
    #linha baixo
    elif board[2][0] == "X" and board[2][1] == "X" and board[2][2] == "X":
        Xwin = True
    #coluna 0
    elif board[0][0] == "X" and board[1][0] == "X" and board[2][0] == "X":
        Xwin = True
    #col 1
    elif board[0][1] == "X" and board[1][1] == "X" and board[2][1] == "X":
        Xwin = True
    #col2
    elif board[0][2] == "X" and board[1][2] == "X" and board[2][2] == "X":
        Xwin = True
    return Xwin

def fullBoard(board):
    for row in board:
        for el in row:
            if el == EMPTY:
                return False
    return True





def player(board):
    """
    Returns player who has the next turn on a board.
    """
    player = X
    contX = 0
    contO = 0

    for row in board:
        for el in row:
            if el == O:
                contO += 1
            elif el == X:
                contX +=1
        
    if contO < contX:
        player = O
        
    return player


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    legalMoves = []
    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] == None:
                legalMoves.append((i, j))
    return legalMoves


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    p = player(board)
    new_board = copy.deepcopy(board)
    new_board[action[0]][action[1]] = p
    return new_board
    


   


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    if XWins(board):
        return X
    if OWins(board):
        return O
    return None
    


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if OWins(board) or XWins(board) or fullBoard(board):
        return True
    return False
       


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if OWins(board):
        return -1
    if XWins(board):
        return 1
    if fullBoard(board):
        return 0
    
def maxValue(board):
    a = actions(board)
    if terminal(board):
        v = utility(board)
        return v
    v = float("-inf")
    
    for action in a:
        temp = result(board, action)
        v = max(v, minValue(temp))
    return v
    
def minValue(board):
    a = actions(board)
    if terminal(board):
        v = utility(board)
        return v
    v = float("inf")
    
    for action in a:
        temp = result(board, action)
        v = min(v, maxValue(temp))
    return v

    
def copyBoard(board):
    copy_board = []
    for row in board:
        temp = []
        for el in row:
            temp.append(el)
        copy_board.append(temp)

    return copy_board

def undoMove(board, action):
     
    print(action)
    board[action[0]][action[1]] = EMPTY
    
    return board

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    # res = []
    # checked = []
    p = player(board)
    a = actions(board)
    copy_board = copyBoard(board)

    

    if terminal(board):
        return None
    
    if p == "X":
        ref = float("-inf")
        melhor_acao = None
        for action in a:
            temp = result(copy_board, action)
            valor_acao = minValue(temp)
            if valor_acao > ref:
                ref = valor_acao
                melhor_acao = action
        return melhor_acao

    else:
        ref = float("inf")
        melhor_acao = None
        for action in a:
            temp = result(copy_board, action)
            valor_acao = maxValue(temp)
            if valor_acao < ref:
                ref = valor_acao
                melhor_acao = action
            
        
        return melhor_acao



###############################






    


    
