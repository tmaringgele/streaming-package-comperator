import numpy as np

def load_games():
    return np.genfromtxt('data/bc_game.csv', delimiter=',', dtype=None, encoding=None)