import itertools
from copy import deepcopy

import pygame as pg

from const import CASTLES
from pieces import Piece, EmptyPiece
from place import Place


class Board:
    def __init__(self, board_list, team='1', selected=None):
        self.board_list = self.create_board(board_list)
        self.team = team
        self.selected = selected

    @staticmethod
    def create_board(board_list):
        return [Piece.from_tile(tile, Place(counter)) for counter, tile in enumerate(board_list)] if type(board_list[0]) is str else board_list

    @property
    def enemy(self):
        return '1' if self.team == '0' else '0'

    @property
    def is_mated(self):
        if not self.is_checked:
            return False
        else:
            for piece in self:
                if piece.team == self.team:
                    for c in range(len(self)):
                        if self.attempt_move(piece.place, Place(c)):
                            return False
            else:
                return True

    def switch_team(self):
        self.team = self.enemy

    def __iter__(self):
        return iter(self.board_list)

    def __getitem__(self, query):
        if type(query) is Place:
            return self.board_list[query.idx]
        elif type(query) is tuple:
            return self.board_list[Place(query).idx]
        elif type(query) in (int, slice):
            return self.board_list[query]

    def __setitem__(self, key, value):
        if type(key) is Place:
            self.board_list[key.idx] = value
        elif type(key) is tuple:
            self.board_list[Place(key).idx] = value
        else:
            self.board_list[key] = value

    def __len__(self):
        return 64

    def copy(self):
        return Board(deepcopy(self.board_list), selected=self.selected, team=self.team)

    def inside_at(self, place):
        x, y = place.coords
        return all((x > 0, x < 9, y > 0, y < 9))

    def empty_at(self, place):
        return type(self[place]) is EmptyPiece

    def enemy_at(self, place):
        return self[place].team == self.enemy

    def move(self, src, tgt, remove=None, end_turn=False):
        if end_turn: self.set_en_passant(src, tgt)

        piece = self[src]
        self[src] = EmptyPiece('*', src)
        piece.place = tgt
        self[tgt] = piece
        if remove:
            self[remove] = EmptyPiece('*', remove)
        if end_turn:
            piece.moved = True
            self.selected = None
            self.switch_team()

    def do_castle(self, castle):
        king_start, king_end = Place(castle.king_change[0]), Place(castle.king_change[1])
        rook_start, rook_end = Place(castle.rook_change[0]), Place(castle.rook_change[1])
        self.move(king_start, king_end)
        self.move(rook_start, rook_end, end_turn=True)

    def attempt_move(self, src, tgt, do_if_possible=False):
        piece = self[src]
        mock_board = self.copy()
        mvs, atks = piece.get_actions(mock_board)

        if piece.id == 'p' and src == piece.can_en_passant[0] and tgt == piece.can_en_passant[1]:
            remove = piece.can_en_passant[2]
            mock_board.move(src, tgt, remove=remove)
            if not mock_board.is_checked:
                self.move(src, tgt, remove, end_turn=True)

        mock_board.move(src, tgt)
        if mock_board.is_checked:
            return False
        else:
            for plc in mvs + atks:
                if tgt == plc:
                    if do_if_possible:
                        self.move(src, tgt, end_turn=True)
                    else:
                        return True
            else:
                return False

    @property
    def is_checked(self):
        for piece in self:
            if piece.team == self.enemy:
                for atk in piece.get_actions(self)[1]:
                    if str(self[atk]) == f'{self.team}i':
                        return True
        else:
            return False

    def attempt_castle(self, src, tgt, do_if_possible=False):
        for castle in CASTLES:
            if (src.coords, tgt.coords) == castle.king_change:
                if self[castle.king_change[0]].moved or self[castle.rook_change[0]].moved:
                    return False if do_if_possible else None
                if not all(map(self.empty_at, castle.move_clear)):
                    return False if do_if_possible else None
                for check in castle.check_clear:
                    mock_board = self.copy()
                    mock_board.move(castle.king_change[0], Place(check))
                    if mock_board.is_checked:
                        return False if do_if_possible else None
                else:
                    if do_if_possible:
                        self.do_castle(castle)
                        return True
                    else:
                        return castle

    def set_en_passant(self, src, tgt):
        piece = self[src]
        src_x, src_y = src.coords
        tgt_x, tgt_y = tgt.coords
        if piece.id == 'p' and abs(tgt_y - src_y) == 2:
            for addx, addy in ((1, 0), (-1, 0)): #TODO refactor
                plc = Place((tgt_x + addx, tgt_y + addy))
                if self.inside_at(plc) and str(self[plc]) == f'{self.enemy}p':
                    self[plc].can_en_passant = (plc, Place((src_x, (tgt_y + src_y) // 2)), tgt) #GOTO; ATTACK

    def update_board(self, plc):
        clicked_place = plc
        clicked_piece = self[clicked_place]
        if clicked_piece.team == self.team:
            self.selected = clicked_place
        elif clicked_place == self.selected:
            self.selected = None
        elif self.selected is not None:
            did_castle = self.attempt_castle(self.selected, clicked_place, do_if_possible=True)
            if not did_castle:
                self.attempt_move(self.selected, clicked_place, do_if_possible=True)


class VisualBoard(Board):
    WHITE = (255, 255, 255)
    BLACK = (45, 90, 181)
    SELECTED_COLOR = (235, 249, 43)

    def __init__(self, board_list, screen, size, should_change_seats=True):
        super().__init__(self.create_board(board_list))
        self.screen = screen
        self.size = size
        self.square_size = size // 8
        self.surface = pg.Surface((self.size, self.size)).convert()
        self.color = itertools.cycle((self.WHITE, self.BLACK))
        self.should_change_seats = should_change_seats

    @property
    def rotation_deg(self):
        return 0 if self.team == '1' else 180

    def blit_piece(self, place, pixel_coords):
        img = pg.image.load(f'resources/{self[place]}.png').convert_alpha()
        piece = pg.transform.scale(pg.transform.rotate(img, self.rotation_deg),
                                          (self.square_size, self.square_size))
        self.surface.blit(piece, pixel_coords)

    def blit_all(self):
        x, y = 0, 0
        squares = []
        for n in range(64):
            square = pg.Surface((self.square_size, self.square_size)).convert()
            if self.selected and n == self.selected.idx:
                next(self.color)
                square.fill(self.SELECTED_COLOR)
            else:
                square.fill(next(self.color))
            squares.append(self.surface.blit(square, (x, y)))
            if not self.empty_at(n):
                self.blit_piece(Place(n), (x, y))
            if (n + 1) % 8 == 0:
                y += self.square_size
                x = 0
                next(self.color)
            else:
                x += self.square_size
        self.screen.blit(pg.transform.rotate(self.surface, self.rotation_deg), (0, 0))
        return squares






