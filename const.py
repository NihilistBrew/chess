from collections import namedtuple

START_BOARD = ['0r', '0k', '0b', '0q', '0i', '0b', '0k', '0r',
               '0p', '0p', '0p', '0p', '0p', '0p', '0p', '0p',
               '**', '**', '**', '**', '**', '**', '**', '**',
               '**', '**', '**', '**', '**', '**', '**', '**',
               '**', '**', '**', '**', '**', '**', '**', '**',
               '**', '**', '**', '**', '**', '**', '**', '**',
               '1p', '1p', '1p', '1p', '1p', '1p', '1p', '1p',
               '1r', '1k', '1b', '1q', '1i', '**', '**', '1r']

Castle = namedtuple('Castle', 'team length king_change rook_change move_clear check_clear')

CASTLES = [
    Castle(team='0',
           length='short',
           king_change=((5, 1), (7, 1)),
           rook_change=((8, 1), (6, 1)),
           move_clear=((6, 1), (7, 1)),
           check_clear=((6, 1), (7, 1))),
    Castle(team='0',
           length='long',
           king_change=((5, 1), (3, 1)),
           rook_change=((1, 1), (4, 1)),
           move_clear=((2, 1), (3, 1), (4, 1)),
           check_clear=((3, 1), (4, 1))),
    Castle(team='1',
           length='short',
           king_change=((5, 8), (7, 8)),
           rook_change=((8, 8), (6, 8)),
           move_clear=((6, 8), (7, 8)),
           check_clear=((6, 8), (7, 8))),
    Castle(team='1',
           length='long',
           king_change=((5, 8), (3, 8)),
           rook_change=((1, 8), (4, 8)),
           move_clear=((2, 8), (3, 8), (4, 8)),
           check_clear=((3, 8), (4, 8)))
    ]
