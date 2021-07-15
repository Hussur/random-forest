from a1_support import *
grid_size=0
game = str()
number_of_pokemons = 0

def find(char,string):
    """find the position of specific char in string"""
    for raw,c in enumerate(string):
        if c == char:
            return raw

def display_game(game, grid_size):
    """This function prints out a grid-shaped representation of the game, given the game string and the grid size as arguments.
       Parameters:
 		game (str): Game string.
 		grid_size (int): Size of game.
 	Returns:
 		print the game as a table."""
    print('  ',end="")
    for i in range(1,grid_size+1):
        print(WALL_VERTICAL+str(i).center(3,' '),end="")
    print(WALL_VERTICAL)
    print(4*(grid_size+1)*WALL_HORIZONTAL)
    for m in range(grid_size):
        print(ALPHA[m],'',end="")
        for n in range(grid_size):
            print(WALL_VERTICAL,game[m*grid_size+n],'',end="")
        print(WALL_VERTICAL)
        print(4*(grid_size+1)*WALL_HORIZONTAL)
    return

def parse_position(action,grid_size): 
    """This function checks if the input action is in a valid format. i.e it checks if the entered action 
    in Table 1. If a non-valid action is entered, None should be returned. If the action is "Select a cell" or
     "Flag remove a cell", the position of the cell should be returned as a tuple.
     Parameters:
 		action(str): The action player want to do, including aquiring help, flagging, selecting a cell, restart and quit the game.
 		grid_size (int): Size of game.
 	Returns:
 		tuple<int>: The raw and column of a cell."""
    if len(action)==0:
        return
    elif action == 'h' or action == 'q':
        return
    elif len(action)==1:
        return
    elif action[0] in ALPHA[:grid_size]:
        if len(action)==1 or action[1] in ALPHA or action[1] in "abcdefghigklmnopqrstuvwxyz":
            return
        elif int(action[1:]) in range(1,grid_size+1):        
            position=(find(action[0],ALPHA),int(action[1:])-1)
            return position
        else:
            return
    elif action[:2] == 'f ':
        if action[2] in ALPHA[:grid_size] and int(action[3:]) in range(1,grid_size+1):  
            position=(find(action[2],ALPHA),int(action[3:])-1)
            return position
        else:
            return
    else:
        return

def position_to_index(position, grid_size):
    """This function should convert the row, column coordinate in the grid to the game strings index. The function
    returns an integer representing the index of the cell in the game string.
    Parameters:
 		position(tuple): raw and column of a cell.
 		grid_size (int): Size of game.
 	Returns:
 		index(int): the position of a cell in game string."""
    index = position[0]*grid_size + position[1]
    return index
    

def replace_character_at_index(game, index, character):
    """This function returns an updated game string with the speciled character placed at the specified index.
        Parameters:
 		game (str): Game string.
 		index(int): The position of a cell in game string.
 		character(str): The string should be replaced in a cell.
 	Returns:
 		game (str): New Game string."""
    game = game[:index]+character+game[index+1:]
    return game

def flag_cell(game, index):
    """This function returns an updated game string after "toggling" the ag at the specified index in the game string.
        Parameters:
 		game (str): Game string.
 		index(int): The position of a cell in game string.

 	Returns:
 		game (str): New Game string."""
    if game[index] == UNEXPOSED:
        game = game[:index] + FLAG + game[index+1:]
    else:
        game = game [:index] + UNEXPOSED +game[index+1:]
    return game
    
