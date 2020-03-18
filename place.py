from string import ascii_lowercase


class Place:
    notation = dict(zip(ascii_lowercase, range(1, 9)))

    def __init__(self, obj, en_passant=False):
        if type(obj) is int:
            self.idx = obj
            self.coords = self.idx_to_coords(obj)
            self.notation = self.coords_to_notation(self.coords)

        elif type(obj) is tuple:
            self.coords = obj
            self.idx = self.coords_to_idx(obj)
            self.notation = self.coords_to_notation(obj)

        elif type(obj) is str:
            self.notation = obj
            self.coords = self.notation_to_coords(obj)
            self.idx = self.coords_to_idx(self.coords)

        else:
            self.idx, self.coords, self.scoords = None, None, None

        self.en_passant = en_passant

    def __eq__(self, other):
        if type(other) is self.__class__:
            return self.idx == other.idx
        else:
            return False

    @staticmethod
    def coords_to_idx(coords):
        x, y = coords
        return (int(y) - 1) * 8 + int(x) - 1

    @staticmethod
    def idx_to_coords(idx):
        for x in range(1, 9):
            for y in range(1, 9):
                if Place.coords_to_idx((x, y)) == idx:
                    return x, y

    @staticmethod
    def coords_to_notation(coords):
        x, y = coords
        for letter, number in Place.notation.items():
            if number == x:
                return letter + str(y)

    @staticmethod
    def notation_to_coords(notation):
        return Place.notation[notation[0]], int(notation[1])

    @staticmethod
    def translate_inp_place(inp):
        new_s = ''
        for char in str(inp):
            new_s += str(9 - int(char)) if char.isdigit() else char
        return new_s

    def inverted(self):
        return Place(63 - self.idx)