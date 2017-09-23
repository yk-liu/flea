class assign_fitness:
    def __init__(self):
        pass

    @staticmethod
    def simple_fitness(chromosome):
        return sum(chromosome)

    @staticmethod
    def user_defined_fitness(chromosome):
        raise NotImplementedError