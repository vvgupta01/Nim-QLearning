This program was created in IntelliJ PyCharm 2019.2.3 and compiled with Python 3.6.

### Overview & Summary
This program tests the effectiveness of varying paramaterized instances of a Q-learning algorithm against an expert algorithm in the game of Nim. 

#### Nim
Nim is a two-player game in which players take alternating turns removing objects from multiple piles. A player can remove any number of objects during their turn, but only from a single pile. In the misère variant of Nim, the losing condition is to remove the last object. The game of Nim is completely solved, meaning there exists an optimal strategy such that the second player to move can always win. 

#### Algorithm
Q-learning is a type of reinforcement learning in which the agent performs an optimal action based on the current state of the environment in order to maximize an arbitrary reward. To do so, an agent utilizes a Q-table in which each possible state-action pair is assigned a value, also known as a Q-value, which reflects the action's direct reward. <br><br>
The learning rate (alpha: 0-1) represents how quickly the algorithm learns (i.e. weight of new/updates values), while the discount factor (gamma: 0-1) represents how much the algorithm discounts future rewards (i.e. weight of future values). <br><br>
The Q-learning algorithm was trained with varying learning rate and discount factor pairs, with each parameter varying in value from 0-1 in 0.2 increments for a total of 36 distinct pairs. Each Q-learning instance was trained for 200,000 games against itself through self-play before playing 200,000 games against an expert algorithm. 

#### Q-Table
The final Q-table consists of 5920 values for a 4-row board with an initial board state of 1-3-5-7. <br>
Each Q-value is associated with a state-action pair as follows: <br>
1. The state of the board consists of the player turn (first/second player = 0/1 respectively) concatenated with the number of items in each   row to create a 5-tuple. <br>
2. The action consists of the row number (0-3) and the number of items removed from the row (max items per row: 1-3-5-7) <br>

Positive Q-values are correlated with better moves for the player that goes first while negative Q-values are correlated with better moves for the player that goes second (i.e. the optimal move for the first player and a given board state is the state-action pair with the highest Q-value). <br><br>

The program includes feature such as data analysis, visualization, and games between the user and agent. <br>
The full paper can be found in the report document. A sample agent with (alpha=1, gamma=1) is included in the agents folder.
