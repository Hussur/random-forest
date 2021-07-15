EMPTY_TILE = "tile"
START_PIPE = "start"
END_PIPE = "end"
LOCKED_TILE = "locked"

SPECIAL_TILES = {
    "S": START_PIPE,
    "E": END_PIPE,
    "L": LOCKED_TILE
}

PIPES = {
    "ST": "straight",
    "CO": "corner",
    "CR": "cross",
    "JT": "junction-t",
    "DI": "diagonals",
    "OU": "over-under"
}

### add code here ###

class PipeGame:
    """
    A game of Pipes.
    """
    def __init__(self, game_file='game_1.csv'):
        """
        Construct a game of Pipes from a file name.

        Parameters:
            game_file (str): name of the game file.
        """
        #########################COMMENT THIS SECTION OUT WHEN DOING load_file#######################
        self.board_layout = [[Tile('tile', True), Tile('tile', True), Tile('tile', True), Tile('tile', True), \
        Tile('tile', True), Tile('tile', True)], [StartPipe(1), Tile('tile', True), Tile('tile', True), \
        Tile('tile', True), Tile('tile', True), Tile('tile', True)], [Tile('tile', True), Tile('tile', True), \
        Tile('tile', True), Pipe('junction-t', 0, False), Tile('tile', True), Tile('tile', True)], [Tile('tile', True), \
        Tile('tile', True), Tile('tile', True), Tile('tile', True), Tile('locked', False), Tile('tile', True)], \
        [Tile('tile', True), Tile('tile', True), Tile('tile', True), Tile('tile', True), EndPipe(3), \
        Tile('tile', True)], [Tile('tile', True), Tile('tile', True), Tile('tile', True), Tile('tile', True), \
        Tile('tile', True), Tile('tile', True)]]

        self.playable_pipes = {'straight': 1, 'corner': 1, 'cross': 1, 'junction-t': 1, 'diagonals': 1, 'over-under': 1}
        #########################COMMENT THIS SECTION OUT WHEN DOING load_file#######################
        self.end_pipe_positions()
        
    def get_board_layout(self):
        """
        Present the present Tile board. Call the board_layout from __init__ function.
        Return: board_layout(2-dimensional list): the tile board include the information of every tile.
        """
        return self.board_layout

    def get_playable_pipes(self):
        """
        Present the present playable pipes. Call the playable_pipes from __init__ function.
        Return: playable_pipes(dict): a dictionary contain every type of pipe and their playable quantity.
        """
        return self.playable_pipes

    def change_playable_amount(self, pipe_name:str, number:int):
        """
        Modify the dictionary of playable pipes, increase or decrease the number of specific pipes. 
        Modify the value of given key in the dictionary.
        Parameters: 
                    pipe_name(str): the type of pipes that player want to change
                    number(int): the quantity of playable changed pipes
        """
        self.playable_pipes[pipe_name] += number
        return

    def get_pipe(self, position):
        """
        Acquire the pipe or the tile of the position from the board.
        Access the specific element in board_layout.
        Parameter: position(tuple<int,int>): the row and the column
        Return: Pipe/Tile
        """
        return self.board_layout[position[0]][position[1]]

    def set_pipe(self, pipe, position):
        """
        Set the pipe to the position to replace the tile or another pipe at the given position, 
        while update the information of the number of playable pipes.
        Parameters: 
                    pipe(Pipe): the pipe will be placed at given position.
                    position(tuple<int,int>): the position of board that will be modified.
        """
        self.playable_pipes[pipe.get_name()] += -1
        self.board_layout[position[0]][position[1]] = pipe
        return

    def pipe_in_position(self, position):
        """
        The pipe at the given postion. Determine whether the position is valid
        and whether the type of the element at the position in board_layout is Pipe.
        Parameter: position(tuple<int,int>): the position that will be accessed.
        Return: pipe(Pipe).
        """
        if position is None:
            return None
        elif position[0]>5 or position[1]>5:
            return None
        else:
            pipe = self.get_pipe(position)
            if type(pipe) == Tile:
                return
            else:
                return pipe

    def remove_pipe(self, position):
        """
        Remove the pipe from given position and replace with a Tile.
        Determine whether the selected pipe is selectable, 
        if True, call the change_playable_amount function to modifiy the playable pipes information.
        Parameter: position(tuple<int,int>): the position that will be accessed.
        """
        pipe = self.pipe_in_position(position)
        if pipe._selectable == True:
            self.board_layout[position[0]][position[1]] = Tile('tile',True)
            self.change_playable_amount(pipe.get_name(), 1)
        return

    def position_in_direction(self, direction, position):
        """
        Find the next position and its connected direction to the given position.
        Check the given direction first, then determine the validation of the next position.
        The connected direction is the opposition of given position.
        Parameters: direction(str): The outward direction.The pipe will leave the position through this direction.
                    position(tuple<int,int>)
        Return: (new_direction(str),new_position(tuple<int,int>)): The following position that the pipe connect with and its connected direction."""
        if direction == 'E':
            new_direction = 'W'
            if position[1]+1 <6:
                new_position = (position[0],position[1]+1)
                return (new_direction,new_position)
            else:
                return None
        elif direction == 'S':
            new_direction = 'N'
            if position[0]+1 <6:
                new_position = (position[0]+1,position[1])
                return (new_direction,new_position)
            else:
                return None
        elif direction == 'W':
            new_direction = 'E'
            if position[1]-1 >=0:
                new_position = (position[0],position[1]-1)
                return (new_direction,new_position)
            else:
                return None
        elif direction == 'N':
            new_direction = 'S'
            if position[0]-1 >=0:
                new_position = (position[0]-1,position[1])
                return (new_direction,new_position)
            else:
                return None

    def end_pipe_positions(self):
        """
        Introduce two attributes of PipeGame: Start_position and End_positon.
        Traverse board_layout to find two elements which is the type of StartPipe and Endpipe respectively.
        """
        for i in range(len(self.board_layout)):
            for j in range(len(self.board_layout[i])):
                if type(self.board_layout[i][j]) == StartPipe:
                    self.Start_position=(i,j)
                elif type(self.board_layout[i][j]) == EndPipe:
                    self.End_position=(i,j)
        return

    def get_starting_position(self):
        """
        Get the starting pipe of the game
        Return: Start_position(tuple<int,int>)
        """
        return self.Start_position

    def get_ending_position(self):
        """
        Get the ending pipe of the game
        Return: End_position(tuple<int,int>)
        """
        return self.End_position
    def check_win(self):
        """(bool) Returns True  if the player has won the game False otherwise."""
        position = self.get_starting_position()
        pipe = self.pipe_in_position(position)
        queue = [(pipe, None, position)]
        discovered = [(pipe, None)]
        while queue:
            pipe, direction, position = queue.pop()
            for direction in pipe.get_connected(direction):
                if self.position_in_direction(direction, position) is None:
                    new_direction = None
                    new_position = None
                else:
                    new_direction, new_position = self.position_in_direction(direction, position)
                if new_position == self.get_ending_position() and direction == self.pipe_in_position(new_position).get_connected()[0]:
                    return True
                pipe = self.pipe_in_position(new_position)
                if pipe is None or (pipe, new_direction) in discovered:
                    continue
                discovered.append((pipe, new_direction))
                queue.append((pipe, new_direction, new_position))
            return False
        
            
        
