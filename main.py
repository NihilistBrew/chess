from board import Board
from const import START_BOARD
from place import Place

TEAMS = {'1': 'White', '0': 'Black'}

board = Board(START_BOARD)
team = '1'
#board.print_out()

playing = True
while playing:
    board.print_out()
    moved = False
    while not moved:
        inp = input(f'\n\n{TEAMS[team]}, (Start) (End): ')
        transl_inp = Place.translate_inp_place(inp).split(' ')
        start, end = Place(transl_inp[0]), Place(transl_inp[1])
        if board.can_move(start, end):
            board.move(start, end)
            moved = True
        else:
            print('Move errored, try again!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')





