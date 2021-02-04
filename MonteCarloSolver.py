from Solver import Delivery, Solver
import util
import random


class MonteCarloSolver(Solver):
    def __init__(self, number_of_pizza, n2, n3, n4, pizza_data):
        super().__init__(number_of_pizza, n2, n3, n4, pizza_data)

    # generate the initial solution
    def initialize(self):
        self.population = [self.generateDelivery()]

    # perform one round of monte carlo
    def monte_carlo(self):
        delivery = self.population[0]
        new_delivery = self.generateDelivery()
        new_delivery.score = self.computeScore(delivery=new_delivery)
        if new_delivery.score > delivery.score:
            self.population[0] = new_delivery

    def solve(self, number_of_generations):
        for i in range(number_of_generations):
            print('generation ' + str(i))
            self.monte_carlo()
            print(self.population[0].score)


if __name__ == "__main__":
    intermediate_data = util.parse("./case2")
    pizza_num = intermediate_data[0]
    num_of_orders = intermediate_data[1]
    pizza_data = intermediate_data[2]

    n2 = num_of_orders[0]
    n3 = num_of_orders[1]
    n4 = num_of_orders[2]

    solver = MonteCarloSolver(number_of_pizza=pizza_num, n2=n2, n3=n3, n4=n4,
                              pizza_data=pizza_data)

    solver.initialize()
    solver.solve(10000)
    best = solver.getBest()
    solver.printDelivery(best)
    # solver.write_to_file(solver.population[0], './sol1')
