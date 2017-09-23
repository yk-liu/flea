# Documentation for List-based Evolutionary Algorithm

author : Yingkai Liu

updated : Aug.2017

status: still incomplete, even this documentation is incomplete

## 1. code overview
This code is written in python3 compatible with python2. Used packages only includes `easygui` `radom` `itertools` to utilize maximum compatibility. 

It has a GUI and you can also disable it with minimum modification.

This code is designed to perform evolutionary algorithm on a population whose gene are in the form of lists. The `fitness function` is an arbitrary user defined function. It can be as simple as `sum` or any other complicated function such as the `how similar of a graph A compared to B`.

This code features a relatively wide range of evolutionary operators. `mutate` `hybrid` `select` are three basics ones. To prevent pre-mature, there are two other functions `migrate` and `niche`. 

The whole package is included in a single class called population. you can add new functions to this class as well, such as `adapt` (which I am planning to add later) .

Also you might find that sometimes you get one more or one less choromosomes than you expected, that is because I used `int()` everything to make sure interger. I assume it won't be a big problem for a large population. This will be fixed in later releases.

## 2. functions and implementation

### 2.1  class attributes

```python
    def __init__(self,gene_set,gene_range,population_size):
        self.gene_set = gene_set
        self.gene_size = len(gene_set)
        self.gene_range = gene_range

        self.population_size = population_size

        self.chromosomes = self.initialize_chromosomes(self.population_size)

        self.generation_number = 0
```
### 2.2 functions

#### 2.2.1 `assign_fitness(self,gene)`
This is user defined function
#### 2.2.2 `initialize_chromosome(self)`
Use attributes and `assign_fitness` to generate a chromosome in the form of 

$$chromosome = [ [  gene[site]  ] , fitness ]$$

#### 2.2.3 `initialize_chromosomes(self,population_size)`
This function use `initialize_chromosome` to generate a list of chromosomes in the form of 

$$chromosomes = [ chromosome ]$$

#### 2.2.4 `roulette_fitness(self)`
This function will use fitness as a bias to choose a chromosome

#### 2.2.5 `mutate(chromosome, mutate_strength=1)`
mutate `mutate_strength` sites in the `chromosome`

#### 2.2.6 `migrate(self,immigration_size)`
same as initialize chromosomes
       
#### 2.2.7 `hybrid(father,mother)`
generate a child using genes randomly chosen from father and mother. If the site of gene are odd, then mother have one more contribution than father. Else choose half of `gene_site` randomly from father and mother

#### 2.2.8 `population_crossover(self,roulette=False,crossover_ratio=0.1)`

#### 2.2.9 `assign_simiarity(self,pair)`
This function takes in chromosomes and extract thier gene and then return the distance of genes as similarity, the distance is simply absulute difference.

**you can make it use euclidean distance**

The similairty is averaged normalized in range (0,1)
the code need to use `gene_range[site]` to normalize and `gene_size` to average

similarity = difference / gene_range  

the similarity is then averaged over all sites
#### 2.2.10 `niche(self, niche_ratio=0.0, niche_criterion=0.0)`
This function use `assign_similarity` and 



#### 2.2.11 `select(self, select_ratio=0.0, select_criterion=0.0)`

#### 2.2.12 `evolve(self, niche_ratio=0.1, niche_criterion=0.0)`



## 3.complex ideas
### 3.1 multiple hybrid
like hybrid using genes from 3 parents. This can be done but is of little use since generating a purmutation list of three parents are slow, and multiple parents is basically the same if you tune up the `crossover_ratio` and set `roulettel` = `True`

### 3.2 hybrid strictly according to fitness

### 3.3 make a method ranks the fitness / number each chromosome /...
later

## 4.acknowledgement 
special thanks to Kai Wu for initial discussions, Yifei Liu for brilliant ideas, Qiang Zhu and Xiangfeng Zhou for instruction. USPEX inspired this script
