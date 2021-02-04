from Solver import Delivery, Solver
import util
import random


def breed(parent1, parent2):
    # print('enter breed')
    gene1 = parent1.gene
    gene2 = parent2.gene
    # print('gene1 is  ' + str(gene1))
    # print('gene2 is  ' + str(gene2))
    cut1 = random.randint(0, len(gene1))
    cut2 = random.randint(0, len(gene1))
    # print('generating cuts')
    # makes sure cut1 != cut2
    while cut1 == cut2:
        cut2 = random.randint(0, len(gene1))

    cut_start = min(cut1, cut2)
    cut_end = max(cut1, cut2)
    # print('cuts generated')

    child_gene = []
    parent2_index = 0
    child1 = gene1[cut_start: cut_end + 1]
    # print('len(gene1) is  ' + str(len(gene1)))
    # print('cut start is  ' + str(cut_start))
    # print('cut end is  ' + str(cut_end))
    # print('child1 is  ' + str(child1))
    # print('parent2 is  ' + str(parent2.gene))
    while len(child_gene) < len(gene1):
        # print('parent2 index is  ' + str(parent2_index))
        # print('len(gene2) is  ' + str(len(gene2)))
        if len(child_gene) == cut_start:
            # print('appending child1')
            child_gene += child1
        else:
            curr = gene2[parent2_index]
            # print('adding from parent 2')
            parent2_index += 1
            if curr not in child1:
                child_gene.append(curr)

    # print('constructing child')
    child = Delivery(child_gene)
    # print('child is')
    # print(child.gene)
    # print('exit breed')
    return child


class GeneticSolver(Solver):
    def __init__(self, number_of_pizza, n2, n3, n4, pizza_data, poplulation_size, elite_size, mutation_rate):
        super().__init__(number_of_pizza, n2, n3, n4, pizza_data)
        self.poplulation_size = poplulation_size
        self.elite_size = elite_size
        self.mutation_rate = mutation_rate

    # returns a list of Deliveries ranked high to low by fitness score
    def generatePopulation(self):
        population = []
        while len(population) < self.poplulation_size:
            delivery = self.generateDelivery()
            delivery.score = self.computeScore(delivery)
            if delivery.score > 0:
                population.append(delivery)

        population.sort(key=(lambda x: x.score), reverse=True)
        # print('the generated population is')
        # for i in population:
        #     print(str(i.gene) + ' ' + str(i.score))
        return population

    # the best elite_size many individuals are selected directly
    # for the rest in the population, each one is selected with
    # probability based on its score
    def select(self, ranked_population):
        # print('enter select')
        roulette_wheel = []
        scores = [i.score for i in ranked_population]
        cumulative_sum = 0
        for i in range(len(scores)):
            cumulative_sum += scores[i]
            roulette_wheel.append(cumulative_sum)

        # the ith individual in the population will be selected
        # if the number drawn is in [roulette_wheel[i - 1], roulette_wheel[i])
        selected = []

        for i in range(self.elite_size):
            selected.append(ranked_population[i])

        for i in range(self.elite_size, len(ranked_population)):
            draw = random.randint(0, cumulative_sum - 1)
            for j in range(len(roulette_wheel)):
                if draw < roulette_wheel[j]:
                    selected.append(ranked_population[i])
                    break

        selected.sort(key=(lambda x: x.score), reverse=True)
        # for i in selected:
        #     print('selected:')
        #     print(i.gene)
        # print('exit select')
        return selected

    # elite_size of ranked_selected goes directly into the
    # next generation, others are children of the selected parents
    def breedPopulation(self, ranked_selected):
        next_population = []
        for i in range(self.elite_size):
            next_population.append(ranked_selected[i])
        while len(next_population) < self.poplulation_size:
            parent1 = ranked_selected[random.randint(0, len(ranked_selected) - 1)]
            parent2 = ranked_selected[random.randint(0, len(ranked_selected) - 1)]
            child = breed(parent1, parent2)
            child.score = self.computeScore(delivery=child)
            if child.score > 0:
                next_population.append(child)
        # next_population.sort(key=(lambda x: x.score), reverse=True)
        return next_population

    def mutate(self, delivery, number_of_mutations):
        # make a copy of the gene
        new_delivery = delivery.copy()
        new_gene = new_delivery.gene
        for i in range(number_of_mutations):
            position1 = random.randint(0, len(new_gene) - 1)
            position2 = random.randint(0, len(new_gene) - 1)
            temp = new_gene[position1]
            new_gene[position1] = new_gene[position2]
            new_gene[position2] = temp
        new_delivery.score = self.computeScore(delivery=new_delivery)
        return new_delivery

    def mutatePopulation(self, next_generation):
        # print('enter mutate population')
        # only mutate those non-elites
        for i in range(self.elite_size, len(next_generation)):
            draw = random.random()
            if draw < self.mutation_rate:
                new_delivery = self.mutate(next_generation[i], 1)
                while new_delivery.score == 0:
                    new_delivery = self.mutate(next_generation[i], 1)
                next_generation[i] = new_delivery

        # rank the entire poplulation
        next_generation.sort(key=(lambda x: x.score), reverse=True)
        return next_generation
        # print('exit mutate population')
        # print('this generation is')
        # for i in self.population:
        #     print(str(i.gene) + ' ' + str(i.score))

    # assmues the input curr_generation is ranked
    def evolve(self):
        ranked_selected = self.select(self.population)
        next_generation = self.breedPopulation(ranked_selected)
        self.population = self.mutatePopulation(next_generation)

    # generate the initial generation
    def initialize(self):
        self.population = self.generatePopulation()

    def solve(self, number_of_generations):
        for i in range(number_of_generations):
            print('generation ' + str(i))
            self.evolve()
            print(self.population[0].score)


if __name__ == "__main__":
    intermediate_data = util.parse("./case1")
    pizza_num = intermediate_data[0]
    num_of_orders = intermediate_data[1]
    pizza_data = intermediate_data[2]

    n2 = num_of_orders[0]
    n3 = num_of_orders[1]
    n4 = num_of_orders[2]

    solver = GeneticSolver(number_of_pizza=pizza_num, n2=n2, n3=n3, n4=n4,
                           pizza_data=pizza_data, poplulation_size=100, elite_size=10, mutation_rate=0.01)

    solver.initialize()
    solver.solve(100)
    best = solver.getBest()
    solver.printDelivery(best)
    # solver.write_to_file(solver.population[0], './sol1')
