import pygame as pg

from board import VisualBoard
from const import START_BOARD

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
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                for c, square in enumerate(squares):
                    if square.collidepoint(*event.pos):
                        board.update_visual(c)
                board.blit_all()
                pg.display.flip()
main()



