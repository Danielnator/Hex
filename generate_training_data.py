# -*- coding: utf-8 -*-
"""
Created on Tue Feb 23 23:31:59 2021

@author: rumin
"""


from hexboard import HexBoard
from ki_monte_carlo import MonteCarloAI
import pandas as pd
import copy



def generate_game_data():
    current_player = 1
    board = HexBoard(9)
    
    ki_1 = MonteCarloAI(9, board.board, 1, 1)
    ki_2 = MonteCarloAI(9, board.board, 2, 1)
    
    data = pd.DataFrame()
    
    game_finished = False 
    
    count = 0
    while not game_finished:
        count += 1
        print('COUNT: ', count)
        print('Current Player: ', current_player)
        print(board.board)
        
        if current_player == 1:
            next_move = ki_1.calculate_next_move()
        else:
            next_move = ki_2.calculate_next_move()
            
        print('NEXT MOVE:', next_move)
            
        ###### HERE GET BOARD AND MOVE ANS SAVE DATA
        data = save_move(data, board.board, next_move, current_player)
        
        game_finished = board.update_move(next_move)
        
        ki_1.receive_move(next_move)
        ki_2.receive_move(next_move)
            
        if game_finished:
            return data
        else:
            current_player = 1 if current_player == 2 else 2
            board.set_current_player(current_player)
        



def save_move(data, game_board, move, current_player):
    
    enemy = (current_player % 2) + 1
    board = copy.deepcopy(game_board)
    
    for i in range(9):
        for j in range(9):
            if board[i][j] == enemy:
                board[i][j] = -1
            elif board[i][j] == current_player:
                board[i][j] = 1
    
    move_transformed = move[0]*9 + move[1]
    board_transformed = []
    for i in range(9):
        for j in range(9):
            board_transformed.append(board[i][j])
    
    data = data.append([board_transformed + [move_transformed]])
    
    return data




if __name__ == "__main__":
    
    for i in range(211, 291):
        data = generate_game_data()
        
        print('DATA: ', data)
        print('************** SAVING CSV *************')
        data.to_csv("training_data/data_" + str(i) + ".csv")
    
    
    
    
    
    