from Agent import Agent


class RandomAgent(Agent):

    def __init__(self):
        super(RandomAgent, self).__init__()

    def move(self, board, turn):
        return Agent.random_move(board)

