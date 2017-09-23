from flea.components import sync
import heapq


class Selection:
    def __init__(self, Population):
        self.individuals = Population.individuals
        self.gene_pool = Population.gene_pool

    def _commit(self):
        sync.flea_population.individuals = self.individuals

    def ratio_select(self, select_ratio=0.1, return_killed=False):
        kill_count = int(len(self.individuals) * select_ratio)

        kill_indices = list(map(self.individuals.index,
                                heapq.nsmallest(kill_count, self.individuals, key=lambda p: p.fitness)))
        # a complicated way to get n smallest items' indices in self.individuals
        kill_indices.sort(reverse=True)

        killed_population = []
        if kill_count != 0:
            for killed_index in kill_indices:
                killed_population.append(self.individuals.pop(killed_index))

        # self._commit()

        if return_killed == True:
            return killed_population

    def criterion_select(self, select_criterion=0., return_killed=False):

        population_temp = [Individual for Individual in self.individuals
                           if Individual.fitness >= select_criterion]


        if return_killed == True:
            killed_population = [Individual for Individual in self.individuals if Individual.fitness < select_criterion]
            return killed_population

        self.individuals = population_temp

        self._commit()


