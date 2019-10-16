import random


class Agent:

    def __init__(self):
        self.losses = 0

    @staticmethod
    def move(board, turn):
        pass

    @staticmethod
    def random_pile(board):
        pile = random.randint(0, len(board)-1)
        while board[pile] == 0:
            pile = random.randint(0, len(board)-1)
        return pile

    @staticmethod
    def random_obj(board, pile):
        obj = random.randint(1, board[pile])
        return obj

    @staticmethod
    def is_board_empty(board):
        for pile in board:
            if pile > 0:
                return False
        return True

    @staticmethod
    def remove_obj(board, pile, obj):
        board[pile] -= obj
        move = 'REMOVED {} OBJECTS FROM PILE {}'.format(obj, pile + 1)
        return Agent.is_board_empty(board), move

    @staticmethod
    def random_move(board):
        pile = Agent.random_pile(board)
        obj = Agent.random_obj(board, pile)
        return Agent.remove_obj(board, pile, obj)

    def __str__(self):
        return self.__class__.__name__[0:-5]
