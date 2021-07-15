from a1_support import *
game = '~~~~~~~~~~9~~~~~☺~~~♥~~~~'
def display_game(game, grid_size):
    #Initialize the game
    
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