def index_in_direction(index, grid_size, direction):
    """This function takes in the index to a cell in the game string and returns a new index corresponding to an adjacent cell in the specified directions.
        Parameters:
 		grid_size (int): Size of game.
 		index(int): The position of a cell in game string.
 		direction(str): the direction of neighbour cells. 
 	Returns:
 		neighbour index(int): The position of a neighbour cell in game string"""
    new_index = None
    if direction == DIRECTIONS[0]:
        if index>=grid_size:
            new_index = index - grid_size
    elif direction == DIRECTIONS[1]:
        if index<grid_size*(grid_size-1):
            new_index = index + grid_size     
    elif direction == DIRECTIONS[2]:
        if index%grid_size!=0:
            new_index = index - 1
    elif direction == DIRECTIONS[3]:
        if index%grid_size!=grid_size-1:
            new_index = index + 1
    elif direction == DIRECTIONS[4]:
        if index>=grid_size and index%grid_size!=0:
            new_index = index - (grid_size+1)
    elif direction == DIRECTIONS[5]:
        if index>=grid_size and index%grid_size!=grid_size-1:
            new_index = index - (grid_size-1)
    elif direction == DIRECTIONS[6]:
        if index<grid_size*(grid_size-1) and index%grid_size!=0:
            new_index = index + (grid_size-1)
    elif direction == DIRECTIONS[7]:
        if index<grid_size*(grid_size-1)and index%grid_size!=grid_size-1:
            new_index = index + (grid_size+1)
    return new_index         

def big_fun_search(game, grid_size, pokemon_locations, index):
    """ Searching adjacent cells to see if there are any Pokemon"s present.
 	Using some sick algorithms.
 	Find all cells which should be revealed when a cell is selected.
 	For cells which have a zero value (i.e. no neighbouring pokemons) all the cell"s
 	neighbours are revealed. If one of the neighbouring cells is also zero then
    all of that cell"s neighbours are also revealed. This repeats until no zero value neighbours exist.
 	For cells which have a non-zero value (i.e. cells with neightbour pokemons), onlythe cell itself is revealed.
 	Parameters:
 		game (str): Game string.
 		grid_size (int): Size of game.
 		pokemon_locations (tuple<int, ...>): Tuple of all Pokemon's locations.
 		index (int): Index of the currently selected cell
 	Returns:
 		(list<int>): List of cells to turn visible."""
    queue = [index]
    discovered = [index]
    visible = []

    if game[index] == FLAG:
        return queue
    number = number_at_cell(game, pokemon_locations, grid_size, index)

    if number != 0:
        return queue

    while queue:
        node = queue.pop()
        for neighbour in neighbour_directions(node, grid_size):
            if neighbour in discovered or neighbour is None:
                continue
            discovered.append(neighbour)
            if game[neighbour] != FLAG:
                number = number_at_cell(game, pokemon_locations, grid_size, neighbour)
                if number == 0:
                    queue.append(neighbour)
            visible.append(neighbour)
    return visible

def neighbour_directions(index,grid_size):
    """This function returns a list of indexes that have a neighbouring cell. (Note that the cells at the edges of the
        grid do not have all possible directions).
        Parameters:		
 		grid_size (int): Size of game.
 		index (int): Index of the currently selected cell
 	Returns:
 		(list<int>): List of neighbour cells of a cell."""
    neighbour = []
    for i in range(len(DIRECTIONS)):
        if index_in_direction(index, grid_size, DIRECTIONS[i])!=None:
            neighbour.append(index_in_direction(index, grid_size, DIRECTIONS[i]))
    return neighbour       

def number_at_cell(game, pokemon_locations, grid_size, index):
    """This function returns the number of Pokemon in neighbouring cells.
        Parameters:		
                game (str): Game string.
                pokemon_locations (tuple<int, ...>): Tuple of all Pokemon's locations.
 		grid_size (int): Size of game.
 		index (int): Index of the currently selected cell
 	Returns:
 		num(int): The number of neighbour pokemons of a cell."""
    num = 0
    neighbour_index = neighbour_directions(index,grid_size)
    for i in range(len(pokemon_locations)):
        if pokemon_locations[i] in neighbour_index:
            num +=1
    game = game[:index] + str(num) + game[index+1:]
    
    return num

