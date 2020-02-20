import numpy as np
from isolation import Isolation
import random
from copy import deepcopy
import datetime
import math
from collections import defaultdict



class Node:
    def __init__(self, state, link=None, parent=None):
        self.state = state
        self.parent = parent
        self.children = []
        self._number_of_visits = 0 # there are no visits in the beginning
        self._results = {0: 0, 1:0} # set a default dictionary
        self._not_visited_actions = self.state.actions()
        self.link = link #link to the action that resulted in the move from parent to children


    @property
    def q(self):
        wins=self._results[1-self.state.player()]
        loses = self._results[self.state.player()]
        return wins - loses
    
    @property
    def n(self):
        return self._number_of_visits


    def is_fully_expanded(self):
        """ check if the length of unvisited nodes is empty """
        return(len(self._not_visited_actions)==0)
    
    def is_terminal_node(self):
        return self.state.terminal_test()

    def max_ucb_child(self, C_PARAM=0.5):
        choices_weights = [(c.q / (c.n)) + C_PARAM * math.sqrt(2*math.log(self.n) / (c.n)) \
                           for c in self.children]
        #return self.children[np.argmax(choices_weights)]
        return self.children[choices_weights.index(max(choices_weights))]

    def max_q_child(self):
        choices_weights = [c.q for c in self.children]
        return self.children[choices_weights.index(max(choices_weights))]

    def rollout_policy(self, pos_moves):
        return random.choice(pos_moves)

    def expand(self):
        """ check which actions can be expanded or not """
        # select one action
        some_action = random.choice(self._not_visited_actions)
        self._not_visited_actions.remove(some_action)
        next_state = self.state.result(some_action)

        child_node = Node(next_state, link=some_action, parent=self)

        self.children.append(child_node)

        return child_node
    
    def rollout(self, player_id):
        """ roll out the selected node  """
        current_rollout_state = self.state
        while not current_rollout_state.terminal_test():
            current_rollout_state = current_rollout_state.result(
                self.rollout_policy(current_rollout_state.actions()))
           
        if current_rollout_state.utility(player_id)==float('inf'):   # Utility with respect to the player of the parent state
            return 1.
        elif current_rollout_state.utility(player_id)==float('-inf'):    # Utility with respect to the player of the parent state
            return -1.
        else:
            return 0

    def backprogagate(self, reward, player_id):
        self._number_of_visits += 1
        # self.n += 1
        #self.q += reward
        self._results[player_id] += reward
        self._results[1-player_id] -= reward
        #reward = -reward # invert the reward as it is the opposite in the above move
        # backpropagte until root node is reached
        if self.parent:
            self.parent.backprogagate(reward, player_id)


class MonteCarloTreeSearch:
    def __init__(self, state_initial):
        #self.game = isolation_state
        self.root = Node(state_initial)
        self.player_id = self.root.state.player()
        self.node_number = 1
    
    def best_action(self, TIME_LIMIT):
        """ return best action based on algorithm evaluation """
        # guarantee that the search time is limited to some amount
        #for _ in range(iter_max): 

        time_out = TIME_LIMIT
        while time_out > 15:
            start = datetime.datetime.now()
            v = self.tree_policy()
            reward = v.rollout(self.player_id)
            v.backprogagate(reward, self.player_id)
            end = datetime.datetime.now()
            time_out -= (end-start).total_seconds()*1000
            time_out = math.floor(time_out)

        res_node = self.root.max_ucb_child(C_PARAM=0.5)
        # get the action that leads to the best child
        res_act = res_node.link

        return res_act


    def tree_policy(self):
        """ tree policy decides which node will be selected """
        #while not self.game.terminal_test():
        current_node = self.root
        while not current_node.is_terminal_node():
            if not current_node.is_fully_expanded():
                new_node = current_node.expand()
                # count the number of nodes visited
                self.node_number += 1      
                return new_node
            else:
                current_node = current_node.max_ucb_child(C_PARAM=0.5)
        return current_node
