from flea.components.population import *
from flea.operators.selection import *
import heapq

from flea.components import sync


gene_pool = [[12,44,5454],[4],[23,4,3,3]]

p = Population(10,gene_pool)
sync.flea_population = p

# for i in p.individuals:
#     print(i.fitness,i.chromosome)
#
# print(p.individuals[0].fitness)
pp = p.individuals
# lambda x : x[i].fitness

# x = heapq.nsmallest(2, pp, key =lambda pp: pp.fitness)
x = map(pp.index, heapq.nlargest(2,pp,key=lambda pp: pp.fitness))
# print(list(x))


print('criterion')
sync.flea_population = p
select = Selection(p)
select.criterion_select(select_criterion=4000)
# print(p)
# print(p.individuals)
for i in p.individuals:
    print(i.fitness,i.chromosome)

# print("ratio")
# sync.flea_population = p
# select = Selection(p)
# select.ratio_select(select_ratio=0.5)
# # print(p)
# # print(p.individuals)
# for i in p.individuals:
#     print(i.fitness,i.chromosome)


