from place import Place


class Piece:
    def __init__(self, team, place, id, moved=False):
        self.team = team
        self.place = place
        self.id = id
        self.moved = moved

    def __repr__(self):
        return f'{self.team}{self.id}'

    @property
    def enemy(self):
        return '1' if self.team == '0' else '0'

    def enemy_at(self, board, place):
        return board[place].team == self.enemy

    @classmethod
    def from_tile(cls, tile, place):
        team, id = tile
        for subclass in cls.__subclasses__():
            if subclass.ID == id:
                return subclass(team=team, place=place)
        else:
            return -1


class EmptyPiece(Piece):
    ID = '*'

    def __init__(self, team, place):
        super().__init__(team, place, self.ID)


class Rook(Piece):
    ID = 'r'

    def __init__(self, team, place):
        super().__init__(team, place, self.ID)

    def get_actions(self, board):
        goto = []
        attack = []
        x, y = self.place.coords

        for axis in ('x', 'y'):
            for sign in (1, -1):
                for n in range(1, 8):
                    plc = Place((x + n * sign, y)) if axis == 'x' else Place((x, y + n * sign))
                    if not board.inside_at(plc):
                        break
                    elif board.empty_at(plc):
                        goto.append(plc)
                    elif self.enemy_at(board, plc):
                        attack.append(plc)
                        break
                    else:
                        break

        return goto, attack


class Bishop(Piece):
    ID = 'b'

    def __init__(self, team, place):
        super().__init__(team, place, self.ID)

    def get_actions(self, board):
        goto = []
        attack = []
        x, y = self.place.coords
        for sign in ((1, 1), (-1, 1), (1, -1), (-1, -1)):
            signx, signy = sign
            for n in range(1, 8):  # Magnitude
                plc = Place((x + n * signx, y + n * signy))
                if not board.inside_at(plc):  # Don't want to raise an error later on
                    break
                elif board.empty_at(plc):
                    goto.append(plc)
                elif self.enemy_at(board, plc):  # Can attack
                    attack.append(plc)
                    break
                else:
                    break

        return goto, attack


class Knight(Piece):
    ID = 'k'

    def __init__(self, team, place):
        super().__init__(team, place, self.ID)

    def get_actions(self, board):
        goto = []
        attack = []
        x, y = self.place.coords
        adders = ((1, -2), (2, -1), (2, 1), (1, 2),
                  (-1, 2), (-2, 1), (-2, -1), (-1, -2)
                  )
        for adder in adders:
            addx, addy = adder
            plc = Place((x + addx, y + addy))
            if not board.inside_at(plc):  # Don't want to raise an error later on
                continue
            elif board.empty_at(plc):
                goto.append(plc)
            elif self.enemy_at(board, plc):  # Can attack
                attack.append(plc)

        return goto, attack


class Queen(Piece):
    ID = 'q'

    def __init__(self, team, place):
        super().__init__(team, place, self.ID)

    def get_actions(self, board):
        # hey, as long as it works
        rook_goto, rook_attack = Rook(self.team, self.place).get_actions(board)
        bishop_goto, bishop_attack = Bishop(self.team, self.place).get_actions(board)
        return rook_goto + bishop_goto, rook_attack + bishop_attack


class King(Piece):
    ID = 'i'

    def __init__(self, team, place):
        super().__init__(team, place, self.ID)

    def get_actions(self, board):
        goto = []
        attack = []
        x, y = self.place.coords
        for adder in ((0, 1), (0, -1),
                      (1, 0), (1, 1), (1, -1),
                      (-1, 0), (-1, 1), (-1, -1)
                      ):
            addx, addy = adder
            plc = Place((x + addx, y + addy))
            if not board.inside_at(plc):
                continue
            elif board.empty_at(plc):
                goto.append(plc)
            elif self.enemy_at(board, plc):
                attack.append(plc)

        return goto, attack


class Pawn(Piece):
    ID = 'p'

    def __init__(self, team, place):
        super().__init__(team, place, self.ID)

    def get_actions(self, board):
        goto = []
        attack = []
        x, y = self.place.coords
        upper = 2 if self.moved else 3
        sign = 1 if self.team == '0' else -1
        for n in range(1, upper):
            plc = Place((x, y + n * sign))
            if not board.inside_at(plc):  # Don't want to raise an error later on
                break
            elif board.empty_at(plc):
                goto.append(plc)
            else:
                break
        for plc in (Place((x + 1, y + 1 * sign)), Place((x - 1, y + 1 * sign))):
            if self.enemy_at(board, plc):
                attack.append(plc)

        return goto, attack
