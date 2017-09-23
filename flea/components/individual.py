import random
from flea.components.fitness import *

class Individual:
    def __init__(self,gene_pool=[]):
        self.fitness_function = assign_fitness.simple_fitness
        self.gene_pool = gene_pool

        chromosome = [random.choice(gene_pool[site]) for site in range(len(gene_pool))]
        self.set_chromosome(chromosome)

        self.fitness = self.fitness_function(self.chromosome)

    def get_chromosome(self):
        return self._chromosome

    def set_chromosome(self, assigned_chromosome):
        self._chromosome = assigned_chromosome
        self.fitness = self.fitness_function(self._chromosome)

    chromosome = property(get_chromosome,set_chromosome)




