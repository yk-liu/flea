from flea.components.population import *
from flea.operators.crossover import *
import heapq

from flea.components import sync


gene_pool = [[12,44,5454],[4],[23,4,3,3]]

p = Population(10,gene_pool)
sync.flea_population = p

C = Crossover(sync.flea_population)
CC = C.simple_mass_crossover_ratio
CCC = C.simple_mass_crossover_n
print(len(p.individuals))
CC(1)
print(len(p.individuals))
CCC(1)

print(len(p.individuals))