class Tile:
    """A tile represents an available space in the game board. Each tile has a name, and can be
    unlocked/selectable (available to have pipes placed on them) or locked/unselectable (cannot
    have pipes placed on them). By default, tiles should be selectable. Tiles should be constructed
    with Tile(name, selectable=True)."""
    def __init__(self, name, selectable=True):
        """Construct Tile"""
        self._name =  name
        self._selectable = selectable

    def get_name(self):
        """Get the name of the title.
        Return: self._name(str)"""
        return self._name

    def get_id(self):
        """Get the id of title class.
        Return: 'title'"""
        return 'tile'

    def set_select(self, select:bool):
        """Reset the selectable of the tile.
        Return: self._selectable(bool)"""
        self._selectable = select
        return self._selectable

    def can_select(self):
        """Determine whether the tile can be selected.
        Return: True or False"""
        if self._selectable == True:
            return True
        else:
            return False

    def __str__(self):
        """Returns the string representation of the Tile"""
        return "Tile('"+self._name+"', "+str(self._selectable)+')'

    def __repr__(self):
        """Same as str(self)"""
        return "Tile('"+self._name+"', "+str(self._selectable)+')'


class Pipe(Tile):
    """A pipe represents a pipe in the game. Pipes are a special type of Tile, which can be connected
        to other pipes in the game board to form a path. Pipes should be selectable unless they are
        loaded in as part of the game board, e.g. from a file or as part of the initial hard coded game.
        Each pipe has a name, which defines its pipe type (see Appendix B for a list of pipe names and
        their corresponding types), and an orientation."""
    def __init__(self, name, orientation=0, selectable=True):
        """Construct Pipe class which is a subclass of Tile"""
        super(Pipe,self).__init__(name, selectable)
        self._orientation = orientation

    def get_id(self):
        """Get the id of Pipe class.
        Return: 'pipe'"""
        return 'pipe'
    def get_orientation(self):
        """Get the orientation of Pipe.
        Return self._orientation(int)"""
        return self._orientation
    
    def get_connected(self, side):
        """Returns a list of all sides that are
        connected to the given side.
        Determine the name of a pipe and its orientation number,
        Introduce a list of possible direction.
        Finally determine whether the parameter 'side' in the list,
        if not return None, if in, remove it.
        Parameter: side(str): the direction that pipe start
        Return: connect(list<str>): the direction connected by the pipe"""
        connect=[]
        if self._name == PIPES["ST"]:
            if self._orientation == 0 or self._orientation == 2:
                connect = ['N','S']
            elif self._orientation == 1 or self._orientation == 3:
                connect = ['E','W']
        elif self._name == PIPES["CO"]:
            if self._orientation == 0:
                connect = ['N','E']
            elif self._orientation == 1:
                connect = ['E','S']
            elif self._orientation == 2:
                connect = ['S','W']
            elif self._orientation == 3:
                connect = ['W','N']
        elif self._name == PIPES["CR"]:
            connect = ['N','W','S','E']
        elif self._name == PIPES["JT"]:
            if self._orientation == 0:
                connect = ['E','W','S']
            elif self._orientation == 1:
                connect = ['W','S','N']
            elif self._orientation == 2:
                connect = ['N','E','W']
            elif self._orientation == 3:
                connect = ['E','N','S']
        elif self._name == PIPES["DI"]:
            if self._orientation == 0 or self._orientation == 2:
                if side == 'N' or side == 'E':
                    connect = ['N','E']
                else:
                    connect = ['S','W']
            else:
                if side == 'N' or side == 'W':
                    connect = ['N','W']
                else:
                    connect = ['S','E']
        elif self._name == PIPES["OU"]:
            if side == 'N' or side == 'S':
                    connect = ['N','S']
            else:
                    connect = ['E','W']
        if side not in connect:
            connect = []
        elif side in connect:
            connect.remove(side)
        return connect
                

    def rotate(self, direction):
        """Rotates the pipe one turn. A positive direction implies
        clockwise rotation, and a negative direction implies counter-clockwise rotation and 0 means no
        rotation.
        Add the number to orientation, if the sum is invalid, change it to valid by adding 4 or subtracting 4.
        Parameter: direction(int): the rotate direction of a pipe.
        """
        if self._orientation+direction>=0 and self._orientation+direction<=3:
            self._orientation += direction
            
        elif self._orientation+direction<0:
            self._orientation += direction +4
            
        elif self._orientation+direction>3:
            self._orientation += direction - 4
        return
           

    def __str__(self):
        """Returns the string representation of the Pipe"""
        return "Pipe('"+self._name+"', "+str(self._orientation)+')'

    def __repr__(self):
        """Returns the string representation of the Pipe"""
        return "Pipe('"+self._name+"', "+str(self._orientation)+')'

