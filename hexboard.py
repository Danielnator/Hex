import numpy as np

class HexBoard:
    
    def __init__(self, n):
        self.n = n
        self.winner = None
        
        # TODO CHANGE TO NP ARRAY
        self.board = np.zeros((n,n), dtype = "int8")
        
        self.side_1_fields = []
        self.side_2_fields = []
        self.current_player = 1
        
        self.move_count = 0
        self.victory_path = []
        
    
    
    def check_finished(self):
        if self.move_count < 2 * self.n - 1:
            return False
        
        if self.current_player == 1:
            return self.depth_first_search(self.side_1_fields)
        else:
            return self.depth_first_search(self.side_2_fields)
        
        
    
    def get_victory_path(self, parent, a):
        x = a
        self.victory_path.append(x)
        while parent[x] != None:
            self.victory_path.append(parent[x])
            x = parent[x]
        return self.victory_path
    
    
    def set_current_player(self, player):
        self.current_player = player
    
    
    def update_move(self, move):
        self.move_count += 1    
        if self.current_player == 1:
            self.board[move[0]][move[1]] = 1
            if move[1] == 0:
                self.side_1_fields.append(move)
        else:
            self.board[move[0]][move[1]] = 2
            if move[0] == 0:
                self.side_2_fields.append(move)              
        # After each move, check if game finished               
        return self.check_finished()
    
    
    
    
    def depth_first_search(self, side_fields):
        visited = {}
        parent = {}
        
        
        for i in range(self.n):
            for j in range(self.n):
                if self.board[i][j] == self.current_player:
                    visited[(i,j)] = False
                    parent[(i,j)] = None
            
        for start in side_fields:
            stack = [start]
            while len(stack) > 0:
                a = stack.pop()
                
                #### TODO CHECK IF MAKES SENSE ???
                #Check for winning condition
                if (self.current_player == 1 and a[1] == self.n-1) or (self.current_player == 2 and a[0] == self.n-1):
                    self.get_victory_path(parent, a)
                    self.winner == self.current_player
                    return True
            
                if not visited[a]:
                    visited[a] = True
                    x = a[0]
                    y = a[1]
                    
                    #Check all 6 surrounding fields
                    if x>0 and self.board[x-1][y] == self.current_player and not visited[(x-1, y)]:
                        stack.append((x-1, y))
                        parent[(x-1, y)] = (x,y)
                    if x>0 and y<self.n-1 and self.board[x-1][y+1] == self.current_player and not visited[(x-1, y+1)]:
                        stack.append((x-1, y+1))
                        parent[(x-1, y+1)] = (x,y)
                    if y>0 and self.board[x][y-1] == self.current_player and not visited[(x, y-1)]:
                        stack.append((x, y-1))
                        parent[(x, y-1)] = (x,y)
                    if y<self.n-1 and self.board[x][y+1] == self.current_player and not visited[(x, y+1)]:
                        stack.append((x, y+1))
                        parent[(x, y+1)] = (x,y)
                    if y>0 and x<self.n-1 and self.board[x+1][y-1] == self.current_player and not visited[(x+1, y-1)]:
                        stack.append((x+1, y-1))
                        parent[(x+1, y-1)] = (x,y)
                    if x<self.n-1 and self.board[x+1][y] == self.current_player and not visited[(x+1, y)]:
                        stack.append((x+1, y))
                        parent[(x+1, y)] = (x,y)
                    
        return False
                        
                        

    

