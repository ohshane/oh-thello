from itertools import chain

import numpy as np

from misc import *


def blocks(s):
    block_pieces = np.array([[int(i) for i in row] for row in s.split()], dtype=bool)
    if len(block_pieces) == ROW and len(block_pieces[0]) == COL:
        pass
    else: raise Exception('shape error')
    if set(chain.from_iterable(block_pieces)) == {0, 1}:
        pass
    else: raise Exception('value error')
    return block_pieces

class State:
    def __init__(self, pieces=None, enemy_pieces=None, block_pieces=None, depth=0):
        self.pass_end = False
        self.pieces = pieces
        self.enemy_pieces = enemy_pieces
        self.block_pieces = block_pieces
        self.depth = depth
        
        if pieces is None and enemy_pieces is None:
            self.pieces = np.zeros(SIZE, dtype=bool)
            self.pieces[ROW//2-1, COL//2] = 1
            self.pieces[ROW//2, COL//2-1] = 1
            
            self.enemy_pieces = np.zeros(SIZE, dtype=bool)
            self.enemy_pieces[ROW//2-1, COL//2-1] = 1
            self.enemy_pieces[ROW//2, COL//2] = 1
        
        if block_pieces is None:
            self.block_pieces = np.zeros((SIZE), dtype=bool)
    
    @property
    def is_black(self):
        return self.depth % 2 == 0

    @property
    def empty(self):
        return ~((self.pieces | self.enemy_pieces) | self.block_pieces)

    def places(self, pieces) -> np.array:
        return np.transpose(pieces.nonzero())
        
    def count(self, pieces) -> int:
        return len(self.places(pieces))
    
    def is_done(self) -> bool:
        return self.count(self.empty) == 0 or self.pass_end

    def is_lose(self):
        return self.is_done() and self.count(self.pieces) < self.count(self.enemy_pieces)

    def is_draw(self):
        return self.is_done() and self.count(self.pieces) == self.count(self.enemy_pieces)

    def wdl(self):
        if not self.is_done():
            return None
        elif self.count(self.pieces) > self.count(self.enemy_pieces):
            return 1
        elif self.count(self.pieces) < self.count(self.enemy_pieces):
            return -1
        else:
            return 0
    
    def legal_actions(self, flatten=False):
        actions = set()

        for action in self.places(self.pieces):
            look = np.array([True] * len(DIRECTIONS), dtype=bool)
            for i in range(1, max(ROW, COL)):
                next_look = look & np.array([p.tolist() in self.places(self.enemy_pieces).tolist() for p in action + np.array(DIRECTIONS)*i], dtype=bool)
                next_next_look = next_look & np.array([p.tolist() in self.places(self.empty).tolist() for p in action + np.array(DIRECTIONS)*(i+1)], dtype=bool)
                for p in action + (np.array(DIRECTIONS)*(i+1))[next_look & next_next_look]:
                    actions.add(tuple(p))

        actions = list(map(list, actions))
        if flatten:
            actions = [i*ROW+j for i, j in actions]

        return actions

    def next(self, action: list):
        state = State(self.enemy_pieces.copy(), self.pieces.copy(), self.block_pieces, self.depth+1)
        if not self.legal_actions():
            if not state.legal_actions():
                state.pass_end = True
            return state
        elif action in self.legal_actions():
            state.enemy_pieces[action[0], action[1]] = 1
            change = []
            for dir in np.array(DIRECTIONS):
                temp = []
                for i in range(1, max(ROW, COL)):
                    flag = (action + dir*i).tolist()
                    if flag in state.places(state.pieces).tolist():
                        temp.append(flag)
                        continue
                    elif flag in state.places(state.enemy_pieces).tolist():
                        change.extend(temp)
                    break
            
            for i, j in change:
                state.enemy_pieces[i, j] = 1
                state.pieces[i, j] = 0

        return state

    def __repr__(self):
        placeables = self.legal_actions()

        rows = []
        for i in range(ROW):
            row = ''
            for j in range(COL):
                if [i,j] in self.places(self.empty).tolist():
                    if [i,j] in placeables:
                        row += VISUAL_PLACEABLE
                    else:
                        row += VISUAL_EMPTY
                elif [i,j] in self.places(self.block_pieces).tolist():
                    row += VISUAL_BLOCK
                elif [i,j] in self.places(self.pieces).tolist():
                    row += VISUAL_BLACK if self.is_black else VISUAL_WHITE
                elif [i,j] in self.places(self.enemy_pieces).tolist():
                    row += VISUAL_WHITE if self.is_black else VISUAL_BLACK
            rows.append(row)

        rows = [' '.join(row) for i, row in enumerate(rows, start=1)]
        return '\n'.join(rows)
