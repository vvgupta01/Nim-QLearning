import random
from Agent import Agent


class ExpertAgent(Agent):

    def __init__(self):
        super(ExpertAgent, self).__init__()
        self.possible_moves = []

    def move(self, board, turn):
        if not ExpertAgent.is_near_end(board):
            self.update_moves(board)
        else:
            pile, one_piles = ExpertAgent.piles_near_end(board)
            if one_piles % 2 == 0:
                return Agent.remove_obj(board, pile, board[pile]-1)
            return Agent.remove_obj(board, pile, board[pile])

        if len(self.possible_moves) > 0:
            index = random.randint(0, len(self.possible_moves) - 1)
            pile = self.possible_moves[index][0]
            obj = self.possible_moves[index][1]
            self.possible_moves.clear()
            return Agent.remove_obj(board, pile, obj)
        return Agent.random_move(board)

    def update_moves(self, board):
        for pile in range(len(board)):
            for obj in range(1, board[pile] + 1):
                temp_board = board.copy()
                temp_board[pile] -= obj
                nim_sum = ExpertAgent.nim_sum(temp_board)
                if nim_sum == 0:
                    self.possible_moves.append([pile, obj])

    @staticmethod
    def nim_sum(board):
        nim_sum = 0
        for pile in board:
            nim_sum ^= pile
        return nim_sum

    @staticmethod
    def is_near_end(board):
        full_piles = 0
        for pile in board:
            if pile > 1:
                full_piles += 1
        return full_piles == 1

    @staticmethod
    def piles_near_end(board):
        pile, one_piles = 0, 0
        for i in range(len(board)):
            if board[i] == 1:
                one_piles += 1
            elif board[i] > 1:
                pile = i
        return pile, one_piles
