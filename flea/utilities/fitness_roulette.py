from flea.components import sync
from flea.components.population import *
import heapq


class Fitness_roulette:
    def __init__(self, Population):
        self.individuals = Population.individuals
        self.gene_pool = Population.gene_pool

    def _commit(self):
        sync.flea_population.individuals = self.individuals

    def fitness_roulette_single(self):
        """
        'roll a roulette, the ball will randomly end up in a pocket, showing the selected result'
        to put it simply, it use fitness as a bias to randomly draw individual
        I am pround to say that this fitness need not to be normalized at all. the implementation is pretty easy.
        read the code and you'll know
        :return: return the individual selected
        """

        fitness_list = [Individual.fitness for Individual in self.individuals]

        roulette_ball = random.uniform(0, sum(fitness_list))
        roulette_result = -1
        roulette_pocket = 0.0

        for index, roulettee in enumerate(fitness_list):
            roulette_pocket += roulettee
            if roulette_ball <= roulette_pocket:
                roulette_result = index
                break

        return self.individuals[roulette_result]

    def fitness_roulette_n(self,n=1):
        lucky_dogs = [self.fitness_roulette_single() for _ in range(n)]
        return lucky_dogs

    def fitness_nlargest(self,n = 1):
        indices = list(map(self.individuals.index,
                                heapq.nlargest(n, self.individuals, key=lambda p: p.fitness)))
        return indices

    def fitness_max(self):
        return self.fitness_nlargest(1)


