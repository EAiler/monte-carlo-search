


def score(state):
    """ this will be a heurisitic function later on """
    return(pos_moves(state))

def pos_moves(state):
    """ return number of possible moves """
    return(len(state.actions()))

def minimax_alphaBeta(state, depth):
    """ Return the move along a branch of the game tree that
    has the best possible value.  A move is a pair of coordinates
    in (column, row) order corresponding to a legal move for
    the searching player.
    
    You can ignore the special case of calling this function
    from a terminal state.
    """
    alpha = float("-inf")
    beta = float("inf")
    best_score = float("-inf")
    best_move = None
    for a in state.actions():
        v = min_value_alphaBeta(state.result(a), depth - 1, alpha, beta)
        if v > best_score:   
            best_score = v
            best_move = a
    return best_move

def min_value_alphaBeta(state, depth, alpha, beta):
    if state.terminal_test():
        return state.utility(0)
    if depth <= 0:
        return score(state)

    v = float("inf")
    for a in state.actions():
        print(beta)
        v = min(max_value_alphaBeta(state.result(a), depth - 1, alpha, beta))
        if v <= alpha:
            return v
        beta = min(beta, v)
    return v

def max_value_alphaBeta(state, depth, alpha, beta):
    if state.terminal_test(): 
        return state.utility(0)
    if depth <= 0:
        return score(state)
    
    v = float("-inf")
    for a in state.actions():
        print(alpha)
        v = max(v, min_value_alphaBeta(state.result(a), depth - 1, alpha, beta))
        if v >= beta:
            return v
        alpha = max(alpha, v)
    return v

def minimax_decision(state, depth):
      """ Return the move along a branch of the game tree that
      has the best possible value.  A move is a pair of coordinates
      in (column, row) order corresponding to a legal move for
      the searching player.
      
      You can ignore the special case of calling this function
      from a terminal state.
      """

      best_score = float("-inf")
      best_move = None
      for a in state.actions():
        v = min_value(state.result(a), depth - 1)
        if v > best_score:
          best_score = v
          best_move = a
      return best_move

def min_value(state, depth):
    """ Return the value for a win (+1) if the game is over,
    otherwise return the minimum value over all legal child
    nodes.
    """

    if state.terminal_test():
        return state.utility(0)
    if depth <= 0:
        return score(state)

    v = float("inf")
    for a in state.actions():
        v = min(max_value(state.result(a), depth - 1))
    
    return v

def max_value(state, depth, alpha, beta):
    """ Return the value for a loss (-1) if the game is over,
    otherwise return the maximum value over all legal child
    nodes."""
    if state.terminal_test(): 
        return state.utility(0)
    if depth <= 0:
        return score(state)
    
    v = float("-inf")
    for a in state.actions():
        v = max(v, min_value(state.result(a), depth - 1))
    
    return v
