import itertools
import random
import easygui

import numpy as np
import pylab as pl
from matplotlib import cm


class population:
    """
    A population has the following properties:

    Attributes:
        gene_set: A list representing the genes
        gene_size: The number of gene-sites in the list (gene_set)
        gene_range: The upper-lower value of each gene-site, this is only for number strings
        population_size: the number of individuals
        individuals: A list of individuals
        generation_number: useful for identifying times of evolution

    Methods:
        __init__: initialize the basic info about the population
        assign_fitness: user defined function. the fitnesss can be any number. the bigger the better
        initialize_individual:
        and others (fill in later)

    """

    def __init__(self, gene_set, gene_range, population_size):
        """
        :param gene_set:
        :param gene_range:
        :param population_size:
        """
        self.gene_set = gene_set
        self.gene_size = len(gene_set)
        self.gene_range = gene_range

        self.population_size = population_size

        self.individuals = self.initialize_individuals()

        self.generation_number = 0

    def assign_fitness(self, chromosome):
        """
        :param chromosome:
        :return: user defined fitness, bigger better
        """
        return sum(chromosome)

    def initialize_individual(self):
        """
        :return: individual: [gene_list,fitness]
        """
        chromosome = []
        for site in range(self.gene_size):
            chromosome.append(random.choice(self.gene_set[site]))

        fitness = self.assign_fitness(chromosome)

        individual = [chromosome, fitness]

        return individual

    def initialize_individuals(self):
        """
        :param size:
        :return: len(individuals) = size
        """
        self.individuals = []
        for i in range(self.population_size):
            self.individuals.append(self.initialize_individual())
        return self.individuals

    def roulette_fitness(self):
        """
        'roll a roulette, the ball will randomly end up in a pocket, showing the selected result'
        to put it simply, it use fitness as a bias to randomly draw individual
        I am pround to say that this fitness need not to be normalized at all. the implementation is pretty easy.
        read the code and you'll know
        :return: return the individual selected
        """

        fitness_list = [individual[1] for individual in self.individuals]

        roulette_ball = random.uniform(0, sum(fitness_list))
        roulette_result = -1
        roulette_pocket = 0.0

        for index, roulettee in enumerate(fitness_list):
            roulette_pocket += roulettee
            if roulette_ball <= roulette_pocket:
                roulette_result = index

        return self.individuals[roulette_result]

    def mutate(self, individual, mutate_strength=1):
        """
        mutate a individual and automatically get fitness

        here I used alternate to make sure mutated gene is different
        here I used a new gramma:  a=b if conditionb else c
        it equals to if conditionb : a=b else: a=c
        :param individual: input
        :param mutate_strength: number of gene-sites mutated
        :return: mutated individual *NOT chromosome, included fitness*
        """
        chromosome = individual[0]
        mutate_site = random.sample(range(self.gene_size), mutate_strength)

        for site in mutate_site:
            new_gene, alternate = random.sample(self.gene_set[site], 2)
            chromosome[site] = new_gene if new_gene != chromosome[site] else alternate

        mutated_individual = [chromosome, self.assign_fitness(chromosome)]
        return mutated_individual

    def migrate(self, immigration_size=2):
        """
        basically the same with initialze, but you cana control the size
        :param immigration_size:
        :return: added self.individuals (to the tail)
        """
        for i in range(int(immigration_size)):
            # print 'x', type(self.individuals),type(x)
            # print type(x),x
            self.individuals.append(self.initialize_individual())

        return self.individuals

    def hybrid(self, father, mother):
        """
        make *one* baby. use population_crossover to perform repoduce

        mother might play a more important role here s
        for odd number, mther will have one more gene pased on
        as in nature, mother will pass on most of cyto-gene
        :param father:
        :param mother:
        :return: a single child
        """
        father_gene = father[0]
        mother_gene = mother[0]
        individual_size = len(father_gene)
        from_father = random.sample(range(individual_size), int(individual_size / 2))
        child_gene = []
        child = []
        for site in range(self.gene_size):
            if site in from_father:
                child_gene.append(father_gene[site])
            else:
                child_gene.append(mother_gene[site])
        child.append(child_gene)
        child.append(self.assign_fitness(child_gene))
        return child

    def population_crossover(self, roulette=False, crossover_ratio=0.1):
        """
        based on hybrid. reproduce babies according to crossover_ratio

        :param roulette: if True: the fittest parents are selected (only *fitness-biased* randomly) (still randomly)\
        if False: all parents are selected randomly
        :param crossover_ratio:
        :return: added self.individuals (to the tail)
        """
        hybird_list = []
        offspring_number = int(len(self.individuals) * crossover_ratio)

        if roulette == True:
            for i in range(offspring_number):
                father = self.roulette_fitness()
                mother = self.roulette_fitness()

                count = 5
                while father == mother:
                    mother = self.roulette_fitness()
                    count -= 1
                    if count == 0:
                        print('warning : father and mother kept being the same in roulette')
                        break

                hybird_list.append([father, mother])
        else:
            # random hybrid
            hybird_list = list(itertools.permutations(self.individuals, 2))
            hybird_list = random.sample(hybird_list, offspring_number)

        for pair in hybird_list:
            self.individuals.append(self.hybrid(pair[0], pair[1]))

        return self.individuals

    def assign_simiarity(self, pair):
        """
        can be user defined, can be complicated as fingerprint functions.

        :param pair: pair of individuals
        :return: the similarity based on the euclidean distance of their genes (normalized and averaged)
        """

        object = pair[0]
        subject = pair[1]

        object_gene = object[0]
        subject_gene = subject[0]

        normalized_diversity = 0.0
        similarity = 0.0

        for site in range(self.gene_size):
            normalized_diversity += ((object_gene[site] - subject_gene[site]) / self.gene_range[site]) ** 2
            similarity += 1.0 - normalized_diversity

        similarity = similarity / self.gene_size

        return similarity

    def niche(self, niche_ratio=0.0, niche_criterion=0.0):
        """
        prevent premature, kill similar individuals to prevent clustering
        :param niche_ratio:if non zero, niche out a ratio of population
        :param niche_criterion: if non zero niche out population similarity higher than criterion
        :return: population, killed
        """
        assert niche_ratio * niche_criterion == 0 and niche_ratio ** 2 + niche_criterion ** 2 != 0
        # one of them is non-zero and the other zero

        killed_index = []
        killed = 0

        pair_list = list(itertools.permutations(enumerate(self.individuals), 2))
        numbered_similarity_list = []

        for numbered_pair in pair_list:
            # numbered_pair = ((index,[chromosome,fitness]),(index,[chromosome,fitness]))
            # items:             00    010              10    110
            index_a = numbered_pair[0][0]
            individual_a = numbered_pair[0][1]

            index_b = numbered_pair[1][0]
            individual_b = numbered_pair[1][1]

            similarity_ab = self.assign_simiarity((individual_a, individual_b))

            numbered_similarity_list.append([index_a, index_b, similarity_ab])

        numbered_similarity_list.sort(key=lambda x: x[2], reverse=True)

        if niche_ratio != 0:
            kill_count = int(len(self.individuals) * niche_ratio)

            while kill_count:
                pair = numbered_similarity_list.pop(0)  # pair = [indexa,indeb,similarityab]
                killed_index.append(pair[1])
                kill_count -= 1

        if niche_criterion != 0:
            for pair in numbered_similarity_list:  # pair = [indexa,indeb,similarityab]
                if pair[2] > niche_criterion:
                    killed_index.append(pair[1])

        killed_index.sort(reverse=True)

        for unfit in killed_index:
            del self.individuals[unfit]
            killed += 1

        return self.individuals, killed

    def select(self, select_ratio=0.0, select_criterion=0.0):
        """
        basic EA operator
        :param select_ratio: if non zero, kill out a ratio of population
        :param select_criterion: if non zero, kill out population similarity lower than criterion
        :return:
        """
        assert select_ratio * select_criterion == 0 and select_ratio ** 2 + select_criterion ** 2 != 0
        # one of them is non-zero and the other zero

        killed_index = []
        killed = 0

        if select_ratio != 0:
            kill_count = int(len(self.individuals) * select_ratio)

            # enumerate(self.individuals)=(index,individual)=(index,[chromosome,fitness])
            rank_fitness = sorted(enumerate(self.individuals), key=lambda list: list[1][1])

            while kill_count:
                target = rank_fitness.pop(0)
                killed_index.append(target[0])
                kill_count -= 1

        if select_criterion != 0:
            for index, individual in enumerate(self.individuals):
                if individual[1] < select_criterion:
                    killed_index.append(index)

        killed_index.sort(reverse=True)

        for unfit in killed_index:
            del self.individuals[unfit]
            killed += 1

        return self.individuals, killed

    def evolve(self, niche_ratio=0.1, niche_criterion=0.0,
               immigration_size=2,
               roulette=False, crossover_ratio=0.2,
               select_ratio=0.1, select_criterion=0.0):
        """
        toy model of evolution
        :param niche_ratio:
        :param niche_criterion:
        :param immigration_size:
        :param roulette:
        :param crossover_ratio:
        :param select_ratio:
        :param select_criterion:
        :return:
        """

        self.individuals, killed = self.niche(niche_criterion=niche_criterion, niche_ratio=niche_ratio)

        self.individuals = self.migrate(immigration_size=immigration_size)

        self.individuals = self.population_crossover(roulette=roulette, crossover_ratio=crossover_ratio)

        self.individuals, killed = self.select(select_ratio=select_ratio, select_criterion=select_criterion)

        self.generation_number += 1

        return self.individuals

    def find_fittest(self, n=1):
        """
        the name says all
        :return:
        """
        assert n <= self.population_size
        rank_fitness = sorted(self.individuals, key=lambda list: list[1], reverse=True)
        return rank_fitness[0:n + 1]

    def gui_display_population(self, n=1):
        """
        the name says all
        :return:
        """
        info_population = []

        for number, individual in enumerate(self.individuals):
            individual_str = ''.join((str(number), '   |||   ', str(individual), '\n'))
            info_population.append(individual_str)
        population_message = ''.join(info_population)

        msg = 'Display generation number : ' + str(self.generation_number) + '\n' + \
              'individual#|||                       chromosome                 |fitness\n' \
              '-----------|||--------------------------------------------|-------\n' + \
              'fittest : ' + str(self.find_fittest(n))
        easygui.textbox(msg=msg, text=population_message, codebox=True)

    def show_radar_individual(self, rect=None):
        if rect is None:
            rect = [0, 0, 1, 1]

        fig = pl.figure()

        angles = np.linspace(90., 90 + 360., len(self.gene_set) + 1)[0:-1]
        axes = [fig.add_axes(rect, projection="polar", label="axes%d" % i) for i in range(len(self.gene_set))]
        ax = axes[0]
        ax.set_thetagrids(angles)

        for ax in axes:
            ax.patch.set_visible(False)
            ax.grid("off")
            ax.xaxis.set_visible(False)
            ax.yaxis.set_ticklabels([])  # hide the numbers of each radar line, took me so long

        for i, ax in enumerate(axes):
            ax.set_rgrids(range(1, len(self.gene_set[i])), angle=angles[i], labels=None)
            ax.spines["polar"].set_visible(False)
            ax.set_ylim(0, len(self.gene_set[i]))
            # due to matplot lib, it requires lim to be positive.
            # for the sake of beauty, I here change it to 0-numberofsites, so the picture looks more 'full'

        for individual in self.individuals:
            chromosome = individual[0]
            fitness = individual[1]
            fitness_max = max(self.individuals, key=lambda list: list[1])[1]
            fitness_min = min(self.individuals, key=lambda list: list[1])[1]
            fitness = (fitness - fitness_min) / (fitness_max - fitness_min + 0.0001)

            angle = np.deg2rad(np.r_[angles, angles[0]])
            chromosome = np.r_[chromosome, chromosome[0]]
            ax.plot(angle, chromosome, "-", lw=1, color=cm.coolwarm(fitness), alpha=0.3)

        fig.savefig('generation' + str(self.generation_number) + '.png')
        pl.close(fig)


