import random
import util


# gene is a permutation of the indices of all pizzas
class Delivery:
    def __init__(self, gene):
        self.score = 0
        self.gene = gene


# compute the score of a single order
def orderScore(order, pizza_data):
    ingredients_union = set(())
    for i in order:
        if i < 0:
            return 0
        ingredients_union = ingredients_union.union(set(pizza_data[i]))
    number_of_ingredients = len(ingredients_union)
    return number_of_ingredients ** 2


# compute the score of a single delivery
def computeScore(delivery, n2, n3, n4, pizza_data):
    total_score = 0
    index = 0
    gene = delivery.gene
    dict = {2: n2, 3: n3, 4: n4}
    for i in range(2, 5):
        while dict[i] > 0:
            order = gene[index: index + i]
            total_score += orderScore(order, pizza_data)
            index += i
            dict[i] -= 1
    # print('the score of the order ' + str(gene) + ' is ' + str(total_score))
    return total_score


# randomly generate a Delivery
def generateDelivery(index_list):
    gene = random.sample(index_list, len(index_list))
    # print(gene)
    return Delivery(gene)


# the best elite_size many individuals are selected directly
# for the rest in the population, each one is selected with
# probability based on its score
def select(ranked_population, elite_size):
    print('enter select')
    roulette_wheel = []
    scores = [i.score for i in ranked_population]
    cumulative_sum = 0
    for i in range(len(scores)):
        cumulative_sum += scores[i]
        roulette_wheel.append(cumulative_sum)

    # the ith individual in the population will be selected
    # if the number drawn is in [roulette_wheel[i - 1], roulette_wheel[i])
    selected = []

    for i in range(elite_size):
        selected.append(ranked_population[i])

    for i in range(elite_size, len(ranked_population)):
        draw = random.randint(0, cumulative_sum - 1)
        for j in range(len(roulette_wheel)):
            if draw < roulette_wheel[j]:
                selected.append(ranked_population[i])
                break

    selected.sort(key=(lambda x: x.score), reverse=True)
    # for i in selected:
    #     print('selected:')
    #     print(i.gene)
    print('exit select')
    return selected


def breed(parent1, parent2):
    print('enter breed')
    gene1 = parent1.gene
    gene2 = parent2.gene
    # print('gene1 is  ' + str(gene1))
    # print('gene2 is  ' + str(gene2))
    cut1 = random.randint(0, len(gene1))
    cut2 = random.randint(0, len(gene1))
    print('generating cuts')
    # makes sure cut1 != cut2
    while cut1 == cut2:
        cut2 = random.randint(0, len(gene1))

    cut_start = min(cut1, cut2)
    cut_end = max(cut1, cut2)
    print('cuts generated')

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
            print('appending child1')
            child_gene += child1
        else:
            curr = gene2[parent2_index]
            print('adding from parent 2')
            parent2_index += 1
            if curr not in child1:
                child_gene.append(curr)

    print('constructing child')
    child = Delivery(child_gene)
    # print('child is')
    # print(child.gene)
    print('exit breed')
    return child


