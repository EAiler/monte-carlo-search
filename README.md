# monte-carlo-search
Implementing Monte Carlo Search Technique on the isolation game   
[Monte Carlo Search (Wiki)](https://en.wikipedia.org/wiki/Monte_Carlo_tree_search)


## Background

### Isolation Game   
![Example game of isolation on a square board](viz.gif)

The framework for the algorithm is provided by the Udacity course of Artificial Intelligence. This version of Isolation gives each agent control over a single token that moves in L-shaped movements--like a knight in chess.
The source code (without the implementation of the MonteCarloPlayer.py) can be found on github:
```
$ git clone https://github.com/udacity/artificial-intelligence
```

**You can find more information (including implementation details) about the in the Isolation library readme [here](/isolation/README.md).**


## Run the code

- Navigate to your folder of choice
- Clone the project 
```
$ git clone https://github.com/EAiler/monte-carlo-search.git
$ cd monte-carlo-search
```
- To play a game using the MonteCarloPlayer use the following command:
```
$ python run_match.py
```
The code is run in Debug Mode, which shows the states of the game in the terminal. The user can follow the choices of the agent.

## Further Modifications that can be made to the code
Udacity leaves multiple choices open for further improving the code and the agent playing isolation:

- **Opening Book**
It is necessary to write own code to develop an opening book, but it is possible to pass the book to the agent by saving the files as "data.pickle" in the same folder as `my_players.py`. Using the [pickle](https://docs.python.org/3/library/pickle.html) module to serialize the object that should be saved. The pickled object will be accessible to the agent through the `self.data` attribute.

For example, the contents of dictionary `my_data` can be saved to disk in the following way:
```
import pickle
from isolation import Isolation
state = Isolation()
my_data = {state: 57}  # opening book always chooses the middle square on an open board
with open("data.pickle", 'wb') as f:
    pickle.dump(my_data, f)
```

- **Custom Heuristic**
In the file _my_players.py_ that was implemented, it is possible to add further heuristic functions and call them in the _score()_ function for the MinimaxAgent with Iterative Deepening. The alternative is to use one of the players implemented in the _sample_players.py_ and add a relevant score function there for computing heurisitics.



