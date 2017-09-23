import random

from flea.components import sync
from flea.components.population import *
from flea.utilities.fitness_roulette import Fitness_roulette


class Crossover:
    def __init__(self, Population):
        self.individuals = Population.individuals
        self.gene_pool = Population.gene_pool
        self.utility = Fitness_roulette(Population)

    def _commit(self):
        sync.flea_population.individuals = self.individuals

    def _simple_2_hybrid(self, father, mother):
        """
        make *ONE* baby. use population_crossover to perform repoduce

        mother might play a more important role here s
        for odd number, mther will have one more gene pased on
        as in nature, mother will pass on most of cyto-gene
        :param father:
        :param mother:
        :return: a single child
        """
        chromosome_size = len(father.chromosome)
        from_father = random.sample(range(chromosome_size), chromosome_size // 2)
        child_chromosome = [father.chromosome[site] if site in from_father
                            else
                            mother.chromosome[site]
                            for site in range(chromosome_size) ]

        child = Individual()
        child.chromosome = child_chromosome
        return child

    def simple_mass_crossover_n(self,n=1):
        children = []
        for _ in range(n):
            father ,mother = self.utility.fitness_roulette_n(2)
            children.append(self._simple_2_hybrid(father,mother))

        self.individuals.extend(children)

        self._commit()



    def simple_mass_crossover_ratio(self,ratio = 0.1):
        """
        N of new baby = len(individuals)*ratio
        :param ratio:
        :return:
        """
        n = int(len(self.individuals)*ratio)
        self.simple_mass_crossover_n(n)

        self._commit()