def check_win(game,pokemon_locations):
    """This function returns True if the player has won the game, and returns False otherwise.
        Parameters:		
                game (str): Game string.
                pokemon_locations (tuple<int, ...>): Tuple of all Pokemon's locations.
 	Returns:
 		bool"""
    num_of_flag=0
    for i in range(len(game)):
        if FLAG==game[i]:
            num_of_flag+=1
    if num_of_flag>len(pokemon_locations):
        return False
    for i in range(len(pokemon_locations)):
        if game[pokemon_locations[i]] == FLAG and UNEXPOSED not in game:
            return True
        else:
            return False

def main():
    """This function handles player interaction. At the start of the game the player should be prompted."""
    grid_size = int(input('Please input the size of the grid: '))
    number_of_pokemons = int(input('Please input the number of pokemons: '))
    game = grid_size*grid_size*UNEXPOSED
    pokemon_locations = generate_pokemons(grid_size, number_of_pokemons)
    display_game(game,grid_size)
    while UNEXPOSED in game:
        action = input('\n'+'Please input action: ')
        if action == 'h':
            print(HELP_TEXT)
            display_game(game,grid_size)    
        elif action == 'q':
            q = input('You sure about that buddy? (y/n): ')
            if q=='y':
                print('Catch you on the flip side.')
                return
            elif q=='n':
                print("Let's keep going.")
                display_game(game,grid_size)
            else:
                print("That ain't a valid action buddy.")
                display_game(game,grid_size)
        elif action ==':)':
            print("It's rewind time.")
            game = grid_size*grid_size*UNEXPOSED
            pokemon_locations = generate_pokemons(grid_size, number_of_pokemons)
            display_game(game, grid_size)
            continue
        elif action=='':
            print("That ain't a valid action buddy.")
            display_game(game,grid_size)
        elif action[0] not in ALPHA: 
            if action[:2]=='f ':
                if action[2] in 'abcdefghigklmnopqrstuvwxyz':
                    print("That ain't a valid action buddy.")
                    display_game(game,grid_size)
                elif int(action[3:]) in range(1,grid_size+1):
                    position = parse_position(action,grid_size)
                    index = position_to_index(position,grid_size)
                    if game[index]==UNEXPOSED:
                        game = flag_cell(game, index)
                    elif game[index]==FLAG:
                        game = replace_character_at_index(game,index,UNEXPOSED)
                    else:
                        print("That ain't a valid action buddy.")
                    display_game(game,grid_size)
                else:
                    print("That ain't a valid action buddy.")
                    display_game(game,grid_size)
            else:
                print("That ain't a valid action buddy.")
                display_game(game,grid_size)
        elif action[0] in ALPHA[:grid_size] and int(action[1:]) in range(1,grid_size+1):
            position = parse_position(action,grid_size)
            index = position_to_index(position,grid_size)
            if game[index]!=UNEXPOSED:
                display_game(game,grid_size)
            elif index in pokemon_locations:
                for i in range(len(pokemon_locations)):
                    game = replace_character_at_index(game, pokemon_locations[i],POKEMON )
                display_game(game,grid_size)
                print('You have scared away all the pokemons.')
                return
            elif game[index]==UNEXPOSED:
                game = replace_character_at_index(game,index,str(number_at_cell(game,pokemon_locations, grid_size, index)) )
                Nonadjacent = big_fun_search(game, grid_size, pokemon_locations, index)
                for i in range(len(Nonadjacent)):
                    if game[Nonadjacent[i]]!=FLAG:
                        game = replace_character_at_index(game, Nonadjacent[i],str(number_at_cell(game, pokemon_locations, grid_size, Nonadjacent[i])))
                display_game(game,grid_size)
        else:
            print("That ain't a valid action buddy.")
            display_game(game,grid_size)
    if check_win(game,pokemon_locations) is True:
            print('You win.')   
    pass




if __name__ == "__main__":
    main()
