import sys
import time
import pandas as pd
import matplotlib.pyplot as plt

from Agent import Agent
from ExpertAgent import ExpertAgent
from RandomAgent import RandomAgent


def full_test(q_learning, board, episodes, trials):
    expert1, expert2 = ExpertAgent(), ExpertAgent()
    random = RandomAgent()

    pos_control = test_agents(expert1, expert2, board, episodes, trials)
    neg_control = test_agents(expert1, random, board, episodes, trials)
    test = test_agents(expert1, q_learning, board, episodes, trials)
    results = pd.concat([pos_control, neg_control, test])
    return results


def play(agent, board):
    games, new_game = 0, True
    agent.losses = 0
    while new_game:
        games += 1
        turn = games % 2
        game_board, empty_board = board.copy(), False
        while not empty_board:
            print()
            print(game_board)
            if turn % 2 == 0:
                empty_board, move = agent.move(game_board, turn)
                print('AGENT ' + move)
                if empty_board:
                    agent.losses += 1
                    print('\nUSER WINS')
            else:
                piles = [pile for pile in range(1, len(game_board) + 1) if game_board[pile - 1] > 0]
                pile = -1
                while pile == -1:
                    try:
                        pile = int(input('SELECT PILE {}: '.format(piles)))
                        if pile not in piles:
                            pile = -1
                            raise ValueError
                    except ValueError:
                        print('INVALID PILE')

                prompt = 'SELECT NUMBER OF OBJECTS [1'
                prompt += '-{}]: '.format(game_board[pile - 1]) if game_board[pile - 1] > 1 else ']: '
                obj = get_variable(prompt, 'INVALID NUMBER OF OBJECTS', 1, game_board[pile - 1])
                empty_board, move = Agent.remove_obj(game_board, pile - 1, obj)
                if empty_board:
                    print('\nAGENT WINS')
            turn += 1
        action = input('NEW GAME? (Y/N): ').upper()
        new_game = action == 'Y'


def test_agents(agent1, agent2, board, episodes, trials):
    print('\nSIMULATING {} GAMES [{}][{}]'.format(episodes, agent1, agent2))
    results = {'TRIAL': list(range(1, trials + 1)), 'AGENT 1': [], 'AGENT 2': [],
               'WINS 1': [], 'WINS 2': [], 'TIME': []}
    for i in range(trials):
        start_time = time.time()
        agent1.losses, agent2.losses = 0, 0
        for j in range(episodes):
            turn, first = 0, j % 2
            game_board, empty_board = board.copy(), False
            while not empty_board:
                agent = agent1 if turn % 2 == first % 2 else agent2
                empty_board, move = agent.move(game_board, turn)
                if empty_board:
                    agent.losses += 1
                turn += 1

            progress = (j + 1) / episodes * 100
            sys.stdout.write('\r')
            sys.stdout.write('%s [%-20s] %d%%' % ('TRIAL: {}/{}'.format(i + 1, trials),
                                                  '=' * int(progress / 5), int(progress)))
            sys.stdout.flush()
        end_time = time.time()
        total_time = round(end_time - start_time, 2)
        results['AGENT 1'].append(str(agent1))
        results['AGENT 2'].append(str(agent2))
        results['WINS 1'].append(episodes - agent1.losses)
        results['WINS 2'].append(episodes - agent2.losses)
        results['TIME'].append(total_time)
    print('\nTOTAL TIME: {}s'.format(sum(results['TIME'])))
    print('AVG WINS:\t[{}]: {}\t[{}]: {}'.format(agent1, sum(results['WINS 1']) / trials,
                                                 agent2, sum(results['WINS 2']) / trials))
    df = pd.DataFrame(results)
    return df


def display_results(q_learning):
    print()
    print(q_learning.results)

    fig, ax = plt.subplots()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    colors = ['b', 'r', 'g']

    x = q_learning.results['AGENT 2'].unique()
    for i, agent in enumerate(x):
        agent_results = q_learning.results[q_learning.results['AGENT 2'] == agent]['WINS 2'] / \
                        q_learning.parameters['EPISODES'] * 100
        mean, error = round(agent_results.mean(), 3), round(agent_results.std(ddof=0), 3)
        plt.bar(agent, mean, yerr=error, color=colors[i], label=agent)

    plt.ylim(0, 60)
    for bar in ax.patches:
        ax.annotate('{}%'.format(bar.get_height()), (bar.get_x() + bar.get_width() / 2, bar.get_height() + 1),
                    ha='center', va='bottom')

    plt.title('AGENT TYPE VS AVG WINS IN NIM ({}, N={})'.format(q_learning.parameters['BOARD'],
                                                                q_learning.parameters['EPISODES']), fontsize=10,
              weight='bold')
    plt.xlabel('AGENT TYPE', fontsize=10)
    plt.ylabel('AVG PERCENTAGE OF WINS (%)', fontsize=10)
    plt.legend(loc='lower left', fontsize=8)
    plt.show()


def get_variable(prompt, error, low_bound, high_bound):
    while True:
        try:
            var = int(input(prompt))
            if var < low_bound or var > high_bound:
                raise ValueError
            return var
        except ValueError:
            print(error)
