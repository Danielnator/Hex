'''
Main class of the Game.
Creates Instances of a HexGui and a HexBoard, 
contains the tkinter mainloop,
updates the types of players (human or AI) 
and handles new moves.
'''



import tkinter as tk
from hexboard import HexBoard
from hexgui import HexGui
from ki_game_tree import GameTreeAI
from ki_monte_carlo import MonteCarloAI
import copy
from ki_ann import AnnAI
import pandas as pd



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



class Game:
    
    def __init__(self, n):
        self.root = tk.Tk()
        self.root.title('Hex')
        
        self.n = n
        
        self.data = pd.DataFrame()
        
        self.current_player = 1
        self.current_player_color = 'blue'
        
        self.current_move = 1
        
        self.player_1_selection = tk.StringVar()
        self.player_1_selection.set('Human Player')
        self.player_2_selection = tk.StringVar()
        self.player_2_selection.set('Human Player')
        
        self.board = HexBoard(n)
        
        self.window = HexGui(n, self)
        
        
        self.root.mainloop()
        
        
    # Handles the case when Player 1 is changes    
    def player_1_changed(self, event):
        print("Player 1:", self.player_1_selection.get()) # prints value based on choice var
        mode = self.player_1_selection.get()
        if mode == "Human Player":
            self.ki_1 = None
        elif mode == "Monte Carlo AI":
            self.ki_1 = MonteCarloAI(self.n, self.board.board, 1, self.current_move)
        elif mode == "Game Tree AI":
            self.ki_1 = GameTreeAI(self.n, self.board.board, 1, self.current_move)
        elif mode == "Neural Net AI":
            #pass
            self.ki_1 = AnnAI(self.n, self.board.board, 1, self.current_move)
        
        if self.current_player == 1 and mode != "Human Player":
            move = self.ki_1.calculate_next_move()
            self.make_move(move)
        
        
        
        
    # Handles the case when player 2 is changed    
    def player_2_changed(self, event):
        print("Player 2:", self.player_2_selection.get()) # prints value based on choice var
        mode = self.player_2_selection.get()
        if mode == "Human Player":
            self.ki_2 = None
        elif mode == "Monte Carlo AI":
            self.ki_2 = MonteCarloAI(self.n, self.board.board, 2, self.current_move)
        elif mode == "Game Tree AI":
            self.ki_2 = GameTreeAI(self.n, self.board.board, 2, self.current_move)
        elif mode == "Neural Net AI":
            #pass
            self.ki_2 = AnnAI(self.n, self.board.board, 1, self.current_move)
        
        if self.current_player == 2 and mode != "Human Player":
            move = self.ki_2.calculate_next_move()
            self.make_move(move)
        
        
        
        
    # Handles updating the game and board with a move    
    def make_move(self, move):
        
        self.current_move += 1
        self.window.update_move(move)
        
        # HexBoard.update_move checks if a winning paths exists and returns a bool
        game_finished = self.board.update_move(move)
        
        self.data = save_move(self.data, self.board.board, move, self.current_player)
        
        if game_finished:
            self.window.game_over()
            ######self.data.to_csv("training_data/data_X.csv")
            return
        else:
            self.update_next_player()
            
        
        # Updates AIs with the move
        if self.player_1_selection.get() != "Human Player":
            self.ki_1.receive_move(move)
        if self.player_2_selection.get() != "Human Player":
            self.ki_2.receive_move(move)


        # If next player is an AI, let them calculate the next Move
        if self.current_player == 1 and self.player_1_selection.get() != "Human Player":
            next_move = self.ki_1.calculate_next_move()
            self.make_move(next_move)
            
        if self.current_player == 2 and self.player_2_selection.get() != "Human Player":
            next_move = self.ki_2.calculate_next_move()
            self.make_move(next_move)
            


        
    # Changes the player after a move has been made
    def update_next_player(self):
        if self.current_player == 1:
            self.current_player = 2
            self.current_player_color = 'red'
        else:
            self.current_player = 1
            self.current_player_color = 'blue'
            
        self.board.set_current_player(self.current_player)
        
        
    
    
    # Destroys the root and starts new game
    def restart(self, n):
        self.root.destroy()
        Game(n) 
    
    
    

    
         
    
if __name__ == "__main__":
    Game(9)
        
        
    