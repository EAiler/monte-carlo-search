import sys
import random
import datetime
import math
import glob
import datetime
from copy import deepcopy
from collections import defaultdict
from sample_players import DataPlayer
from isolation import Isolation
import pickle
from gamestate import GameState


from isolation import DebugState
from helper import minimax_decision, minimax_alphaBeta
from MonteCarloSearchTree import MonteCarloTreeSearch, Node
from MinimaxAlphaBeta import MinimaxAlphaBetaSearch


class MonteCarloPlayer(DataPlayer):

    def get_action(self, state):
        
        TIME_LIMIT = 150 # milliseconds

        if state.terminal_test() or state.ply_count < 2:
          self.queue.put(random.choice(state.actions()))
        else:
            debug_board = DebugState.from_state(state)
            print(debug_board)
            mcts = MonteCarloTreeSearch(state)
            res = mcts.best_action(TIME_LIMIT)

        if res:
            self.queue.put(res)
        elif state.actions():
            self.queue.put(random.choice(state.actions()))
        else:
            self.queue.put(None)



class MinimaxIterativePlayer(DataPlayer):
   
    def get_action(self, state):
        
        TIME_LIMIT = 150 # milliseconds

        if state.terminal_test() or state.ply_count < 2:
            self.queue.put(random.choice(state.actions()))   
        else:
            minimaxAB = MinimaxAlphaBetaSearch(state, depth=6)
            res = minimaxAB.minimax_alphaBeta(TIME_LIMIT)
  
        if res:
            self.queue.put(res)
        elif state.actions():
            self.queue.put(random.choice(state.actions()))
        else:
            self.queue.put(None)

