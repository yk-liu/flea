from flea.components import sync
from flea.components.population import *

from flea.operators.mutation import *
from flea.operators.niching import *
from flea.operators.crossover import *
from flea.operators.selection import *

from flea.analyzer.fitnesstracker import *

from flea.utilities.gui_io import *



print(dir(sync))
class Session:
    def __init__(self,gene_pool = [],population_size= 100):
        self.p = Population(size=population_size, gene_pool=gene_pool)
        sync.flea_population = self.p
        print(self.p.individuals[0].chromosome)

        mutation = Mutation(sync.flea_population)
        niching = Niching(sync.flea_population)
        crossover = Crossover(sync.flea_population)
        selection = Selection(sync.flea_population)

        self.mutate = mutation.simple_mass_random_mutate
        self.niche = niching.criterion_niche
        self.cross = crossover.simple_mass_crossover_ratio
        self.select = selection.ratio_select

        self.fitnessTracker = FitnessTracker()

    def run(self,n = 100):
        sync.flea_population = self.p
        for _ in range(n):
            self.mutate()
            self.select()
            self.niche()
            self.cross()

            sync.update_generation_number(sync.flea_population)
            self.fitnessTracker.store_best(sync.flea_population)
            self.fitnessTracker.store_mean(sync.flea_population)

        print(self.fitnessTracker.report_best())
        print(self.fitnessTracker.report_mean())





