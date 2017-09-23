from flea.components.individual import *


class Population:
    def __init__(self,size,gene_pool):
        self.size = size
        self.gene_pool = gene_pool
        individuals = [Individual(self.gene_pool) for i in range(self.size)]
        self.set_individuals(individuals)

        self.generation_number = 0

    def get_individuals(self):
        return self._individuals

    def set_individuals(self,assigned_individuals):
        self._individuals = assigned_individuals
        self.size = len(assigned_individuals)

    individuals = property(get_individuals,set_individuals)

