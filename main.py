import random
import os

n = 9
mines = 10
debug = False
board = None
numbers = None
MINE = -1
mask = None
flags = None

hide = False



def make_mask():
    global mask
    mask = []
    for i in range(n):
        mask.append([])
        for j in range(n):
            mask[i].append(0)

def make_flags():
    global flags
    flags = []
    for i in range(n):
        flags.append([])
        for j in range(n):
            flags[i].append(0)

def make_board():
    global board
    board = []
    for i in range(n):
        board.append([])
        for j in range(n):
            board[i].append(0)

def place_mines():
    global board
    for t in range(mines):
        i, j = int(random.random() * n), int(random.random() * n)
        if get_board(i,j) == MINE:
            t-=1
            continue
        board[i][j] = MINE

def get_board(i,j):
    if i < 0 or i >= n or j < 0 or j >= n:
        return 0
    return board[i][j]

def get_number(i,j):
    if i < 0 or i >= n or j < 0 or j >= n:
        return 0
    return numbers[i][j]

def get_mask(i,j):
    if i < 0 or i >= n or j < 0 or j >= n:
        return 1
    return mask[i][j]
    
def make_numbers():
    global numbers
    numbers = []
    for i in range(n):
        numbers.append([])
        for j in range(n):
            numbers[i].append(0)
    for i in range(n):
        for j in range(n):
            if get_board(i,j) == MINE:
                numbers[i][j] = 9
                continue
            neighbours = [(i+I,j+J) for I in [-1,0,1] for J in [-1,0,1]]
            for p in neighbours:
                i_, j_ = p
                if get_board(i_,j_) == MINE:
                    try:
                        numbers[i][j]+=1
                    except:
                        pass

make_board()
place_mines()
make_numbers()
make_mask()
make_flags()

def get_flag():
    return '\x1b[1;31;40m' + ' P ' + '\x1b[0m'

def get_question_mark():
    return '\x1b[1;35;40m' + ' ? ' + '\x1b[0m'

def get_blank():
    return '\x1b[0;30;47m' + '   ' + '\x1b[0m'

def get_character(num):
    if num == 0:
        return '\x1b[6;30;40m' + '   ' + '\x1b[0m'
    if num == 1:
        return '\x1b[1;37;44m' + ' 1 ' + '\x1b[0m'
    elif num == 2:
        return '\x1b[1;37;42m' + ' 2 ' + '\x1b[0m'
    elif num == 3:
        return '\x1b[1;37;41m' + ' 3 ' + '\x1b[0m'
    elif num == 4:
        return '\x1b[1;37;45m' + ' 4 ' + '\x1b[0m'
    elif num == 5:
        return '\x1b[1;37;45m' + ' 5 ' + '\x1b[0m'
    elif num == 6:
        return '\x1b[1;37;45m' + ' 6 ' + '\x1b[0m'
    elif num == 7:
        return '\x1b[1;37;45m' + ' 7 ' + '\x1b[0m'
    elif num == 8:
        return '\x1b[1;37;45m' + ' 8 ' + '\x1b[0m'
    elif num == 9:
        return '\x1b[1;37;45m' + ' 9 ' + '\x1b[0m'

i_player = 0
j_player = 0

def move_player(i,j):
    global i_player, j_player
    if i >= 0 and j>=0 and i < n and j < n:
        i_player, j_player = i,j

def explode(i,j):
    global mask
    if get_board(i,j) == MINE:
        return
    try:
        mask[i][j] = 1
    except:
        pass
    if get_number(i,j) == 0:
        neighbours = [(i+I,j+J) for I in [-1,0,1] for J in [-1,0,1]]
        for p in neighbours:
            i_, j_ = p
            if get_mask(i_,j_)==0:
                explode(i_,j_)

def render():
    global hide
    s = ""
    for i in range(n):
        for j in range(n):
            char = "   "
            
            if get_mask(i,j) == 1:
                char = str(get_character(get_number(i,j)))
            else:
                char = get_blank()
            if i == i_player and j == j_player and not hide:
                char = ' x '

            if flags[i][j]%3 == 1:
                char = get_flag()
            if flags[i][j]%3 == 2:
                char = get_question_mark()
            s+=char
        if not debug:
            s+="\n"
            continue
        s+="\t\t\t\t"
        for j in range(n):
            s+=str(numbers[i][j])+" "
        s+="\t\t\t\t"
        for j in range(n):
            s+=str(mask[i][j])+" "
        s+="\n"
    print(s)

def check_loss(i,j):
    if get_board(i,j) == MINE:
        return True
    return False

def check_win():
    for i in range(n):
        for j in range(n):
            if get_mask(i,j) == 0 and get_board(i,j)!=MINE:
                return False
    return True

def cls():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    global hide
    cls()
    while True:
        render()
        inp = input()
        cls()
        if inp == 'w':
            move_player(i_player-1,j_player)
        if inp == 's':
            move_player(i_player+1,j_player)
        if inp == 'a':
            move_player(i_player,j_player-1)
        if inp == 'd':
            move_player(i_player,j_player+1)
        if inp == 'h':
            hide = not hide
        if inp == 'q':
            break
        if inp == 'f' and get_mask(i_player,j_player) == 0:
            try:
                flags[i_player][j_player] += 1
            except:
                pass
        if inp == 'j':
            if check_loss(i_player,j_player):
                print("GAME OVER")
                break
            explode(i_player, j_player)
        if check_win():
            print("VICTORY")
            break

main()