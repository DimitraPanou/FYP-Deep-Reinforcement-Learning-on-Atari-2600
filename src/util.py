import os
import glob
from pprint import pprint
from datetime import datetime
import numpy as np
from matplotlib import pyplot as plt


def get_supported_games():
    with open('../supported-games.txt', 'r') as f:
        games = f.read().strip().split('\n')

    return games


def save_results(path, data):
    ''' Save a set of metrics to numpy arrays specified by pathx, pathy '''

    try:
        data_loaded = np.load(path)
        data_loaded = np.append(data_loaded, data)

    except FileNotFoundError:
        if '.npy' not in path:
            print('Paths must include the .npy extension')
            raise FileNotFoundError
        else:
            data_loaded = data

    np.save(path, data_loaded)
    print('Saved {} at {}'.format(path, datetime.now()))


def print_results(game, mode):
    if game not in ['space_invaders', 'breakout', 'space_invaders_test', 'breakout_test']:
        print('Invalid game name: ', game)
        return

    if mode not in ['dqn', 'double', 'duel']:
        print('Invalid DL Mode: ', mode)
        return

    print('Average Score')
    pprint(np.load('./data/{1}/{0}_avgscore_{1}.npy'.format(game, mode)))
    print('-----------------------')
    print('Average Frames Survived')
    pprint(np.load('./data/{1}/{0}_avgframes_surv_{1}.npy'.format(game, mode)))
    print('-----------------------')
    print('Average Model Loss')
    print(np.load('./data/{1}/{0}_loss_{1}.npy'.format(game, mode)))


def plot_results(game, mode, feature):
    if feature not in ['avgscore', 'avgframes', 'loss']:
        print('Feature must be one of avgscore, avgframes, loss')
        return

    try:
        ydata = np.load('./data/{1}/{0}_{2}_{1}.npy'.format(game, mode, feature))
        xdata = [i + 1 for i in range(len(ydata))]
        plt.plot(xdata, ydata, 'r')
        plt.show()
    except FileNotFoundError:
        print('No {} data found to plot for {} {}'.format(feature, game, mode))
        raise KeyboardInterrupt


def record(agent, path):
    name = input('What should this recording be called? ')
    agent.ale.reset_game()
    try:
        agent.simulate_intelligent(evaluating=True)
        print('Compiling video using ffmpeg')
        run(['ffmpeg', '-r', '60', '-i', path + 'tmp/%06d.png', '-an', '-f', 'mov', '-c:v', 'libx264', path + name])
    except:
        print("There was an error recording")
        return

    print('Recording saved to {} at {}'.format(path, datetime.now()))
    print('Cleaning up tmp')
    files = glob.glob(path + 'tmp/*')
    for f in files:
        os.remove(f)
