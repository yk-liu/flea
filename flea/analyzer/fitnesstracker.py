from flea.components import sync
from flea.components.population import *
from flea.utilities.fitness_roulette import Fitness_roulette


class FitnessTracker:
    def __init__(self):
        self.mean_fitness = []
        self.best_fitness = []

    def store_best(self,Population):
        fitness_list = [individual.fitness for individual in Population.individuals]
        self.mean_fitness.append(max(fitness_list))

    def report_best(self):
        return self.best_fitness

    def store_mean(self,Population):
        fitness_list = [individual.fitness for individual in Population.individuals]
        self.mean_fitness.append(sum(fitness_list)/len(sync.flea_population.individuals))

    def report_mean(self):
        return self.mean_fitness