import util
import minimal_solver
import randomized_greedy_solver

for i in range(1, 6):
    intermediate_data = util.parse("./case" + str(i))
    pizza_num = intermediate_data[0]
    num_of_orders = intermediate_data[1]
    pizza_data = intermediate_data[2]

    processed_data = util.data_to_dict(pizza_data)
    pizza_dict = processed_data[0]
    pizza_type_list = processed_data[1]

    n2 = num_of_orders[0]
    n3 = num_of_orders[1]
    n4 = num_of_orders[2]

    # solution = minimal_solver.minimal_solver(pizza_num, n2, n3, n4, pizza_data)
    # util.write_minimal(solution, pizza_data, i)

    total_score, solution = randomized_greedy_solver.randomized_greedy_solver(
        m=pizza_num, n2=n2, n3=n3, n4=n4, pizza_dict=pizza_dict, pizza_type_list=pizza_type_list, choice_function=randomized_greedy_solver.urandom_greedy_choose_pizza, pool_size=100000, rejection_rate=0.25, max_depth=10)
    util.write(solution, i)
    print('The score for case ' + str(i) + ' is ' + str(total_score))
