# -*- coding: utf-8 -*-
"""
Created on Mon May 13 16:56:50 2019

@author: Callum
"""

import numpy as np
from random import randint as rnd
from random import uniform



aiValue = np.ones(shape=(3,3), dtype=float)
scoreBoard = np.zeros(shape=(3,3), dtype=int)

board = np.full((3,3), ' ')
player = True

#player input module
def PlayerInput():
    playerY = int(input('Enter the vertical (y) coordinate of your chosen position (0-2) : '))
    while playerY > 2 or playerY < 0:
        playerY = int(input('Enter the vertical (y) coordinate of your chosen position (0-2) : '))
        
    playerX = int(input('Enter the horizontal (x) coordinate of your chosen position (0-2) : '))
    while playerX > 2 or playerX < 0:
        playerX = int(input('Enter the horizontal (x) coordinate of your chosen position (0-2) : '))

    return playerX, playerY

def UpdateBoard(Y, X, board, player):
    
    if player:
        board[Y][X] = 'X'
    else:
        board[Y][X] = 'O'
        Display(board)
        
    
def UpdateValues(aiValue, board):
    
    '''
    This procedure is the main bulk of the AI that works with the AI function.
    This procedure valuates each position on the board, based on the location
    of entities. This valuation algorithm is based on attempting to stalemate
    the game, or win the game through directly attacking the player.
    
    '''
    
    #This first loop valuates each position on the game board initially
    for i in range(0, 3):
        for j in range(0, 3):

            if board[i,j] == 'X': # unplaying a taken spot by player
                aiValue[i,j] = -1000
            elif board[i,j] == 'O':
                aiValue[i,j] = -1200 # unplaying a taken spot by AI
            
            if i+1 <=2:
                if board[i+1,j] == 'X': # boosting the above spot
                    aiValue[i,j] += 7 + uniform(4.5, 5.5)
                if board[i+1,j] == 'O':
                    aiValue[i,j] += 5 + uniform(4.5, 5.5)
                    
            if i-1 >= 0:        
                if board[i-1,j] == 'X': # boosting the below spot
                    aiValue[i,j] += 7 + uniform(4.5, 5.5)
                if board[i-1,j] == 'O':
                    aiValue[i,j] += 5 + uniform(4.5, 5.5)

            if j+1 <= 2:
                if board[i,j+1] == 'X': # boosting the left spot
                    aiValue[i,j] += 7 + uniform(4.5, 5.5)
                if board[i,j+1] == 'O':
                    aiValue[i,j] += 5 + uniform(4.5, 5.5)
        
            if j-1 >= 0:
                if board[i,j-1] == 'X': # boosting the right spot
                    aiValue[i,j] += 7 + uniform(4.5, 5.5)
                if board[i,j-1] == 'O':
                    aiValue[i,j] += 7 + uniform(4.5, 5.5)
    
    for i in range(0,3): # vertical index
        for j in range(0,3): # horizontal index
            
            if j-2 == 0:
                if board[i,j-2] == 'X' and board[i,j-1] == 'X' and board[i,j] == ' ':
                    aiValue[i,j] = aiValue[i,j] * 2 # boosting the end of a full row
                    
            if j == 0 and board[i,j+1] == 'X' and board[i,j+2] == 'X' and board[i,j] == ' ':
                aiValue[i,j] = aiValue[i,j] * 2 # boosting the start of a full row
                
            if i-2 == 0:
                if board[i-2,j] == 'X' and board[i-1,j] == 'X' and board[i,j] == ' ':
                    aiValue[i,j] = aiValue[i,j] * 2 # boosting the end of a full column
            
            if i == 0 and board[i+1,j] == 'X' and board[i+2,j] == 'X' and board[i,j] == ' ':
                aiValue[i,j] = aiValue[i,j] * 2 # boosting the start of a full column
            
            
            
            if i == 1: 
                if board[i-1,j] == 'X' and board[i+1, j] == 'X':
                    aiValue[i,j] = aiValue[i,j] * 3
                if board[i-1,j] == 'O' and board[i+1, j] == 'O':
                    aiValue[i,j] = aiValue[i,j] * 4
            if j == 1:
                if board[i,j-1] == 'X' and board[i,j+1] == 'X':
                    aiValue[i,j] = aiValue[i,j] * 3
                if board[i,j-1] == 'O' and board[i,j+1] == 'O':
                    aiValue[i,j] = aiValue[i,j] * 4
            



def ArtificialIntelligence(aiValue, board):
    
    '''
    This is a simple Artificial Intelligence model that plays the highest value position on
    the board.
    '''
    
    pos = np.unravel_index(np.argmax(aiValue, axis=None), aiValue.shape)
    if aiValue[pos] == np.max(aiValue):
        #print(str(round(aiValue[pos], 3)), ' is equal to the value of the max , ', str(round(np.max(aiValue), 3)))
        return pos
    else:
        print('You have some maaaad problem with finding the maxima in this array')
 
    
def Display(board):
    
    print('    0   1   2 ')
    print('0', board[0,:])
    print('1', board[1,:])
    print('2', board[2,:])

    
    
def Scorer(board, scoreBoard):
    # 0 = no winner, continue playing; 1 = player win; 2 = ai win; 3 = stalemate
        
    for i in range(0,3): # y index
        for j in range(0,3): # x index
            
            if board[i,j] == 'X':
                scoreBoard[i,j] = -2
            elif board[i,j] == 'O':
                scoreBoard[i,j] = 2
                
    #This bit of code sums the scores of each row and column to determine whether they are filled
    #if a summed score value os -6, the player has won; 6, the AI has won.
    sumArray = np.zeros(shape=(2,3)) #rows on top, columns on the bottom
    for i in range(0,3):
        rowIsum = np.sum(scoreBoard[i,:])
        columnIsum = np.sum(scoreBoard[:, i])
        sumArray[0,i] = rowIsum
        sumArray[1,i] = columnIsum       
    
    if 0 not in scoreBoard:
        return 3
    if -6 in sumArray:
        return 1
    elif 6 in sumArray:
        return 2
    else:
        return 0

 

#Main Loop              
Display(board)
while True:
    
    #Computation for the Players Turn
    playerX, playerY = PlayerInput()
    UpdateBoard(playerY, playerX, board, True)
    aiValue = np.ones(shape=(3,3), dtype=float)
    UpdateValues(aiValue, board)
    if Scorer(board, scoreBoard) == 3:
        Display(board)
        print('Stalemate, good game')
        break
    elif Scorer(board, scoreBoard) == 1:
        Display(board)
        print('You win, congrats')
        break
    elif Scorer(board, scoreBoard) == 2:
        Display(board)
        print('The AI has won')
        break
 
    
    
    #Computation for the AIs Turn
    pos = (0,0)
    pos = ArtificialIntelligence(aiValue, board)
    UpdateBoard(pos[0], pos[1], board, False)
    aiValue = np.ones(shape=(3,3), dtype=float)
    UpdateValues(aiValue, board)
    if Scorer(board, scoreBoard) == 3:
        Display(board)
        print('Stalemate, good game')
        break
    if Scorer(board, scoreBoard) == 1:
        Display(board)
        print('You win, congrats')
        break
    elif Scorer(board, scoreBoard) == 2:
        Display(board)
        print('The AI has won')
        break
    
    
