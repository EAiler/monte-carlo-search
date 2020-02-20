import numpy as np
from isolation import Isolation
import random
from copy import deepcopy
import datetime
import math
from collections import defaultdict


class MinimaxAlphaBetaSearch():


    def __init__(self, state, depth):
        self.state = state
        self.num_visits = 0
        self.depth = depth

  
  
    def minimax_alphaBeta(self, TIME_LIMIT, depth=3):
      """ Return the move along a branch of the game tree that
      has the best possible value.  A move is a pair of coordinates
      in (column, row) order corresponding to a legal move for
      the searching player.
      
      You can ignore the special case of calling this function
      from a terminal state.
      """
      time_out = TIME_LIMIT
      start = datetime.datetime.now()
      while time_out > 15:
        
        
        alpha = float("-inf")
        beta = float("inf")
        best_score = float("-inf")
        best_move = None

        for a in self.state.actions():
            v = self.min_value_alphaBeta(self.state.result(a), self.depth - 1, alpha, beta, TIME_LIMIT, start)
            if v > best_score:   
                best_score = v
                best_move = a

        end = datetime.datetime.now()
        time_out -= (end-start).total_seconds()*1000
        time_out = math.floor(time_out)
        # increase the depth that can be searched
        self.depth += 1

      return best_move

    def min_value_alphaBeta(self, state, depth, alpha, beta, TIME_LIMIT, start):
      if state.terminal_test():
          return state.utility(0)
      if depth <= 0 or (self.tick_tock(start, TIME_LIMIT)<10):
          return self.score(state)

      v = float("inf")
      for a in state.actions():
          self.num_visits += 1 # for each node increase the count by 1
          v = min(v, self.max_value_alphaBeta(state.result(a), depth - 1, alpha, beta, TIME_LIMIT, start))
          if v <= alpha:
              return v
          beta = min(beta, v)
      return v

    def max_value_alphaBeta(self, state, depth, alpha, beta, TIME_LIMIT, start):
      if state.terminal_test(): 
          return state.utility(0)
      if depth <= 0 or (self.tick_tock(start, TIME_LIMIT)<10):
          return self.score(state)
      
      v = float("-inf")
      for a in state.actions():
        self.num_visits += 1 # for each node increase the count by 1
        v = max(v, self.min_value_alphaBeta(state.result(a), depth - 1, alpha, beta, TIME_LIMIT, start))
        if v >= beta:
            return v
        alpha = max(alpha, v)

      return v  
    


    def tick_tock(self, start, TIME_LIMIT):
       return(math.floor(TIME_LIMIT - (datetime.datetime.now()-start).total_seconds()*1000))

    def score(self, state):
      return(self.diff_moves(state)) 

    def close_moves(self, state):
      """ higher value for possible close moves to opponent """
      own_loc = state.locs[state.player()]
      opp_loc = state.locs[1 - state.player()]

      own_liberties = state.liberties(own_loc)
      
      if opp_loc == None:
        return(float("-inf"))
      else:
        close_move = sum([abs(x - opp_loc) for x in own_liberties])
        return(1/(20*close_move))
    
    def diff_moves(self, state):
      """ return number of possible moves """
      own_loc = state.locs[state.player()]
      opp_loc = state.locs[1 - state.player()]
     
      own_liberties = state.liberties(own_loc)
      opp_liberties = state.liberties(opp_loc)
      return len(own_liberties) - 2 * len(opp_liberties)