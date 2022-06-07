import random
import time

from components import State, blocks
from misc import *

block = blocks('''11100111
                  11000011
                  10000001
                  00000000
                  00000000
                  10000001
                  11000011
                  11100111''')

state = State(block_pieces=block)

while True:
    print(f'depth: {state.depth}')
    print(f'turn : {"BLACK" if state.is_black else "WHITE"}')
    print(state)
    print('-'*30)

    if state.is_done():
        print(f'{"BLACK" if state.is_black else "WHITE"}', end=' ')
        wdl = state.wdl()
        if wdl == 1:
            print("WIN")
        elif wdl == 0:
            print("DRAW")
        elif wdl == -1:
            print("LOOSE")
        
        print(state.count(state.pieces))
        print(state.count(state.enemy_pieces))
        print(state.count(state.block_pieces))
        break

    actions = state.legal_actions()
    if actions:
        state = state.next(random.choice(actions))
    else:
        state = state.next(None)
