import copy
import random
import numpy as np



'''
Game AI based on Monte-Carlo.
For each possible moves, the class plays self.number_games many random games until a player won.
The move which had the highest win ratio will be chosen.
    
'''


class MonteCarloAI:
    
    def __init__(self, n, board, player, current_move):
        self.n = n
        self.player = player
        self.enemy = (player%2)+1
        self.board = board
        self.number_games = 700
        self.current_move = current_move
        
        
    # Iterates over all possible next moves, keeps track of move with highest win ratio    
    def calculate_next_move(self):
        best_move = (None, None, 0)
        
        for i in range(self.n):
            for j in range(self.n):
                
                if self.board[i][j] == 0:
                    win_ratio = self.simulate_games((i,j))
                    
                    # If win is certain, immediately return the move
                    if win_ratio == 1:
                        return (i,j)
                    
                    if win_ratio > best_move[2]:
                        best_move = (i, j, win_ratio)
                        
        print("BEST MOVE: ", best_move)
        
        return best_move[0:2]
    
    
    
    def receive_move(self, move):
        self.current_move += 1
        
                    
                    
    ## For a given move, play self.number_games many random games to the end                
    def simulate_games(self, first_move):
        wins = 0
        
        game_board = copy.deepcopy(self.board)
        game_board[first_move[0]][first_move[1]] = self.player
            
        empty_fields = self.init_empty_fields(game_board)
        
        for _ in range(self.number_games):
            empty_fields_cpy = copy.deepcopy(empty_fields)
            board_cpy = copy.deepcopy(game_board)
                            
            current_player = self.enemy
            
            while len(empty_fields_cpy) > 0:
                next_move = random.choice(empty_fields_cpy)
                empty_fields_cpy.remove(next_move)
                
                board_cpy[next_move[0]][next_move[1]] = current_player
    
                current_player = 1 if current_player == 2 else 2
            
            
            wins+= self.depth_first_search(board_cpy, self.player)
            #wins += self.finish_game(game_board, empty_fields)
        
        return wins / self.number_games
    
    
    
    # Initialize empty_fields and side_fields in simulate_games, which are then used in finish_game
    def init_empty_fields(self, board):
        empty_fields = []
        
        for i in range(self.n):
            for j in range(self.n):
                if board[i][j] == 0:
                    empty_fields.append((i,j))
                    
        return empty_fields
    
    

    
    # DFS for finding the winning player on a given board
    def depth_first_search(self,  board, player):
        visited = {}
        
        start_fields = []
        if player == 1:
            for j in range(self.n):
                if board[j][0] == 1:
                    start_fields.append((j,0))
        else:
            for j in range(self.n):
                if board[0][j] == 2:
                    start_fields.append((0,j))
        
        
        for i in range(self.n):
            for j in range(self.n):
                if board[i][j] == player:
                    visited[(i,j)] = False
            
        for start in start_fields:
            stack = [start]
            while len(stack) > 0:
                a = stack.pop()
                
                if (player == 1 and a[1] == self.n-1) or (player == 2 and a[0] == self.n-1):
                    return True
            
                if not visited[a]:
                    visited[a] = True
                    x = a[0]
                    y = a[1]
                    
                    #Check all 6 surrounding fields
                    if x>0 and board[x-1][y] == player and not visited[(x-1, y)]:
                        stack.append((x-1, y))
                    if x>0 and y<self.n-1 and board[x-1][y+1] == player and not visited[(x-1, y+1)]:
                        stack.append((x-1, y+1))
                    if y>0 and board[x][y-1] == player and not visited[(x, y-1)]:
                        stack.append((x, y-1))
                    if y<self.n-1 and board[x][y+1] == player and not visited[(x, y+1)]:
                        stack.append((x, y+1))
                    if y>0 and x<self.n-1 and board[x+1][y-1] == player and not visited[(x+1, y-1)]:
                        stack.append((x+1, y-1))
                    if x<self.n-1 and board[x+1][y] == player and not visited[(x+1, y)]:
                        stack.append((x+1, y))
                    
        return False
