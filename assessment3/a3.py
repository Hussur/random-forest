import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
import random
import time
import os
import sys

ALPHA = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
UP = "up"
DOWN = "down"
LEFT = "left"
RIGHT = "right"
DIRECTIONS = (UP, DOWN, LEFT, RIGHT,
              f"{UP}-{LEFT}", f"{UP}-{RIGHT}",
              f"{DOWN}-{LEFT}", f"{DOWN}-{RIGHT}")
WALL_VERTICAL = "|"
WALL_HORIZONTAL = "-"
POKEMON = "☺"
FLAG = "♥"
UNEXPOSED = "~"
EXPOSED = "0"
INVALID = "That ain't a valid action buddy."
HELP_TEXT = """h - Help.
<Uppercase Letter><number> - Selecting a cell (e.g. 'A1')
f <Uppercase Letter><number> - Placing flag at cell (e.g. 'f A1')
:) - Restart game.
q - Quit.
"""
TASK_ONE = "TASK_ONE"
TASK_TWO = "TASK_TWO"

cell_size = 60
class BoardModel:
    """The BoardModel class is used to store and manage the internal game state."""
    def __init__(self,grid_size,num_pokemon):
        """
        Construct the basic model of the game..
        Parameters:
            grid_size(int): The cell number of raws and columns
            num_pokemon(int): The number of pokemons
        """
        self._grid_size = grid_size
        self._number_pokemon =num_pokemon
        self._game = '~'*grid_size**2
        self._pokemon_locations = self.generate_pokemons(self._grid_size, self._number_pokemon)

    def get_game(self):
        """Returns an appropriate representation of the current state of the game board."""
        return self._game
    def get_pokemon_location(self):
        """Returns the indices describing all pokemon locations."""
        return self._pokemon_locations
    def get_num_attempted_catches(self):
        """Returns the number of pokeballs currently placed on the board."""
        return self._game.count(FLAG)
    def get_num_pokemon(self):
        """Returns the number of pokemon hidden in the game."""
        return self._number_pokemon
    def check_loss(self):
        """Returns True if the game has been lost, else False."""
        if POKEMON in self._game:
            return True
        else:
            return False
    def index_to_position(self,index):
        """Returns the (row, col) coordinate corresponding to the supplied index.
        Parameter:
        index(int): The index of a cell in game string."""
        return (index//self._grid_size,index%self._grid_size)
    
    def index_in_direction(self,index, grid_size, direction):
        """The index in the game string is updated by determining the
        adjacent cell given the direction.
        The index of the adjacent cell in the game is then calculated and returned.

        For example:
        | 1 | 2 | 3 |
        A | i | j | k |
        B | l | m | n |
        C | o | p | q |

        The index of m is 4 in the game string.
        if the direction specified is "up" then:
        the updated position corresponds with j which has the index of 1 in the game string.

        Parameters:
            index (int): The index in the game string.
            grid_size (int): The grid size of the game.
            direction (str): The direction of the adjacent cell.

        Returns:
            (int): The index in the game string corresponding to the new cell position
            in the game.

            None for invalid direction.
        """
        # convert index to row, col coordinate
        col = index % self._grid_size
        row = index // self._grid_size
        if RIGHT in direction:
            col += 1
        elif LEFT in direction:
            col -= 1
        # Notice the use of if, not elif here
        if UP in direction:
            row -= 1
        elif DOWN in direction:
            row += 1
        if not (0 <= col < self._grid_size and 0 <= row < self._grid_size):
            return None
        return self.position_to_index((row, col), self._grid_size)
    
    def replace_character_at_index(self,game, index, character):
        """A specified index in the game string at the specified index is replaced by
        a new character.
        Parameters:
            game (str): The game string.
            index (int): The index in the game string where the character is replaced.
            character (str): The new character that will be replacing the old character.

        Returns:
            (str): The updated game string.
        """
        self._game = self._game[:index] + character + self._game[index + 1:]
        return self._game

    def flag_cell(self, game, index):
        """Toggle Flag on or off at selected index. If the selected index is already
            revealed, the game would return with no changes.
            Parameters:
                game (str): The game string.
                index (int): The index in the game string where a flag is placed.
            Returns
                (str): The updated game string.
        """
        if self._game[index] == FLAG:
            self._game = self.replace_character_at_index(self._game, index, '~')

        elif self._game[index] == '~':
            self._game = self.replace_character_at_index(self._game, index, FLAG)

        return self._game

    def position_to_index(self, position, grid_size):
        """Convert the row, column coordinate in the grid to the game strings index.

        Parameters:
            position (tuple<int, int>): The row, column position of a cell.
            grid_size (int): The grid size of the game.

        Returns:
            (int): The index of the cell in the game string.
        """
        x, y = position
        return x * grid_size + y
    
    def neighbour_directions(self,index, grid_size):
        """Seek out all direction that has a neighbouring cell.

        Parameters:
            index (int): The index in the game string.
            grid_size (int): The grid size of the game.

        Returns:
            (list<int>): A list of index that has a neighbouring cell.
        """
        neighbours = []
        for direction in DIRECTIONS:
            neighbour = self.index_in_direction(index, self._grid_size, direction)
            if neighbour is not None:
                neighbours.append(neighbour)

        return neighbours
    
    def number_at_cell(self,game, pokemon_locations, grid_size, index):
        """Calculates what number should be displayed at that specific index in the game.

        Parameters:
            game (str): Game string.
            pokemon_locations (tuple<int, ...>): Tuple of all Pokemon's locations.
            grid_size (int): Size of game.
            index (int): Index of the currently selected cell

        Returns:
            (int): Number to be displayed at the given index in the game string.
        """
        if self._game[index] != UNEXPOSED:
            return int(self._game[index])
        number = 0
        for neighbour in self.neighbour_directions(index, self._grid_size):
            if neighbour in self._pokemon_locations:
                number += 1
        return number
    
    def reveal_cells(self,game, grid_size, pokemon_locations, index):
        """Reveals all neighbouring cells at index and repeats for all
        cells that had a 0.

        Does not reveal flagged cells or cells with Pokemon.

        Parameters:
            game (str): Game string.
            pokemon_locations (tuple<int, ...>): Tuple of all Pokemon's locations.
            grid_size (int): Size of game.
            index (int): Index of the currently selected cell

        Returns:
            (str): The updated game string
        """
        number = self.number_at_cell(game, pokemon_locations, self._grid_size, index)
        self._game = self.replace_character_at_index(game,index, str(number))
        clear = self.big_fun_search(game,self._grid_size,self._pokemon_locations,index)
        print('!')
        for i in clear:
            if self._game[i] != FLAG:
                number = self.number_at_cell(game, pokemon_locations, self._grid_size, i)
                self._game = self.replace_character_at_index(game,i, str(number))

        return self._game

    def big_fun_search(self,game, grid_size, pokemon_locations, index):
        """Searching adjacent cells to see if there are any Pokemon"s present.

        Using some sick algorithms.

        Find all cells which should be revealed when a cell is selected.

        For cells which have a zero value (i.e. no neighbouring pokemons) all the cell"s
        neighbours are revealed. If one of the neighbouring cells is also zero then
        all of that cell"s neighbours are also revealed. This repeats until no
        zero value neighbours exist.

        For cells which have a non-zero value (i.e. cells with neighbour pokemons), only
        the cell itself is revealed.

        Parameters:
            game (str): Game string.
            grid_size (int): Size of game.
            pokemon_locations (tuple<int, ...>): Tuple of all Pokemon's locations.
            index (int): Index of the currently selected cell

        Returns:
            (list<int>): List of cells to turn visible.
        """
        queue = [index]
        discovered = [index]
        visible = []
        if self._game[index] == FLAG:
            return queue

        number = self.number_at_cell(self._game, self._pokemon_locations, self._grid_size, index)
        if number != 0:
            return queue

        while queue:
            node = queue.pop()
            for neighbour in self.neighbour_directions(node, self._grid_size):
                if neighbour in discovered:
                    continue
                discovered.append(neighbour)
               
                if self._game[neighbour] != FLAG:
                    number = self.number_at_cell(self._game, self._pokemon_locations, self._grid_size, neighbour)
                    if number == 0:
                        queue.append(neighbour)
                visible.append(neighbour)
        return visible
    
    def generate_pokemons(self,grid_size, number_of_pokemons):
        """Pokemons will be generated and given a random index within the game.
        Parameters:
            grid_size (int): The grid size of the game.
            number_of_pokemons (int): The number of pokemons that the game will have.
        Returns:
            (tuple<int>): A tuple containing  indexes where the pokemons are
            created for the game string.
        """
        cell_count = self._grid_size ** 2
        pokemon_locations = ()

        for _ in range(self._number_pokemon):
            if len(pokemon_locations) >= cell_count:
                break
            index = random.randint(0, cell_count-1)
            while index in pokemon_locations:
                index = random.randint(0, cell_count-1)
            pokemon_locations += (index,)
        return pokemon_locations

    def write_file(self,path,data):
        """Create a new file to store data and write data in it
        Parameters:
            path<str>:The name and the path of the file.
            data<str>:The data which will be write in the file."""
        file = open(path,'w')
        file.write(data)
        file.close()
    
    def check_win(self,game, pokemon_locations):
        """Checking if the player has won the game.

        Parameters:
            game (str): Game string.
            pokemon_locations (tuple<int, ...>): Tuple of all Pokemon's locations.

        Returns:
            (bool): True if the player has won the game, false if not.

        """
        return UNEXPOSED not in self._game and self._game.count(FLAG) == len(self._pokemon_locations)
    
class PokemonGame:
    """This class should manage necessary communication
    between any model and view classes, as well as event handling.
    """
    def __init__(self,master,grid_size=10,num_pokemon=15,task=TASK_ONE):
        """
        Construct a game.
        Parameters:
            master (tk.Widget): Widget within which to place the selection panel.
            grid_size(int): The cell number of raws and columns
            num_pokemon(int): The number of pokemons
            task<str>: The name of the game which can be used to select games.
        """
        self._master = master
        self._grid_size = grid_size
        self._num_pokemon = num_pokemon
        self._task = task
        self._game = BoardModel(self._grid_size,self._num_pokemon)
        #self._Time = Time()

        self._menuBar = tk.Menu(self._master)
        self._master.config(menu=self._menuBar)
        self._fileMenu = tk.Menu(self._menuBar, tearoff=0)
        self._menuBar.add_cascade(label="File", menu=self._fileMenu)
        self._fileMenu.add_command(label='Save Game', command=self.save_game)
        self._fileMenu.add_command(label='Load Game', command=self.load_game)
        self._fileMenu.add_command(label='Restart Game', command=self.restart_game)
        self._fileMenu.add_command(label='New Game', command=self.new_game)
        self._fileMenu.add_command(label='End Game', command=self.end_game)
        
        self.draw()

    def save_game(self):
        """Prompt the user for the location to save their le (using an appro-
        priate method of your choosing) and save all necessary information
        to replicate the current state of the game. Include appropriate error
        handling."""
        file_path="Saved_Game.txt"
        grid_size = str(self._grid_size)+'\n'
        pokeball = str(15-self._game.get_num_attempted_catches())+'\n'
        game = str(self._game.get_game())+'\n'
        pokemon_location=''
        for i in range(14):
            pokemon_location += str(self._game.get_pokemon_location()[i])+','
        if not os.path.isfile(file_path):
            self._game.write_file(file_path,'')
        with open(file_path,'w') as file:
            file.write(grid_size)
            file.write(pokeball)
            file.write(game)
            file.write(pokemon_location)
    
    def load_game(self):
        """Prompt the user for the location of the le to load a game from
        and load the game described in that le. Include approriate error
        handling."""
        with open('Saved_Game.txt','r') as file:
            game_list=file.readlines()
        self._game._game=game_list[2].rstrip('\n')
        pokemon_locations=game_list[3].split(',', 15)
        pokemon_locations.remove('')
        for i in range(15):
            pokemon_locations[i]=int(pokemon_locations[i])
        self._game._pokemon_locations=tuple(pokemon_locations)
        self._board_view.draw_board(self._game.get_game())
        print(self._game._pokemon_locations)
        

    def restart_game(self):
        """Restart the current game, including game timer. Pokemon locations
        should persist."""
        self._game._game = UNEXPOSED*(self._grid_size*self._grid_size)
        self._board_view.draw_board(self._game.get_game())
    def new_game(self):
        """Restart to a new game (i.e. new pokemon locations). Use the same
        grid size and number of pokemon as the current game."""
        self._game._game = UNEXPOSED*(self._grid_size*self._grid_size)
        self._game._pokemon_locations = self._game.generate_pokemons(self._grid_size, self._game.get_num_pokemon)
        self._board_view.draw_board(self._game.get_game())
    def end_game(self):
        """Prompt the player via messagebox to ask whether they are sure
        they would like to quit. If no, do nothing. If yes, quit the game
        (window should close and program should terminate)."""
        response = messagebox.askyesno("Quit the game","Would you like to quit the game?")
        if response:
            os._exit(0)
    def draw(self):
        """Draw the title of the game and call Class BoardView to draw the board."""
        Title = tk.Label(self._master,text='Pokemon: Got 2 Find Them All!',bg='pink',font=50,fg='white')
        Title.pack(fill=tk.X)
        if self._task == TASK_ONE:
            self._board_view = BoardView(self._master,self._grid_size,self._grid_size*cell_size,self._game)
            self._board_view.draw_board(self._game.get_game())
            self._board_view.pack()
        elif self._task == TASK_TWO:
            self._board_view = ImageBoardView(self._master,self._grid_size,self._grid_size*cell_size,self._game)
            self._board_view.draw_board(self._game.get_game())
            self._board_view.pack()

class BoardView(tk.Canvas):
    """BoardView represents the GUI for the board. At the beginning of the game the board display 
    all dark green squares. BoardView  inherit from tk.Canvas"""
    def __init__(self,master,grid_size,board_width=600,*args,**kwargs):
        super().__init__(master,**kwargs)
        self._master = master
        self._grid_size = grid_size
        self._board_width = board_width
        self.config(width=self._grid_size*cell_size,height=self._grid_size*cell_size)
        self._game = args[0]
        self._origin_box=None

    def draw_board(self,board):
        """Given an appropriate representation of the current state of the
        game board, draw the view to react this game state.
        Paremeter:
            board<str>:The game string."""
        self.delete(tk.ALL)
        for i in range(self._grid_size):
            for j in range(self._grid_size):
                char = board[self._game.position_to_index((j,i),self._grid_size)]
                x0=j*cell_size
                y0=i*cell_size
                x1=x0+cell_size
                y1=y0+cell_size
                if char =='~':
                    """Color the unexposed cell as darkgreen"""
                    self.create_rectangle(x0,y0,x1,y1, fill='darkgreen')    
                elif char == POKEMON:
                    """Color the exposed pokemon cell as yellow"""
                    self.create_rectangle(x0,y0,x1,y1, fill='yellow')
                    self.create_text(x0+cell_size/2,y0+cell_size/2,text=POKEMON,font=(42))
                elif char == FLAG:
                    """Color the flag cell as red"""
                    self.create_rectangle(x0,y0,x1,y1, fill='red')
                    self.create_text(x0+cell_size/2,y0+cell_size/2,text=FLAG,font=(42))
                else:
                    """Color the exposed cell as lightgreen and text the number of neighbor pokemons."""
                    self.create_rectangle(x0,y0,x1,y1, fill='lightgreen')
                    self.create_text(x0+cell_size/2,y0+cell_size/2,text=char,font=(42))
        self.bind_clicks()
        
    def _left_click(self,x,y):
        """Control the behavior of the game when a cell is clicked by left button.
        Parameter:
            (x,y)<tuple(int,int)>: The pixel of current mouse location."""
        pixel=x,y
        position=self.pixel_to_position(pixel)
        index = self._game.position_to_index(position,self._grid_size)
        if self._game.get_game()[index]==FLAG:
            """Left click on an 'attempted catch' square will not change to game view."""
            self.draw_board(self._game.get_game())
        elif index in self._game.get_pokemon_location():
            """If Left click on tall grass square with hidden pokemon,
            Yellow rectangles for squares that hide pokemon (including any previously caught pokemon) will be show.
            Present a messagebox to tell the player they loss and quit the game."""
            for k in self._game.get_pokemon_location():
                self._game.replace_character_at_index(self._game,k,POKEMON)
            self.draw_board(self._game.get_game())
            messagebox.showinfo("Game Over", "You loss! :D")
            self._master.destroy()
        elif index not in self._game.get_pokemon_location():
            """If Left click on tall grass square with no hidden pokemon,
            light green colour with superimposed text displaying the number of surrounding pokemon. 
            If there are no surrounding pokemon, the number 0 should be displayed, and neighbouring cells should be exposed."""
            number=str(self._game.number_at_cell(self._game.get_game(),self._game.get_pokemon_location(),self._grid_size, index))
            if number=='0':
                self._game.reveal_cells(self._game.get_game(), self._grid_size, self._game.get_pokemon_location, index)
            else:
                self._game.replace_character_at_index(self._game,index,number)
            self.draw_board(self._game.get_game())

    def _right_click(self,x,y):
        """If Right click on unexposed square,
        red rectangle for `attempted catch', dark green rectangle for tall grass.
        Parameter:
            (x,y)<tuple(int,int)>: The pixel of current mouse location."""
        pixel=x,y
        position=self.pixel_to_position(pixel)
        index = self._game.position_to_index(position,self._grid_size)        
        self._game.flag_cell(self._game, index)
        self.draw_board(self._game.get_game())   
        if self._game.check_win(self._game.get_game(), self._game.get_pokemon_location):
            messagebox.showinfo("Game Over", "You won! :D")
            self._master.destroy()
            
    def highlight(self,x,y):
        """When the game is run in TASK ONE mode, motion onto a grid square should cause a border to
        appear around the square that the cursor is on. Motion on a grid square should cause this border
        to disappear.
        Parameter:
            (x,y)<tuple(int,int)>: The pixel of current mouse location."""
        pixel = x,y
        current_box= self.get_bbox(pixel)
        if current_box!=self._origin_box:
            if self._origin_box is not None:
                self.create_rectangle(self._origin_box[0],self._origin_box[1],self._origin_box[2],self._origin_box[3],outline=None) 
            self._origin_box = current_box
        self._highlight=self.create_rectangle(current_box[0],current_box[1],current_box[2],current_box[3],outline="red")
        
        
    def bind_clicks(self):
        """Bind clicks on a label to the left and right click handlers.
        """
        self.bind('<Button-1>',lambda e:self._left_click(e.x,e.y))
        self.bind('<Button-2>',lambda e:self._right_click(e.x,e.y))
        self.bind('<Button-3>',lambda e:self._right_click(e.x,e.y))
        self.bind('<Motion>', lambda e: self.highlight(e.x,e.y))
                   
    def get_bbox(self,pixel):
        """Returns the bounding box for a cell centered at the provided pixel coordinates.
        Parameter:
            pixel<tuple(int,int)>:The location of the mouse in this programme.
        Return:
            <tuple(int,int,int,int)>:The NW and SE corner of the cell which include the pixel."""
        j=self.pixel_to_position(pixel)[0]
        i=self.pixel_to_position(pixel)[1]
        x0=j*cell_size
        y0=i*cell_size
        x1=x0+cell_size
        y1=y0+cell_size
        return (x0,y0,x1,y1)
    def position_to_pixel(self,position):
        """Returns the center pixel for the cell at position.
        Parameter:
            position<tuple(int,int)>: The cell coordinate in the cell matrix.
        Return:
            <tuple(int,int)>: The pixel of NW corner of the cell."""
        x,y=position
        return x*cell_size, y*cell_size
    def pixel_to_position(self,pixel):
        """Converts the supplied pixel to the position of the cell
        it is contained within
        Parameter:
            pixel<tuple(int,int)>:The location of the mouse in this programme.
        Return:
            <tuple(int,int)>:The cell coordinate in the cell matrix."""
        x,y=pixel
        return x//cell_size, y//cell_size

class ImageBoardView(BoardView):
    """"BoardView represents the GUI for the board. At the beginning of the game the board display 
    all tall grass squares. ImageBoardView inherit from BoardView"""
    def __init__(self,master,grid_size,board_width=600,*args,**kwargs):
        super().__init__(master,grid_size,board_width,*args,**kwargs)
        self._master = master
        self._grid_size = grid_size
        self._board_width = board_width
        self.config(width=self._grid_size*cell_size,height=self._grid_size*cell_size)
        self._game = args[0]
        #self._Title = args[1]
        self._images=[]
        self._origin_box=None

    def draw_board(self,board):
        """Given an appropriate representation of the current state of the
        game board, draw the view to react this game state.
        Paremeter:
            board<str>:The game string."""
        self.delete(tk.ALL)
        self._images.clear()
        image1 = get_image("images/pokemon_sprites/togepi")
        image2 = get_image("images/pokemon_sprites/charizard")
        image3 = get_image("images/pokemon_sprites/cyndaquil")
        image4 = get_image("images/pokemon_sprites/pikachu")
        image5 = get_image("images/pokemon_sprites/psyduck")
        image6 = get_image("images/pokemon_sprites/umbreon")
        pokemon_list=[image1,image2,image3,image4,image5,image6]
        adjacent0 = get_image("images/zero_adjacent")
        adjacent1 = get_image("images/one_adjacent")
        adjacent2 = get_image("images/two_adjacent")
        adjacent3 = get_image("images/three_adjacent")
        adjacent4 = get_image("images/four_adjacent")
        adjacent5 = get_image("images/five_adjacent")
        adjacent6 = get_image("images/six_adjacent")
        adjacent7 = get_image("images/seven_adjacent")
        adjacent8 = get_image("images/eight_adjacent")
        near_pokemons=[adjacent0,adjacent1,adjacent2,adjacent3,adjacent4,adjacent5,adjacent6,adjacent7,adjacent8]
        for i in range(self._grid_size):
            for j in range(self._grid_size):
                x0=j*cell_size
                y0=i*cell_size
                char = board[self._game.position_to_index((j,i),self._grid_size)]
                if char =='~':
                    """Give the Unexposed cell tall grass"""
                    image0 = get_image("images/unrevealed")
                    self.create_image(x0+cell_size/2,y0+cell_size/2,image=image0)
                    self._images.append(image0)
                elif char == POKEMON:
                    """Give the exposed pokemon cell the pokemons images."""
                    pokemon_image = pokemon_list[random.randint(0, 5)]
                    self.create_image(x0+cell_size/2,y0+cell_size/2,image=pokemon_image)
                    self._images.append(pokemon_image)

                elif char == FLAG:
                    """Give the Flag cell pokemon ball."""
                    image7 = get_image("images/pokeball")
                    self.create_image(x0+cell_size/2,y0+cell_size/2,image=image7)
                    self._images.append(image7)
             
                else:
                    """Give the exposed cell short grass."""
                    adjacent = near_pokemons[int(char)]
                    self.create_image(x0+cell_size/2,y0+cell_size/2,image=adjacent)
                    self._images.append(adjacent)

        self.bind_clicks()
        
    def _left_click(self,x,y):
        """Control the behavior of the game when a cell is clicked by left button.
        Parameter:
            (x,y)<tuple(int,int)>: The pixel of current mouse location."""
        pixel=x,y
        position=self.pixel_to_position(pixel)
        index = self._game.position_to_index(position,self._grid_size)
        if self._game.get_game()[index]==FLAG:
            """Left click on an 'attempted catch' square will not change to game view."""
            self.draw_board(self._game.get_game())
        elif index in self._game.get_pokemon_location():
            """If Left click on tall grass square with hidden pokemon,
            `Expose' all hidden pokemon, and provide a tkinter messagebox to tell the user they lost the game."""
            for k in self._game.get_pokemon_location():
                self._game.replace_character_at_index(self._game,k,POKEMON)           
            self.draw_board(self._game.get_game())
            messagebox.showinfo("Game Over", "You loss! :D")
            self._master.destroy()
        elif index not in self._game.get_pokemon_location():
            """If Left click on tall grass square with no hidden pokemon,
            `Expose' tall grass to short grass."""
            number=str(self._game.number_at_cell(self._game.get_game(),self._game.get_pokemon_location(),self._grid_size, index))
            if number=='0':
                self._game.reveal_cells(self._game.get_game(), self._grid_size, self._game.get_pokemon_location, index)
            else:
                self._game.replace_character_at_index(self._game,index,number)
            self.draw_board(self._game.get_game())

    def _right_click(self,x,y):
        """If Right click on unexposed square,
        Toggle status (between `attempted catch' and tall grass).
        Parameter:
            (x,y)<tuple(int,int)>: The pixel of current mouse location."""
        pixel=x,y
        position=self.pixel_to_position(pixel)
        index = self._game.position_to_index(position,self._grid_size)        
        self._game.flag_cell(self._game, index)
        self._game.set_num_pokemon(self._game.get_num_pokemon()-1)
        #self._label.config(text = f"{self._game.get_num_pokemon()} pokemons left")
        self.draw_board(self._game.get_game())
        if self._game.check_win(self._game.get_game(), self._game.get_pokemon_location):
            messagebox.showinfo("Game Over", "You won! :D")
            self._master.destroy()

    def highlight(self,x,y):
        """motion on tall grass squares should cause the grass to `rustle'. 
        Motion onto a tall grass square should cause the image to change to the `unexposed moved.png' image, 
        whereas motion on a tall grass square should restore the image to the `unexposed.png' image."""
        pixel = x,y
        image_highlight = get_image("images/unrevealed_moved")
        image_common = get_image("images/unrevealed")
        current_box= self.get_bbox(pixel)
        position=self.pixel_to_position(pixel)
        index = self._game.position_to_index(position,self._grid_size)
        if self._game.get_game()[index]=='~':
            if current_box!=self._origin_box:
                if self._origin_box is not None:
                    position1=self.pixel_to_position((self._origin_box[0],self._origin_box[1]))
                    index1 = self._game.position_to_index(position1,self._grid_size)
                    if self._game.get_game()[index1]=='~':
                        self.create_image(self._origin_box[0]+cell_size/2,self._origin_box[1]+cell_size/2,image=image_common)
                        self._images.append(image_common)
                self._origin_box = current_box
            self._highlight=self.create_image(current_box[0]+cell_size/2,current_box[1]+cell_size/2,image=image_highlight)
            self._images.append(image_highlight)        
        
    def bind_clicks(self):
        """Bind clicks on a label to the left and right click handlers.
        """
        self.bind('<Button-1>',lambda e:self._left_click(e.x,e.y))
        self.bind('<Button-2>',lambda e:self._right_click(e.x,e.y))
        self.bind('<Button-3>',lambda e:self._right_click(e.x,e.y))
        self.bind('<Motion>', lambda e: self.highlight(e.x,e.y))
                   
    def get_bbox(self,pixel):
        """Returns the bounding box for a cell centered at the provided pixel coordinates.
        Parameter:
            pixel<tuple(int,int)>:The location of the mouse in this programme.
        Return:
            <tuple(int,int,int,int)>:The NW and SE corner of the cell which include the pixel."""
        j=self.pixel_to_position(pixel)[0]
        i=self.pixel_to_position(pixel)[1]
        x0=j*cell_size
        y0=i*cell_size
        x1=x0+cell_size
        y1=y0+cell_size
        return (x0,y0,x1,y1)

    def position_to_pixel(self,position):
        """Returns the center pixel for the cell at position.
        Parameter:
            position<tuple(int,int)>: The cell coordinate in the cell matrix.
        Return:
            <tuple(int,int)>: The pixel of NW corner of the cell."""
        x,y=position
        return x*cell_size, y*cell_size
    def pixel_to_position(self,pixel):
        """Converts the supplied pixel to the position of the cell
        it is contained within
        Parameter:
            pixel<tuple(int,int)>:The location of the mouse in this programme.
        Return:
            <tuple(int,int)>:The cell coordinate in the cell matrix."""
        x,y=pixel
        return x//cell_size,y//cell_size

"""class Time(tk.Frame):
    def __init__(self):
        self.root = tk.Tk()
        self.label = tk.Label(text="")
        self.start_time = time.time()
        self.label.pack()

        self.update_clock()
        self.root.mainloop()
    def update_clock(self):
        current_time = int(time.time() - self.start_time)
        mins = current_time//60
        seconds = current_time%60
        self.label.config(image = get_image("images/clock"),text=f"{mins}m'\n'{seconds}s")
        self.root.after(1000,self.update_clock)"""
        
def get_image(image_name):
    """(tk.PhotoImage) Get a image file based on capability.

    If a .png doesn't work, default to the .gif image.
    """
    try:
        image = tk.PhotoImage(file=image_name + ".png")
    except tk.TclError:
        image = tk.PhotoImage(file=image_name + ".gif")
    return image

def main():
    root = tk.Tk()
    root.title("Pokemon:Got 2 Find Them All!")

    PokemonGame(root)

    root.update()
    root.mainloop()


if __name__ == "__main__":
    main()