class GeneticSolver:
    def __init__(self, number_of_pizza, n2, n3, n4, pizza_data, poplulation_size, elite_size, mutation_rate):
        self.number_of_pizza = number_of_pizza
        self.n2 = n2
        self.n3 = n3
        self.n4 = n4
        self.pizza_data = pizza_data
        self.poplulation_size = poplulation_size
        self.elite_size = elite_size
        self.mutation_rate = mutation_rate
        self.population = []

    # returns a list of Deliveries ranked high to low by fitness score
    def generatePopulation(self, num_of_people):
        population = []
        index_list = list(range(self.number_of_pizza))
        empty_pizza = -1
        while len(index_list) < num_of_people:
            index_list.append(empty_pizza)
            empty_pizza -= 1
        while len(population) < self.poplulation_size:
            delivery = generateDelivery(index_list)
            delivery.score = computeScore(delivery=delivery, n2=self.n2,
                                          n3=self.n3, n4=self.n4, pizza_data=self.pizza_data)
            if delivery.score > 0:
                population.append(delivery)

        population.sort(key=(lambda x: x.score), reverse=True)
        # print('the generated population is')
        # for i in population:
        #     print(str(i.gene) + ' ' + str(i.score))
        return population

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
            child.score = computeScore(delivery=child, n2=self.n2,
                                       n3=self.n3, n4=self.n4, pizza_data=self.pizza_data)
            if child.score > 0:
                next_population.append(child)
        # next_population.sort(key=(lambda x: x.score), reverse=True)
        return next_population

    def mutatePopulation(self):
        print('enter mutate population')
        # only mutate those non-elites
        for i in range(0, len(self.population)):
            delivery = self.population[i]
            draw = random.random()
            if draw < self.mutation_rate:
                gene = delivery.gene
                position1 = random.randint(0, len(gene) - 1)
                position2 = random.randint(0, len(gene) - 1)
                temp = gene[position1]
                gene[position1] = gene[position2]
                gene[position2] = temp
            delivery.score = computeScore(delivery, n2=self.n2, n3=self.n3,
                                          n4=self.n4, pizza_data=pizza_data)

        # rank the entire poplulation
        self.population.sort(key=(lambda x: x.score), reverse=True)
        print('exit mutate population')
        # print('this generation is')
        # for i in self.population:
        #     print(str(i.gene) + ' ' + str(i.score))

    # assmues the input curr_generation is ranked
    def evolve(self, curr_generation, poplulation_size, elite_size, mutation_rate, pizza_data,):
        ranked_selected = select(curr_generation, elite_size)
        next_generation = self.breedPopulation(ranked_selected)
        self.mutatePopulation()
        return next_generation

    # generate the initial generation
    def initialize(self):
        number_of_people = self.n2 * 2 + self.n3 * 3 + self.n4 * 4
        self.population = self.generatePopulation(number_of_people)

    def solve(self, number_of_generations):
        for i in range(number_of_generations):
            print('generation ' + str(i))
            self.population = self.evolve(curr_generation=self.population, poplulation_size=self.poplulation_size,
                                          elite_size=self.elite_size, mutation_rate=self.mutation_rate, pizza_data=self.pizza_data)
            print(self.population[0].score)

    # returns the best individual in the population
    def getBest(self):
        return self.population[0]

    # print a delivery in the output file format
    def printDelivery(self, delivery):
        num2 = self.n2
        num3 = self.n3
        num4 = self.n4
        gene = delivery.gene

        lines = []
        index = 0
        dict = {2: num2, 3: num3, 4: num4}
        for i in range(2, 5):
            while dict[i] > 0:
                empty_order = False
                line = str(i)
                for j in range(i):
                    if gene[index + j] < 0:
                        empty_order = True
                        continue
                    line += ' ' + str(gene[index + j])
                dict[i] -= 1
                index += i
                if not empty_order:
                    lines.append(line)
        print(len(lines))
        for line in lines:
            print(line)


if __name__ == "__main__":
    intermediate_data = util.parse("./case4")
    pizza_num = intermediate_data[0]
    num_of_orders = intermediate_data[1]
    pizza_data = intermediate_data[2]

    # processed_data = util.data_to_dict(pizza_data)
    # pizza_dict = processed_data[0]
    # pizza_type_list = processed_data[1]

    n2 = num_of_orders[0]
    n3 = num_of_orders[1]
    n4 = num_of_orders[2]

    solver = GeneticSolver(number_of_pizza=pizza_num, n2=n2, n3=n3, n4=n4,
                           pizza_data=pizza_data, poplulation_size=10, elite_size=1, mutation_rate=0.01)

    solver.initialize()
    solver.solve(15)
    best = solver.getBest()
    solver.printDelivery(best)
