from a1_support import *
game = 25*['~']
def find(char,string):
        for raw,c in enumerate(string):
            if c == char:
                return raw
def parse_position(action,grid_size):
        #return different tasks after enter orders    
        if action == 'h':
            print(HELP_TEXT)
        elif action == 'q':
            q = input('You sure about that buddy? (y/n): ')
            if q=='y':
                exit()
            elif q=='n':
                print("Let's keep going.")
        #elif action == ':)':
           # python = sys.executable
           # os.execl(python,python,*sys.argv)
        elif action[0] in ALPHA[:grid_size] and int(action[1]) in range(1,grid_size):        
            position=(find(action[0],ALPHA),int(action[1])-1)
        elif action[0] == 'f' and action[1] in ALPHA[:grid_size] and int(action[2]) in range(1,grid_size):  
            position=(find(action[1],ALPHA),int(action[2])-1)
        else:
            print('INVALID')
        return position
def position_to_index(position, grid_size):              
        index = position[0]*grid_size + position[1]
        return index
def replace_character_at_index(game, index, character):
        game[index] = character
        return game
position = parse_position('B3',5)
index = position_to_index(position, 5)
replace_character_at_index(game, index, 2)


