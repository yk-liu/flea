from flea.components.population import *
import heapq
gene_pool = [[12,44,5454],[4],[23,4,3,3]]

p = Population(3,gene_pool)

for i in p.individuals:
    print(i.fitness,i.chromosome)

print(p.individuals[0].fitness)
pp = p.individuals
# lambda x : x[i].fitness

# x = heapq.nsmallest(2, pp, key =lambda pp: pp.fitness)
x = map(pp.index, heapq.nlargest(2,pp,key=lambda pp: pp.fitness))
print(list(x))

# for i in x:
#     print(i.fitness,i.chromosome)