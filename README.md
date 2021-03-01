#The Game of Hex

Hex is a two player strategy board game in which players attempt to
connect opposite sides of a hexagonal board. It was developed by the
mathematician John Nash. Even though the rules for Hex are extremely
simple, it has a deep strategic complexity comparable to that of
chess. I have used Python and the tkinter library to build a Hex GUI
and developed 3 different types of computer AIs:

1) A search-tree based minimax algorithm with alpha-beta pruning

2) A Monte-Carlo based approach 

3) An artificial neural network



## 1) Search Tree

The game tree is a standard approach in game theory. It models the game as a directed graph, where the nodes respresent states of the game and the edges represent moves. The artificial intelligence builds and searches this tree in order to find the best move. The biggest limitation of this approach is the exponentially growing computational power: Each node branches into n children, where n is the number of available moves. This is especially a challenge for Hex, due to its large branching factor. For a classic 11×11 Hex board the average number of legal moves is about 100 (compare with 40 for Chess).

For the Game Tree approach I have used a minimax algorithm, improved
with alpha-beta pruning. Alpha-beta pruning is an algorithm that
decreases the number of nodes which are evaluated by the search tree.
The second important component is the evaluation function, which
assigns to each leave-node/board a value representing how favorable
the board is for a given player. I have used a simple function that
uses a custom search algorithm to count the minimum number of pieces a
player needs to place in order to win. This number is calculated for
both players and the function outputs *f(d)* where *f*
is a linear function and *d* the difference of both numbers.
The AI uses a tree-depth of 4. While this is not enough for the AI to
beat an average human player, anything deeper than that results in
uncomfortable long computation times.


Further improvements that can be made for this approach:
- Use heuristics to order the available moves: alpha-beta pruning works better if "good" moves are evaluated first, since this leads to more alpha-/beta-cutoffs. Very "bad" moves can even by excluded from the tree to reduce the branching factor. 
- The evaluation function is too simple to account for the complexity of the game and can be improved with additional heuristic methods.



## 2) Monte Carlo


  The Monte-Carlo method uses a randomized approach to avoid the need
  for massive game-trees. For each available move, the AI plays
  *n* number of games to the end and keeps track of the ratio of
  games won. It then picks the move that had the highest win-ratio. This
  appraoch proved superior to the game tree: With *n=1000* , the
  AI plays on a 11x11 comparable to a beginner human player, but it
  takes around 30 seconds to make a move in the early game.
  

  Further Improvements for this approach:
  - Confidence Intervals:
  Currently the AI iterates over all possible moves and keeps track of
  the current best moves and its win-ratio. For each subsequent move
  *n=1000* games are played to finish. However, after playing a
  few hundred games, we can construct a confidence interval for the
  win-ratio of the current move. If there is a 99% chance that the final
  ratio will be below the current maximum win-ratio, the remaining few
  hundred games don't have to be played and we can jump to the next move
  early.


## 3) Artificial Neural Network

Recent breakthroughs from DeepMind's AlphaZero Go, showed how
effective reinforcement learning can be for strategic board games.
AlphaGo Zero was trained by playing against itself, with no prior
knowledge about the rules of Go. Within just a few days, it was good
enough to beat top human players. In comparison, it's predecessor
AlphaGo took months of training and large amounts of data to
accomplish similar results. This showed a clear superiority of
reinforcement learning, which is not limited by the constraints of
human knowledge. 

My goal is to use reinforcement learning to
train a neural network to play Hex. However, this approach is very
challenging to implement. The number of available moves and positions
is very high in Hex and the reward signal (game won/lost) only occurs
at the end of the game, so the signal has to be backpropagated a large
number of steps. Similar to AlphaGo, I will try to overcome these
challenges with convolutional neural networks and initial supervised
learning. However, I am currently still working on a deeper
understanding of the mathematical methods involved.


As an alternative for now, I have used a classic artificial neural
network that requires data to be trained. Since the MC approach plays
very well for high numbers of simulated games, the move it makes for a
given board can be used as an approximation for the "ideal" move.
Based on this, I have generated datasets by letting two Monte-Carlo
AIs play against each other. The resulting dataset consists of a board
and the resulting "optimal" next move for the current player. To
further increase the training data, I have played a few hundred game
against myself. Furthermore, I am working on a algorithm that
automatically generates boards in advanced positions, where only one
or two pieces have to be placed in order to win, or where a winning
bridge exists.

To build and train the ANN I have used the tensorflow and keras
libraries. Currently, I use a sequential model with 2 hidden layers
and 81 neurons each. The accuracy on the training-data is around 1-2%
and the AI plays significantly worse than the first two approaches.
However, I am currently still generating more training data and trying
to improve the architecture of the neural network to improve the
results.
