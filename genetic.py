import random
import util


# gene is a permutation of the indices of all pizzas
class Delivery:
    def __init__(self, gene):
        self.score = 0
        self.gene = gene

    # returns a deep copy of the object
    def copy(self):
        new_gene = []
        new_gene += self.gene
        new_delivery = Delivery(new_gene)
        new_delivery.score = self.score
        return new_delivery


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
    # print('exit select')
    return selected


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

        # compute number_of_people
        self.number_of_people = self.n2 * 2 + self.n3 * 3 + self.n4 * 4

        # initialize index_list
        self.index_list = list(range(self.number_of_pizza))
        empty_pizza = -1
        while len(self.index_list) < self.number_of_people:
            self.index_list.append(empty_pizza)
            empty_pizza -= 1

    # returns a list of Deliveries ranked high to low by fitness score
    def generatePopulation(self, num_of_people):
        population = []
        while len(population) < self.poplulation_size:
            delivery = generateDelivery(self.index_list)
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
        new_delivery.score = computeScore(delivery=new_delivery, n2=self.n2,
                                          n3=self.n3, n4=self.n4, pizza_data=self.pizza_data)
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
        ranked_selected = select(self.population, self.elite_size)
        next_generation = self.breedPopulation(ranked_selected)
        self.population = self.mutatePopulation(next_generation)

    # assmues the input curr_generation is ranked
    def steepest_ascent_hill_climb(self, pool_size):
        # only one individual in each population
        delivery = self.population[0]
        neighbors = []
        for i in range(pool_size):
            neighbor = self.mutate(delivery, 1)
            neighbors.append(neighbor)
        neighbors.sort(key=(lambda x: x.score), reverse=True)
        if neighbors[0].score > delivery.score:
            self.population[0] = neighbors[0]

    # perform one round of monte carlo
    def monte_carlo(self):
        delivery = self.population[0]
        new_delivery = generateDelivery(self.index_list)
        new_delivery.score = computeScore(
            new_delivery, n2=self.n2, n3=self.n3, n4=self.n4, pizza_data=pizza_data)
        if new_delivery.score > delivery.score:
            self.population[0] = new_delivery

    # generate the initial generation
    def initialize(self):
        self.population = self.generatePopulation(self.number_of_people)

    # load a single solution into population[0] from file
    # assuming the solutions gives orders for 4-person teams first,
    # then 3-person teams and 2-person teams
    def load_from_file(self, filename):
        with open(filename, "r") as f:
            lines = f.readlines()[1:]
            gene = []
            line_number = 0
            empty_pizza = -1
            num2 = self.n2
            num3 = self.n3
            num4 = self.n4
            dict = {2: num2, 3: num3, 4: num4}
            for i in range(2, 5):
                print(i)
                while line_number < len(lines):
                    line = lines[line_number].split(' ')
                    if int(line[0]) != i:
                        break
                    gene += [int(j) for j in line[1:]]
                    line_number += 1
                    dict[i] -= 1
                while dict[i] > 0:
                    for j in range(i):
                        gene.append(empty_pizza)
                        empty_pizza -= 1
                    dict[i] -= 1
            solution = Delivery(gene)
            solution.score = computeScore(delivery=solution, n2=self.n2,
                                          n3=self.n3, n4=self.n4, pizza_data=self.pizza_data)
            print('the solution is')
            print(solution.gene)
            # self.printDelivery(solution)
            print('the score for the loaded solution is ' + str(solution.score))
            return solution

    def write_to_file(self, delivery, outfile):
        with open(outfile, "w") as f:
            index = 0
            gene = delivery.gene
            num2 = self.n2
            num3 = self.n3
            num4 = self.n4
            dict = {2: num2, 3: num3, 4: num4}
            valid_orders = []
            for i in range(2, 5):
                while dict[i] > 0:
                    empty_order = False
                    dict[i] -= 1
                    order = gene[index: index + i]
                    for pizza in order:
                        if pizza < 0:
                            empty_order = True
                            break
                    if not empty_order:
                        valid_orders.append(order)
                    index += i
            f.write(str(len(valid_orders)) + '\n')
            for order in valid_orders:
                line = str(len(order))
                for pizza_index in order:
                    line += ' '
                    line += str(pizza_index)
                f.write(line + '\n')

    def solve(self, number_of_generations):
        for i in range(number_of_generations):
            print('generation ' + str(i))
            # self.evolve()
            self.steepest_ascent_hill_climb(1)
            # self.monte_carlo()
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
    intermediate_data = util.parse("./case3")
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
                           pizza_data=pizza_data, poplulation_size=1, elite_size=1, mutation_rate=0.01)

    # solver.initialize()
    solver.population = [solver.load_from_file('./sol3')]
    solver.solve(100)
    best = solver.getBest()
    solver.printDelivery(best)
    solver.write_to_file(solver.population[0], './sol3')
