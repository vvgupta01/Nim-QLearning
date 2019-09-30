import os
import Utils
from QLearningAgent import QLearningAgent


def main():
    action, agent_path = '', ''
    episodes, board = 0, []
    q_learning = QLearningAgent()

    while action != 'Q':
        print('\nAGENT:', q_learning.get_name())
        print('LOAD AGENT[L] NEW AGENT[N] QUIT[Q]')

        action = input('ENTER ACTION: ').upper()
        if action == 'L':
            dirs = os.listdir('agents')
            if len(dirs) == 0:
                print('NO AGENTS FOUND')
            else:
                print()
                for i, agent_name in enumerate(dirs):
                    agent_path = 'agents/' + agent_name
                    temp_agent = QLearningAgent()
                    temp_agent.load(agent_path)
                    print('[{}]{}'.format(i + 1, temp_agent.get_name()))
                agent = Utils.get_variable('SELECT AGENT: ', 'INVALID AGENT', 1, len(dir()))
                agent_path = 'agents/agent{}'.format(agent)
                q_learning.load(agent_path)
                board, episodes = q_learning.parameters['BOARD'], q_learning.parameters['EPISODES']
        elif action == 'N':
            rows = Utils.get_variable('ROWS [1-10]: ', 'INVALID NUMBER OF ROWS', 1, 10)
            board = [i * 2 + 1 for i in range(rows)]
            print('BOARD =', board)

            episodes = Utils.get_variable('EPISODES [1-1000000]: ', 'INVALID NUMBER OF EPISODES', 1, 1000000)
            alpha = Utils.get_variable('LEARNING RATE [0-1]: ', 'INVALID LEARNING RATE', 0, 1)
            gamma = Utils.get_variable('DISCOUNT FACTOR [0-1]: ', 'INVALID DISCOUNT FACTOR', 0, 1)
            q_learning.train(board, episodes, alpha, gamma)
        elif action != 'Q':
            print('INVALID ACTION')

        while q_learning.is_trained():
            print('\nAGENT:', q_learning.get_name())
            if q_learning.results.empty:
                print('TEST AGENT[T] PLAY AGENT[P] QUIT[Q]')
            else:
                print('RETEST AGENT[T] RESULTS[R] PLAY AGENT[P] QUIT[Q]')

            action = input('ENTER ACTION: ').upper()
            if action == 'T':
                trials = Utils.get_variable('TRIALS [1-100]: ', 'INVALID NUMBER OF TRIALS', 1, 100)
                results = Utils.full_test(q_learning, board, episodes, trials)
                q_learning.set_results(results)
            elif action == 'R' and not q_learning.results.empty:
                Utils.display_results(q_learning)
            elif action == 'P':
                Utils.play(q_learning, board)
            elif action == 'Q':
                dirs = os.listdir('agents')
                if agent_path == '':
                    agent_path = 'agents/agent{}'.format(len(dirs) + 1)
                    os.mkdir(agent_path)
                q_learning.save(agent_path)
                print('SUCCESSFULLY SAVED AGENT')

                q_learning = QLearningAgent()
                action = ''
            else:
                print('INVALID ACTION')


if __name__ == '__main__':
    main()
