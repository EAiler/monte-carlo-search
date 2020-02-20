
import sys
import random
import datetime
import math
import glob
from collections import defaultdict
from sample_players import DataPlayer

from gamestate import GameState
from isolation import DebugState
#from helper import minimax_decision, minimax_alphaBeta
from MonteCarloSearchTree import MonteCarloTreeSearch, Node
from MinimaxAlphaBeta import MinimaxAlphaBetaSearch
import pickle

class CustomPlayer(DataPlayer):
    """ Implement your own agent to play knight's Isolation

    The get_action() method is the only required method for this project.
    You can modify the interface for get_action by adding named parameters
    with default values, but the function MUST remain compatible with the
    default interface.

    **********************************************************************
    NOTES:
    - The test cases will NOT be run on a machine with GPU access, nor be
      suitable for using any other machine learning techniques.

    - You can pass state forward to your agent on the next turn by assigning
      any pickleable object to the self.context attribute.
    **********************************************************************
    """
    def get_action(self, state):
        """ Employ an adversarial search technique to choose an action
        available in the current state calls self.queue.put(ACTION) at least

        This method must call self.queue.put(ACTION) at least once, and may
        call it as many times as you want; the caller will be responsible
        for cutting off the function after the search time limit has expired.

        See RandomPlayer and GreedyPlayer in sample_players for more examples.

        **********************************************************************
        NOTE: 
        - The caller is responsible for cutting off search, so calling
          get_action() from your own code will create an infinite loop!
          Refer to (and use!) the Isolation.play() function to run games.
        **********************************************************************
        """
        TIME_LIMIT = 150 # milliseconds

        ALGO = "MCT"
        # filename = "mct.pickle" if ALGO=="MCT" else "minimax.pickle"

        # delete the following for performance reasons, takes time to write pickle file
        #------------------------------------------------------------
        # try: 
        #   with open(filename, "rb") as f:
        #     self.context = pickle.load(f)
        # except:
        #   self.context = defaultdict()
        #   self.context["info_dict"] = defaultdict()
        #   self.context.update({"game_num": 1})
        #   self.context.update({"iteration" : 1})
        #------------------------------------------------------------ 

        if state.terminal_test() or state.ply_count < 2:
          # print("Set iteration to 1")
          # num_iter = 1
          # game_num = self.context["game_num"] + 1
          # self.context["iteration"] = num_iter
          # self.context["game_num"] = game_num
          # self.context["info_dict"].update({str(game_num) + "_" + str(num_iter): 0})
          # with open(filename, "wb") as f:
          #   pickle.dump(self.context, f)
          
          self.queue.put(random.choice(state.actions()))
        
        else:
          # delete the following for performance reasons, takes time to write pickle file
          #------------------------------------------------------------
          # num_iter = self.context["iteration"] + 1
          #------------------------------------------------------------
          if ALGO == "MCT":
            mcts = MonteCarloTreeSearch(state)
            res = mcts.best_action(TIME_LIMIT)
            
            # # save the following information
            # list_visits = [child.n for child in mcts.root.children]
            # num_visits = sum(list_visits)
            # dict_info = {"num_visits": num_visits}
          else:
            minimaxAB = MinimaxAlphaBetaSearch(state, depth=6)
            res = minimaxAB.minimax_alphaBeta(TIME_LIMIT)
  
            # num_visits = minimaxAB.num_visits
            # dict_info = {"num_visits": num_visits,
            #               "depth": minimaxAB.depth}

          # # delete the following for performance reasons, takes time to write pickle file
          # #------------------------------------------------------------
          # self.context["iteration"] = num_iter
          # game_num = self.context["game_num"]
          # self.context["info_dict"].update({str(game_num) + "_" + str(num_iter): dict_info})
     
          # with open(filename, "wb") as f:
          #   pickle.dump(self.context, f)
          # #------------------------------------------------------------

          if res:
              self.queue.put(res)
          elif state.actions():
              self.queue.put(random.choice(state.actions()))
          else:
              self.queue.put(None)
