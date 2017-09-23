from flea.components.population import *
from flea.operators.niching import *
import heapq

from flea.components import sync


gene_pool = [[12,44,5454],[4],[23,4,3,3]]

p = Population(10,gene_pool)
sync.flea_population = p

N = Niching(sync.flea_population)
NN = N.criterion_niche
NNN = N.ratio_niche

print(len(p.individuals))

NN(1)
print(len(p.individuals))
NNN(0.5)

print(len(p.individuals))