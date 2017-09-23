from flea.components.population import *
from flea.components import sync
import math, itertools,heapq


class Niching():
    def __init__(self, Population):
        self.individuals = Population.individuals
        self.gene_pool = Population.gene_pool

        self.similarity_function = self._simple_assign_simiarity
        self.similarity_list = self._generate_similarity_list()

    def _commit(self):
        sync.flea_population.individuals = self.individuals

    @staticmethod
    def _simple_assign_simiarity(object_Individual, subject_Individual):
        """
        can be user defined, can be complicated as fingerprint functions.

        :param pair: pair of individuals
        :return: the similarity based on the euclidean distance of their genes
        (NOT-normalized and NOT-averaged)
        """
        euclidean_distance = math.sqrt(sum([(x - y) ** 2
                                            for x, y in zip(object_Individual.chromosome,
                                            subject_Individual.chromosome)]))
        similarity = 1 / (euclidean_distance + 1)

        return similarity

    def _generate_similarity_list(self):

        similarity_list = [[index_a, index_b, self.similarity_function(a, b)]
                           for [index_a, a], [index_b, b]
                           in itertools.combinations(enumerate(self.individuals), 2)]

        return similarity_list

    def ratio_niche(self, niche_ratio=0.1, return_killed=False):
        """
        prevent premature, kill similar individuals to prevent clustering

        THIS IS NOT STABLE NICHE. every time the result is different since I chose n largest indexs
        but some of them are the same. need a bigger implementation.
        :param niche_ratio:if non zero, niche out a ratio of population
        :param return_killed
        :return: population, (killed)
        """
        kill_count = int(len(self.individuals) * niche_ratio)

        killed_population = []

        if kill_count != 0:
            kill_pairs = heapq.nlargest(kill_count,self.similarity_list,key= lambda x:x[-1])
            # find the nlargest
            kill_indices = [i[0] for i in kill_pairs]
            kill_indices = list(set(kill_indices))
            # remove same elements
            kill_indices.sort(reverse=True)
            # get indices from the list [index_a,index_b,sim_ab]

            for index in kill_indices:
                killed_population.append(self.individuals.pop(index))

        self._commit()

        if return_killed == True:
            return killed_population


    def criterion_niche(self,niche_criterion = 0., return_killed = False):
        survived_individuals = [self.individuals[index_a]
                           for [index_a,_,sim_ab] in self.similarity_list
                           if sim_ab <= niche_criterion]
        survived_individuals = list(set(survived_individuals))
        # remove same elements from list

        if return_killed == True:
            killed_population = [self.individuals[index_a]
                           for [index_a,_,sim_ab] in self.similarity_list
                           if sim_ab >= niche_criterion]
            self.individuals = survived_individuals
            self._commit()
            return killed_population
        else:
            self.individuals = survived_individuals
            self._commit()