class SpecialPipe(Pipe):
    """SpecialPipe is an abstract class used to represent the start and end pipes in the game (see
    Appendix A). Neither the start nor end pipe should be selectable, and the orientations should be
    fixed."""
    def __init__(self, name, orientation=0, selectable=False):
        """Construct the SpecialPipe class which is a subclass of Pipe"""
        super(SpecialPipe,self).__init__(name,orientation)
        self._selectable = selectable

    def get_id(self):
        """Get the id of SpecialPipe class.
        Return: 'special_pipe'"""
        return 'special_pipe'
    def __str__(self):
        """Returns the string representation of the SpecialPipe"""
        return 'SpecialPipe({0})'.format(self._orientation)

    def __repr__(self):
        """Returns the string representation of the Tile"""
        return 'SpecialPipe({0})'.format(self._orientation)
    
class StartPipe(SpecialPipe):
    """A StartPipe represents the start pipe in the game"""
    def __init__(self,orientation=0, selectable=False):
        """Construct the StartPipe class which is a subclass of SpecialPipe"""
        super(StartPipe,self).__init__(orientation,orientation, selectable)
        self._name='start'

    def get_connected(self,side = None):
        """Returns a list of all sides that are
        connected to the given side.
        Determine the name of a pipe and its orientation number,
        Introduce a list of possible direction.
        Finally determine whether the parameter 'side' in the list,
        if not return None, if in, remove it.
        Parameter: side(str): the direction that pipe start
        Return: connect(list<str>): the direction connected by the pipe"""
        if self._orientation == 0:
            return ['N']
        elif self._orientation == 1:
            return ['E']
        elif self._orientation == 2:
            return ['S']
        elif self._orientation == 3:
            return ['W']
    
    
    def __str__(self):
        """Returns the string representation of the StartPipe"""
        return 'StartPipe({0})'.format(self._orientation)

    def __repr__(self):
        """Returns the string representation of the StartPipe"""
        return 'StartPipe({0})'.format(self._orientation)

    

class EndPipe(SpecialPipe):
    """An EndPipe represents the end pipe in the game."""
    def __init__(self, orientation=0, selectable=False):
        """Consturct the EndPipe class which is a subclass of SpecialPipe"""
        super(EndPipe,self).__init__(orientation,orientation, selectable)
        self._name = 'end'

    def get_connected(self,side = None):
        """Returns a list of all sides that are
        connected to the given side.
        Determine the name of a pipe and its orientation number,
        Introduce a list of possible direction.
        Finally determine whether the parameter 'side' in the list,
        if not return None, if in, remove it.
        Parameter: side(str): the direction that pipe start
        Return: connect(list<str>): the direction connected by the pipe"""
        if self._orientation == 0:
            return ['S']
        elif self._orientation == 1:
            return ['W']
        elif self._orientation == 2:
            return ['N']
        elif self._orientation == 3:
            return ['E']

    def __str__(self):
        """Returns the string representation of the EndPipe"""
        return 'EndPipe({0})'.format(self._orientation)

    def __repr__(self):
        """Returns the string representation of the EndPipe"""
        return 'EndPipe({0})'.format(self._orientation)


   

def main():
    print("Please run gui.py instead")
    

if __name__ == "__main__":
    main()
