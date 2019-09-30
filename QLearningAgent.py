import os
import sys
import time
import pickle
import pandas as pd
from Agent import Agent


class QLearningAgent(Agent):
    REWARD = 1000
    MIN_REWARD, MAX_REWARD = REWARD + 1, -REWARD - 1

    def __init__(self):
        super(QLearningAgent, self).__init__()
        self.parameters = {'ALPHA': 0.0, 'GAMMA': 0.0, 'BOARD': [], 'EPISODES': 0, 'Q_VALUES': {}}
        self.results = pd.DataFrame()

    def load(self, agent_path):
        config_path = agent_path + '/agent_config.txt'
        with open(config_path, 'rb') as file:
            self.parameters = pickle.load(file)

        results_path = agent_path + '/test_results.csv'
        if os.path.exists(results_path):
            self.results = pd.read_csv(results_path)

    def save(self, agent_path):
        config_path = agent_path + '/agent_config.txt'
        with open(config_path, 'wb') as file:
            pickle.dump(self.parameters, file)

        results_path = agent_path + '/test_results.csv'
        self.results.to_csv(results_path, index=False)

        q_values_path = agent_path + '/q_values.txt'
        with open(q_values_path, 'w') as file:
            for key, value in self.parameters['Q_VALUES'].items():
                file.write('Q[{},{}] = {}\n'.format(key[:-2], key[-2:], value))

    def set_results(self, results):
        self.results = results

    def train(self, board, episodes, alpha, gamma):
        self.parameters['ALPHA'] = alpha
        self.parameters['GAMMA'] = gamma
        self.parameters['BOARD'] = board
        self.parameters['EPISODES'] = episodes
        self.parameters['Q_VALUES'].clear()

        print('\nTRAINING Q-LEARNING AGENT [ALPHA={}][GAMMA={}]'.format(self.parameters['ALPHA'],
                                                                        self.parameters['GAMMA']))
        start_time = time.time()
        for i in range(episodes):
            turn = 0
            game_board, game_over = board.copy(), False
            while not game_over:
                pile = Agent.random_pile(game_board)
                obj = Agent.random_obj(game_board, pile)

                self.update_q_value(game_board, turn, pile, obj)
                game_over, move = Agent.remove_obj(game_board, pile, obj)
                turn += 1
            progress = (i + 1) / episodes * 100
            sys.stdout.write('\r')
            sys.stdout.write('[%-20s] %d%%' % ('=' * int(progress / 5), int(progress)))
            sys.stdout.flush()
        end_time = time.time()
        total_time = round(end_time - start_time, 2)
        print('\nSUCCESSFULLY TRAINED AGENT IN {}s'.format(total_time))

    def move(self, board, turn):
        pile = Agent.random_pile(board)
        obj = Agent.random_obj(board, pile)
        min_value, max_value = QLearningAgent.MIN_REWARD, QLearningAgent.MAX_REWARD
        for p in range(len(board)):
            for o in range(1, board[p] + 1):
                temp_pair = QLearningAgent.get_pair(board, turn, p, o)
                if temp_pair in self.parameters['Q_VALUES']:
                    q_value = self.parameters['Q_VALUES'][temp_pair]
                    if (turn % 2 == 0 and q_value > max_value) or (turn % 2 == 1 and q_value < min_value):
                        min_value, max_value = q_value, q_value
                        pile, obj = p, o
        return Agent.remove_obj(board, pile, obj)

    @staticmethod
    def get_pair(board, turn, pile, obj):
        return QLearningAgent.get_state(board, turn) + QLearningAgent.get_action(pile, obj)

    @staticmethod
    def get_state(board, turn):
        state = str(turn % 2)
        for pile in board:
            state += str(pile)
        return state

    @staticmethod
    def get_action(pile, obj):
        return str(pile) + str(obj)

    @staticmethod
    def get_next_board(board, pile, obj):
        next_board = board.copy()
        next_board[pile] -= obj
        return next_board

    @staticmethod
    def get_reward(next_board, turn):
        reward = 0
        if Agent.is_board_empty(next_board):
            reward = QLearningAgent.REWARD
            if turn % 2 == 1:
                reward *= -1
        return reward

    def update_q_value(self, board, turn, pile, obj):
        pair = QLearningAgent.get_pair(board, turn, pile, obj)
        next_board = QLearningAgent.get_next_board(board, pile, obj)
        turn += 1
        reward = self.get_reward(next_board, turn)

        if pair not in self.parameters['Q_VALUES']:
            self.parameters['Q_VALUES'][pair] = 0.00
        min_value, max_value = self.get_min_max(turn, board, next_board)

        q_value = self.parameters['Q_VALUES'][pair]
        multiplier = max_value if turn % 2 == 0 else min_value
        new_value = q_value + self.parameters['ALPHA'] * (reward + self.parameters['GAMMA'] * multiplier - q_value)
        self.parameters['Q_VALUES'][pair] = new_value

    def get_min_max(self, turn, board, next_board):
        min_value, max_value = QLearningAgent.MIN_REWARD, QLearningAgent.MAX_REWARD
        for pile in range(len(board)):
            for obj in range(1, board[pile] + 1):
                temp_pair = QLearningAgent.get_pair(next_board, turn, pile, obj)
                if temp_pair in self.parameters['Q_VALUES']:
                    value = self.parameters['Q_VALUES'][temp_pair]
                    min_value = min(value, min_value)
                    max_value = max(value, max_value)
        min_value = 0 if min_value == QLearningAgent.MIN_REWARD else min_value
        max_value = 0 if max_value == QLearningAgent.MAX_REWARD else max_value
        return min_value, max_value

    def is_trained(self):
        return len(self.parameters['Q_VALUES']) > 0

    def get_name(self):
        if not self.is_trained():
            return 'NO TRAINED AGENT'
        else:
            params = {}
            for key, value in self.parameters.items():
                if key != 'Q_VALUES':
                    params[key] = value
            return str(params)

    def __str__(self):
        return super().__str__() + ' [{},{}]'.format(self.parameters['ALPHA'], self.parameters['GAMMA'])
