# -*- coding: utf-8 -*-
'''
Game AI using a trained Artificial Neural Network to predict the next best move
'''



import tensorflow as tf
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import copy


class AnnAI:
    
    def __init__(self, n, board, player, current_move):
        self.n = n
        self.player = player
        self.enemy = (player%2)+1
        self.board = board
        self.current_move = current_move
        
        # Load the trained keras model
        self.ann = tf.keras.models.load_model("ann_model")
        
        
        
    def receive_move(self, move):
        pass
    
    
    def calculate_next_move(self):
        board = copy.deepcopy(self.board)
    
    
        # Transform the board in to an 1D array with values -1,0,1
        for i in range(9):
            for j in range(9):
                if board[i][j] == self.enemy:
                    board[i][j] = -1
                elif board[i][j] == self.player:
                    board[i][j] = 1
                    
        board_transformed = []
        for i in range(9):
            for j in range(9):
                board_transformed.append(board[i][j])
                
        predictions = self.ann.predict(np.array([board_transformed]))
        
        
        # Iterate over all moves to get the maximal possible move
        max_prop = 0
        for i, prop in enumerate(predictions[0]):
            m = (i//9, i%9)
            print(prop, max_prop)
            if self.board[m[0]][m[1]] == 0 and prop > max_prop:
                max_prop = prop
                move = m
                
        
        
        print('ANN MOVE: ', move)
        return move
                
        
                    
        
                    
        