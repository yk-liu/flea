from flea.components.population import *
from flea.components import sync

class Mutation:
    def __init__(self, Population):
        self.individuals = Population.individuals
        self.gene_pool = Population.gene_pool

    def _commit(self):
        sync.flea_population.individuals = self.individuals


    def simple_single_mutate(self, individual, n_mutate_sites=1):
        """
        mutate a individual and automatically get fitness

        here I used alternate to make sure mutated gene is different
        here I used a new gramma:  a=b if conditionb else c
        it equals to if conditionb : a=b else: a=c
        :param individual: input
        :param mutate_strength: number of gene-sites mutated
        :return: mutated individual *NOT chromosome, included fitness*
        """
        chromosome_length = len(individual.chromosome)
        chromosome = individual.chromosome

        print(chromosome,chromosome_length,len(range(chromosome_length)),n_mutate_sites)

        mutate_site = random.sample(range(chromosome_length), n_mutate_sites)

        for site in mutate_site:
            new_gene, alternate = random.sample(self.gene_pool[site], 2)
            chromosome[site] = new_gene if new_gene != chromosome[site] else alternate

        mutated_individual =  Individual()
        mutated_individual.chromosome = chromosome
        return mutated_individual

    def simple_mass_random_mutate(self,mutate_ratio = 0.1,mutate_site = 1):
        mutate_number = int(len(self.individuals)*mutate_ratio)
        mutated_indices = random.choices(range(len(self.individuals)),k=mutate_number)
        for index in mutated_indices:
            self.individuals[index] = self.simple_single_mutate(self.individuals[index],mutate_site)

        self._commit()


    def simple_mass_baised_mutate(self):
        raise NotImplementedError

    def user_defined_mutate(self):
        raise NotImplementedError
        pass