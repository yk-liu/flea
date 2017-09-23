from flea.components.population import *
from flea.operators.mutation import *
import heapq

from flea.components import sync
print(dir(sync))

gene_pool = [[12,44,5454],[4,6,7],[23,4,3,3]]

p = Population(10,gene_pool)

sync.flea_population = p
M = Mutation(sync.flea_population )
MM = M.simple_mass_random_mutate

print(len(p.individuals))

MM(mutate_ratio=0.1,mutate_site=2)
print(len(p.individuals))


print(len(p.individuals))