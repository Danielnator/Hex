import numpy as np

class GameTreeAI:
    
    # TODO
    # 1. create and update empty fields
    
    
    def __init__(self, n, board, player, current_move):
        self.n = n
        self.board = board
        self.player = player
        self.enemy = (player%2)+1
        self.empty_fields = self.init_empty_fields()
        self.current_move = current_move
        self.last_move = None
        
        
        
        
    # Gets called in game after each move
    def receive_move(self, move):
        self.empty_fields.remove(move)         
        self.current_move += 1
        self.last_move = move
        



    def calculate_next_move(self):
        val, move = self.build_game_tree(self.board, 3, True)
        print('GameTreeAI Move: ', move, val)
        return move
    
    
    
    
    def build_game_tree(self, board, depth, maximizing_player, alpha = -float('inf'), beta = float('inf')):
        
        # Base Case: When in a leave node, evaluate the board
        if depth == 0 or len(self.empty_fields) == 0:
            ####### !!!!!! player = self.player if maximizing_player else self.enemy
            value = self.evaluate_board(board, self.player) 
            
            return (value, None)
        
        
        # TODO: forEach move: update board, remove move from available_moves, start recurions, 
        # then add move back to avalablie moves and remove from board
        
        
        # Case: Maximizing Player
        if maximizing_player:
            
            value = -float('inf')
            m = None
            for move in self.empty_fields:
                
                #Make the next move
                board[move[0]][move[1]] = self.player
                self.empty_fields.remove(move)
                
                #Compute value of move recursively
                deep_val = self.build_game_tree(board, depth-1, False, alpha, beta)[0]
                if deep_val > value:
                    value, m = deep_val, move
                alpha = max(alpha, value)
                
                # Undo the last move
                board[move[0]][move[1]] = 0
                self.empty_fields.append(move)
                
                if alpha >= beta:
                    break
            return (value, m)
        
        
        # Case: Minimizing Player
        else:
            value = float('inf')
            m = None
            for move in self.empty_fields:
                
                #Make the next move
                board[move[0]][move[1]] = self.enemy
                self.empty_fields.remove(move)
                
                #Compute value of move recursively
                deep_val = self.build_game_tree(board, depth-1, True, alpha, beta)[0]
                if deep_val < value:
                    value, m = deep_val, move
                beta = min(beta, value)
                
                # Undo the last move
                board[move[0]][move[1]] = 0
                self.empty_fields.append(move)
                
                if beta <= alpha:
                    break
            return (value, m)
    
    
    
    
    # Outputs the value of a board from player's perspective
    def evaluate_board(self, board, player):
        path_lengths_1 = [[0 for _ in range(self.n)] for i in range(self.n)]
        path_lengths_2 = [[0 for _ in range(self.n)] for i in range(self.n)]
        
        # Calculate path lengths for player 1
        for y in range(self.n-1, -1, -1):
            rerun_col = False
            for x in range(self.n):
                state = board[x][y]
                
                if state==1:
                    rerun_col = True
                
                if state == 2:
                    path_lengths_1[x][y] = float('inf')
                elif y == self.n-1:
                    path_lengths_1[x][y] = 0 if state == 1 else 1
                elif x == 0:
                    path_lengths_1[x][y] = (state+1)%2 + path_lengths_1[x][y+1]     # (state+1)%2 maps 1 on 0 and 0 on 1
                else:
                    path_lengths_1[x][y] = (state+1)%2 + min(path_lengths_1[x-1][y+1], path_lengths_1[x][y+1])
                    
                    
            if rerun_col:
                
                for x in range(1, self.n):
                    state = board[x][y]
                    if  state != 2 and path_lengths_1[x-1][y] + (state+1)%2 < path_lengths_1[x][y]:
                        path_lengths_1[x][y] = path_lengths_1[x-1][y] + (state+1)%2
                    
                for x in range(self.n-2, -1, -1):
                    state = board[x][y]
                    if state != 2 and path_lengths_1[x+1][y] + (state+1)%2 < path_lengths_1[x][y]:
                        path_lengths_1[x][y] = path_lengths_1[x+1][y] + (state+1)%2
                
                
            
            
                    
                    
        # Calculate path lengths for player 2
        for x in range(self.n-1, -1, -1):
            rerun_row = False
            for y in range(self.n):
                state = board[x][y]
                
                if state==2:
                    rerun_row = True
                
                if state == 1:
                    path_lengths_2[x][y] = float('inf')
                elif x == self.n-1:
                    path_lengths_2[x][y] = 0 if state == 2 else 1
                elif y == 0:
                    path_lengths_2[x][y] = (state+1)%3 + path_lengths_2[x+1][y]     
                else:
                    path_lengths_2[x][y] = (state+1)%3 + min(path_lengths_2[x+1][y-1], path_lengths_2[x+1][y])
                    
                    
            if rerun_row:
                
                for y in range(1, self.n):
                    state = board[x][y]
                    
                    if  state != 1 and path_lengths_2[x][y-1] + (state+1)%3 < path_lengths_2[x][y]:
                        path_lengths_2[x][y] = path_lengths_2[x][y-1] + (state+1)%3
                    
                for y in range(self.n-2, -1, -1):
                    state = board[x][y]
                    
                    if state != 1 and path_lengths_2[x][y+1] + (state+1)%3 < path_lengths_2[x][y]:
                        path_lengths_2[x][y] = path_lengths_2[x][y+1] + (state+1)%3
           
        
        
        
        
        val_1 = min(x[0] for x in path_lengths_1)
        val_2 = min(path_lengths_2[0])
        
        
        # If one of the values is 0 it means a winning path exists
        # Otherwise return the difference
        if val_1 == 0:
            return float('inf') if player == 1 else -float('inf')
        elif val_2 == 0:
            return -float('inf') if player == 1 else float('inf')
        else:
            result = (self.n - val_1)**2 - (self.n - val_2)**2
            
            #print(val_1)
            #print(val_2)
            
            return result if player == 1 else -result
        
    
    
 



    def init_empty_fields(self):
        fields = []
        for i in range(self.n):
            for j in range(self.n):
                if self.board[i][j] == 0:
                    fields.append((i,j))
        return fields
    

    