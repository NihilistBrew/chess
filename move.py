import pygame as pg

from board import VisualBoard
from const import START_BOARD
from place import Place

DIM = 700


def main():
    pg.init()
    screen = pg.display.set_mode((DIM, DIM))
    board = VisualBoard(START_BOARD, screen, DIM)
    squares = board.blit_all()
    clock = pg.time.Clock()
    pg.display.flip()
    while 1:
        clock.tick(60)
        if board.is_mated: print('done'); return
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                for c, square in enumerate(squares):
                    if square.collidepoint(*event.pos):
                        targeted = Place(c) if board.team == '1' else Place(c).inverted()
                        board.update_board(targeted)
                board.blit_all()
                #screen.blit(pg.transform.rotate(board.surface, 180), (0, 0))
                pg.display.flip()
main()



