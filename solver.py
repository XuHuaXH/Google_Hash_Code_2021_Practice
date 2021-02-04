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


class Solver:
    def __init__(self, number_of_pizza, n2, n3, n4, pizza_data):
        self.number_of_pizza = number_of_pizza
        self.n2 = n2
        self.n3 = n3
        self.n4 = n4
        self.pizza_data = pizza_data
        self.population = []

        # compute number_of_people
        self.number_of_people = self.n2 * 2 + self.n3 * 3 + self.n4 * 4

        # initialize index_list
        self.index_list = list(range(self.number_of_pizza))
        empty_pizza = -1
        while len(self.index_list) < self.number_of_people:
            self.index_list.append(empty_pizza)
            empty_pizza -= 1

    # randomly generate a Delivery
    def generateDelivery(self):
        gene = random.sample(self.index_list, len(self.index_list))
        # print(gene)
        return Delivery(gene)

    # compute the score of a single order
    def orderScore(self, order):
        ingredients_union = set(())
        for i in order:
            if i < 0:
                return 0
            ingredients_union = ingredients_union.union(set(self.pizza_data[i]))
        number_of_ingredients = len(ingredients_union)
        return number_of_ingredients ** 2

    # compute the score of a single delivery
    def computeScore(self, delivery):
        total_score = 0
        index = 0
        gene = delivery.gene
        dict = {2: self.n2, 3: self.n3, 4: self.n4}
        for i in range(2, 5):
            while dict[i] > 0:
                order = gene[index: index + i]
                total_score += self.orderScore(order)
                index += i
                dict[i] -= 1
        # print('the score of the order ' + str(gene) + ' is ' + str(total_score))
        return total_score

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
            solution.score = self.computeScore(delivery=solution)
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
