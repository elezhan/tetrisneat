from __future__ import print_function
from math import sqrt
from random import randint
from neat import nn, population, statistics
import os
import curses
import kivytetris
import numpy as np

def eval_fitness(genomes):
    for g in genomes:
        net = nn.create_feed_forward_phenotype(g)
        score = play_game(net)
        #print ("Score, turns", score, turns)
        g.fitness = score 

def play_game(net):
    """
    Simulates game with net's outputs for controls
    
    Args:
        net: Neural Net that inputs can be thrown to to get an output
    Returns:
        int: Score earned
    """

    game = kivytetris.GameHandler()

    keep_playing = True
    score = 0
    while keep_playing:
        inputs = game.get_neural_net_inputs()

        #output = int(net.serial_activate(inputs)[0] * 4.0)
        output = np.argmax(np.array(net.serial_activate(inputs)))

        if output == 0:
            game.move_right()
        if output == 1:
            game.rotate_current_piece()
        if output == 2:
            game.move_left()
        else:
            game.drop_piece()

        keep_playing = game.keep_playing()

    score = game.get_score()
    return score

local_dir = os.path.dirname(__file__)
config_path = os.path.join(local_dir, 'tetrisConfig')
pop = population.Population(config_path)
pop.run(eval_fitness, 1000)

winner = pop.statistics.best_genome()
winner_net = nn.create_feed_forward_phenotype(winner)
print('\nBest genome:\n{!s}'.format(winner))



