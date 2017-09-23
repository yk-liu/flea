from flea.components.individual import *
import random
gene_pool = [[12,44,5454],[4],[23,4,3,3]]
# print(type(gene_pool) is list )
chromosome = [random.choice(gene_pool[site]) for site in range(len(gene_pool))]
print(chromosome)

i=Individual([[12,44,5454],[4],[23,4,3,3]])

print(i.fitness,i.chromosome)
i.chromosome = [12,32,23,23]

print(i.fitness,i.chromosome)

k = Individual()

print(k.fitness,k.chromosome)
k.chromosome = chromosome

print(k.fitness,k.chromosome)

