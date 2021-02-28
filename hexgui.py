import tkinter as tk
import math

class HexGui:
    
    def __init__(self, n, game):
        self.game = game   
        self.root = self.game.root
        
        title = tk.Label(self.root, text = "Hex Game", bg = "purple", fg = "white", font=("Helvetica", 25))
        title.pack(fill="x", side = "top")
        
        self.window = tk.Canvas(self.root, width=700, height = 500)
        self.window.pack()
        
        self.n = n
        
        # Setting length of the hexagons and the starting
        # position of the first hexagon
        self.hexagon_length = 200 // n
        self.start_x = 100
        self.start_y = 50
        self.y = (self.hexagon_length*math.sqrt(3)/2)
        self.x = math.sqrt(self.hexagon_length**2-self.y**2)
        
        
        self.move_count = 0
        
        # Key is (i,j), value is [id, isEmpty]           
        self.hexagons = {}
        
        self.draw_game_screen()
        
        
    
    
    
        
    def draw_game_screen(self):
        # Draw the field and border lines
        self.make_player_labels()
        self.draw_field()
        self.draw_vertical_lines()
        self.draw_horizontal_lines()
        
        
        drop = tk.OptionMenu(self.root, self.game.player_1_selection, "Human Player", "Monte Carlo AI", "Game Tree AI", "Neural Net AI", command=self.game.player_1_changed)
        drop.pack(side="left")
        
        drop2 = tk.OptionMenu(self.root, self.game.player_2_selection, "Human Player", "Monte Carlo AI", "Game Tree AI", "Neural Net AI", command=self.game.player_2_changed)
        drop2.pack(side="right")
        
        
        
        # initialize two buttons on bottom of window
        self.window.bind('<Button-1>', self.find_object)
        restart_button = tk.Button(self.root, text = 'New Game', command = self.restart_game) ###### TODO
        restart_button.pack(side="bottom")
    
    
        
        
        
    # Colors the clicked hexagon with respective color    
    def update_move(self, move):
        self.window.itemconfigure(self.hexagons[move][0], fill = self.game.current_player_color, activefill = self.game.current_player_color)
        self.hexagons[move][1] = False
        
        self.move_count += 1
        
        for key in self.hexagons:
            if self.hexagons[key][1]:
                self.window.itemconfigure(self.hexagons[key][0], fill = "grey", activefill = 'red' if self.game.current_player == 1 else 'blue')
        
        
        # TODO SOME WEIRD STUFF HAPPENS HERE ??
        
        
    
    
    
    def restart_game(self):
        answer = tk.messagebox.askokcancel('New Game', 'Are you sure you want to start a new game?')
        if answer:
            self.game.restart(self.n)
            
        
        
        
    #Gets called on a mouse click, calls game.make_move
    def find_object(self, event):
        #id of the clicked hexagon
        hex_id = self.window.find_closest(event.x, event.y)[0]
        if hex_id <= self.n**2:
            j = (hex_id-1) % self.n
            i = int((hex_id-j-1) / self.n)
            if self.hexagons[(i,j)][1]:
                self.game.make_move((i,j))
                
                         
                
    def game_over(self):
        # disable mouse click
        self.window.unbind('<Button-1>')
        # 
        for key in self.hexagons:
            if self.hexagons[key][1]:
                self.window.itemconfigure(self.hexagons[key][0], activefill = 'grey')
        # Color the winning path yellow
        path = self.game.board.victory_path
        for key in path:
            self.window.itemconfigure(self.hexagons[key][0], activefill = 'yellow', fill = 'yellow')
            
        tk.messagebox.showinfo('GAME OVER', 'Player ' + str(self.game.current_player) + ' won.')
        
        
        




        
        
    def calculate_hexagon_points(self, a, b):
        y = (self.hexagon_length*math.sqrt(3)/2)
        x = math.sqrt(self.hexagon_length**2-y**2)
        length = self.hexagon_length
        points = [a,b,a+y,b-x,a+2*y,b,a+2*y,b+length,a+y,b+length+x,a,b+length]
        return points
    
    
    def draw_field(self):
        a = self.start_x
        b = self.start_y
        y = (self.hexagon_length*math.sqrt(3)/2)
        x = math.sqrt(self.hexagon_length**2-y**2)
        for j in range(self.n):
            if j != 0:
                a += y
                b += self.hexagon_length+x
            for i in range(self.n):
                u = a + 2*i*y
                hex_id = self.window.create_polygon(self.calculate_hexagon_points(u, b), fill = 'grey', outline = 'black', activefill = self.game.current_player_color)
                self.hexagons[(j, i)] = [hex_id, True]
                
                
    # Create Labels "Player 1/2" with respective Colors
    def make_player_labels(self):
        player_1_label = tk.Label(self.root, text = "Player 1",font=("Helvetica", 16), fg =  'blue')
        player_2_label = tk.Label(self.root, text = "Player 2",font=("Helvetica", 16), fg =  'red')
        
        player_1_label.pack(side = 'left')
        player_2_label.pack(side = 'right')
        
    
    
    ####### TODO understand and refactor both draws into one functions!
    
    def draw_horizontal_lines(self):
        top_line = []
        bottom_line = []
        for i in range(self.n):
            top_line.append([self.start_x + i*2*self.y, self.start_y, self.start_x + i*2*self.y + self.y, self.start_y - self.x])
            bottom_line.append([self.start_x + (self.n - 1 + 2*i) * self.y, self.start_y - self.x + (self.n * (self.hexagon_length + self.x)), self.start_x + (self.n + 2*i) * self.y, self.start_y + self.n * (self.hexagon_length + self.x)])
            
        top_line.append([self.start_x + self.n*2*self.y, self.start_y])
        bottom_line.append([self.start_x + (self.n + 2*self.n)*self.y - self.y, self.start_y + self.n * (self.hexagon_length + self.x) - self.x])
        
        self.window.create_line(top_line, fill = 'red', width = 7)
        self.window.create_line(bottom_line, fill = 'red', width = 7)
        
    
    def draw_vertical_lines(self):
        left_line = []
        right_line = []
        for j in range(self.n): 
            left_line.append([self.start_x + j*self.y, self.start_y + j* (self.hexagon_length + self.x)])
            left_line.append([self.start_x + j * self.y, self.start_y + j * (self.hexagon_length + self.x) + self.hexagon_length])
            right_line.append([self.start_x + (2*self.n + j)* self.y, self.start_y + j*(self.hexagon_length + self.x)])
            right_line.append([self.start_x + (2*self.n + j) * self.y, self.start_y + j*(self.hexagon_length + self.x) + self.hexagon_length])
            
        self.window.create_line(right_line, fill = 'blue', width = 7)
        self.window.create_line(left_line, fill = 'blue', width = 7)
        
            
    
    
