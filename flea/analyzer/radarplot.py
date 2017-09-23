import matplotlib.pyplot as pl
import numpy as np


def plot_radar_individual(self, rect=None):
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