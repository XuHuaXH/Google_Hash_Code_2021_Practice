from Solver import Delivery, Solver
import util
import random
import math


class SimulatedAnnealingSolver(Solver):
    def __init__(self, number_of_pizza, n2, n3, n4, pizza_data, pool_size, number_of_mutations, initial_temp, final_temp, alpha, beta, iterations_per_temp, temp_reduction):
        super().__init__(number_of_pizza, n2, n3, n4, pizza_data)
        self.pool_size = pool_size
        self.number_of_mutations = number_of_mutations
        self.curr_temp = initial_temp
        self.final_temp = final_temp
        self.alpha = alpha
        self.beta = beta
        self.iterations_per_temp = iterations_per_temp

        if temp_reduction == 'linear':
            self.temp_reduction = self.tempLinearReduction
        elif temp_reduction == 'geometric':
            self.temp_reduction = self.tempGeometricReduction
        elif temp_reduction == 'slow':
            self.temp_reduction = self.tempSlowReduction

    def tempLinearReduction(self):
        self.curr_temp -= self.alpha

    def tempGeometricReduction(self):
        self.curr_temp *= self.alpha

    def tempSlowReduction(self):
        self.curr_temp = self.curr_temp / (1 + self.beta * self.curr_temp)

    # generate the initial solution
    def initialize(self):
        self.population = [self.generateDelivery()]

    def mutate(self, delivery):
        # make a copy of the gene
        new_delivery = delivery.copy()
        new_gene = new_delivery.gene
        for i in range(self.number_of_mutations):
            position1 = random.randint(0, len(new_gene) - 1)
            position2 = random.randint(0, len(new_gene) - 1)
            temp = new_gene[position1]
            new_gene[position1] = new_gene[position2]
            new_gene[position2] = temp
        new_delivery.score = self.computeScore(delivery=new_delivery)
        return new_delivery

    def generate_neighbors(self):
        delivery = self.population[0]
        neighbors = []
        for i in range(self.pool_size):
            neighbor = self.mutate(delivery)
            neighbors.append(neighbor)
        return neighbors

        # assmues the input curr_generation is ranked
    def steepest_ascent_hill_climb(self, pool_size):
        # only one individual in each population
        delivery = self.population[0]
        neighbors = []
        for i in range(pool_size):
            neighbor = self.mutate(delivery)
            neighbors.append(neighbor)
        neighbors.sort(key=(lambda x: x.score), reverse=True)
        if neighbors[0].score > delivery.score:
            self.population[0] = neighbors[0]

    def simulated_annealing(self):
        while self.curr_temp > self.final_temp:
            for i in range(self.iterations_per_temp):
                neighbors = self.generate_neighbors()
                new_delivery = random.choice(neighbors)
                delta = new_delivery.score - self.population[0].score
                if delta >= 0 or random.random() < math.exp(delta / self.curr_temp):
                    self.population[0] = new_delivery
                print('iteration ' + str(i))
                print('current temp: ' + str(self.curr_temp))
                print(self.population[0].score)
            self.temp_reduction()

    def solve_by_hill_climb(self, number_of_generations):
        for i in range(number_of_generations):
            print('generation ' + str(i))
            self.steepest_ascent_hill_climb(1)
            print(self.population[0].score)


if __name__ == "__main__":
    intermediate_data = util.parse("./case2")
    pizza_num = intermediate_data[0]
    num_of_orders = intermediate_data[1]
    pizza_data = intermediate_data[2]

    n2 = num_of_orders[0]
    n3 = num_of_orders[1]
    n4 = num_of_orders[2]

    solver = SimulatedAnnealingSolver(number_of_pizza=pizza_num, n2=n2, n3=n3, n4=n4, pizza_data=pizza_data, pool_size=100,
                                      number_of_mutations=1, initial_temp=10, final_temp=0.1, alpha=0.9, beta=0, iterations_per_temp=100, temp_reduction='geometric')

    # solver.initialize()
    # solver.simulated_annealing()
    solver.population = [solver.load_from_file('./sol2')]
    solver.solve_by_hill_climb(100000)
    best = solver.getBest()
    solver.printDelivery(best)
    solver.write_to_file(solver.population[0], './sol2')
