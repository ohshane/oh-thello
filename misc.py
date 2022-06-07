ROW = 8
COL = 8
SIZE = (ROW, COL)

DIRECTIONS = (
    (-1, 0),  # N
    (-1, 1),  # NE
    ( 0, 1),  # E
    ( 1, 1),  # SE
    ( 1, 0),  # S
    ( 1,-1),  # SW
    ( 0,-1),  # W
    (-1,-1),  # NW
)

EMPTY = 0
BLOCK = 1
BLACK = 2
WHITE = 3
PLACEABLE = 4

VISUAL_EMPTY = '·'
VISUAL_BLOCK = ' '
VISUAL_BLACK = '●'
VISUAL_WHITE = '◯'
VISUAL_PLACEABLE = '*'
