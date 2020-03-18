def print_actions_for(self, place):
    piece = self[place]
    display_board = Board(self.board_list)
    display_board[place] = 'OO'
    gotos, attacks = piece.get_actions(self)
    for goto in gotos:
        display_board[goto] = 'GG'
    for attack in attacks:
        display_board[attack] = 'AA'

    display_board.print_out()


def inside_at(self, place):
    x, y = place.coords
    return all((x > 0, x < 9, y > 0, y < 9))


def print_out(self):
    s = ''
    for row in range(8):
        slc = self[row*8:row*8+8]
        s += ' '.join(str(i) for i in slc) + ' ' + str(8-row) + '\n'
    s += '  '.join(ascii_lowercase[:8])
    print(s)