def gui_input_gene():
    easygui.msgbox('  This is a (List-based Evolutionary Algorithm) program built by Yingkai Liu'
                   '\n                                enjoy!                                      '
                   '\n'
                   '\n                  should you find any problems, contact                     '
                   '\n                      water@mail.nankai.edu.cn                              ',
                   'List-based Evolutionary Algorithm')

    number_of_gene_input = easygui.enterbox(
        msg='           Here you need to specify number of chromosome sites first.',
        title='-number_of_gene',
        default='5')

    number_of_gene = int(number_of_gene_input)
    gene_set_field_name = []
    for i in range(number_of_gene):
        gene_set_field_name.append("*****************" + str(i) + "th gene's high")
        gene_set_field_name.append("low")
        gene_set_field_name.append("number of interval")

    gene_set_input = easygui.multenterbox(
        msg='Here you need to specify the high,low,step of each parameter\n and of course, it starts from zero\n',
        title='LEA-gene_set[]',
        fields=gene_set_field_name,
        values = [5,0,5,5,0,5,5,0,5,5,0,5,5,0,5])
        #values=[str(7 * i - i + 6) for i in range(len(gene_set_field_name))])

    hi_of_each_gene = []
    lo_of_each_gene = []
    n_of_each_gene = []

    step_of_each_gene = []
    range_of_each_gene = []
    val_of_each_gene = []

    for i in range(number_of_gene):
        hi_of_each_gene.append(float(gene_set_input[3 * i + 0]))
        lo_of_each_gene.append(float(gene_set_input[3 * i + 1]))
        n_of_each_gene.append(int(gene_set_input[3 * i + 2]))

    for i in range(number_of_gene):
        # take the absolute of high - low
        step_of_each_gene.append(abs((hi_of_each_gene[i] - lo_of_each_gene[i]) / float(n_of_each_gene[i] - 1)))
        range_of_each_gene.append(abs(hi_of_each_gene[i] - lo_of_each_gene[i]))
        val_of_each_gene.append([])

    for m in range(number_of_gene):
        for k in range(n_of_each_gene[m]):
            val_of_each_gene[m].append(lo_of_each_gene[m] + k * step_of_each_gene[m])

    confirm_message = ''
    for i in range(number_of_gene):
        info = ['***the ', str(i), 'th Gene:',
                '\n                 High:: ', str(hi_of_each_gene[i]),
                '\n                  Low:: ', str(lo_of_each_gene[i]),
                '\n                Range:: ', str(range_of_each_gene[i]),
                '\n                    N:: ', str(n_of_each_gene[i]),
                '\n                 Step:: ', str(step_of_each_gene[i]),
                '\n                         **********Gene Set @ site ' + str(i) + '**********',
                '\n                        ', str(val_of_each_gene[i]),
                '\n']
        confirm_message += ''.join(info)

    easygui.textbox(msg='Here is the confirm message of your input:\n'
                        '\n'
                        'total site = ' + str(number_of_gene) + '\n',
                    title='NSGA-confirm_message',
                    text=confirm_message,
                    codebox=True)

    gene_set = val_of_each_gene
    gene_range = range_of_each_gene

    return gene_set, gene_range


geneSet, geneRange = gui_input_gene()

a = population(gene_range=geneRange, gene_set=geneSet, population_size=10)
a.show_radar_individual()
for i in range(100):
    print('gen', a.generation_number)
    x = int(15 / (i+1))
    a.evolve(immigration_size=x)
    if a.generation_number == 100:
        a.show_radar_individual()


a.gui_display_population(4)
