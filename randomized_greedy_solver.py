import math
import random


# choose the next pizza with the most number of ingredients
def plain_greedy_choose_pizza(pizza_dict, pizza_type_list, pool_size, rejection_rate, max_depth):
    return pizza_type_list[0]


# pool_size is the number of pizzas to randomly choose from
# assuming we still have at least pool_size many pizzas
def urandom_greedy_choose_pizza(pizza_dict, pizza_type_list, pool_size, rejection_rate, max_depth):
    chosen_index = random.randint(0, pool_size - 1)
    i = 0
    while i + 1 < len(pizza_type_list) and chosen_index - len(pizza_dict[pizza_type_list[i + 1]]) > 0:
        chosen_index -= len(pizza_dict[pizza_type_list[i + 1]])
        i += 1
    return pizza_type_list[i]


# for each pizza in the pool, we reject it with probability
# rejection_rate, unless we reach max_depth and accepts it
def random_reject_greedy_fill_orders(pizza_dict, pizza_type_list, pool_size, rejection_rate, max_depth):
    order = []
    num_of_ingredients = 0

    # TODO


def fill_orders(order_size, pizza_dict, pizza_type_list, choice_function, pool_size, rejection_rate, max_depth):
    order = []
    num_of_ingredients = 0
    ingredients_union = set(())

    while len(order) < order_size:
        chosen_pizza = choice_function(pizza_dict, pizza_type_list,
                                       pool_size, rejection_rate, max_depth)
        ingredients_union = ingredients_union.union(set(chosen_pizza))
        temp_list = pizza_dict[chosen_pizza]
        order.append(temp_list[len(temp_list) - 1])

        # remove the data related to the pizza chosen
        temp_list.pop(len(temp_list) - 1)
        if len(temp_list) == 0:
            pizza_dict.pop(chosen_pizza)
            pizza_type_list.remove(chosen_pizza)

    num_of_ingredients = len(ingredients_union)
    single_order_score = math.pow(num_of_ingredients, 2)
    return single_order_score, order


def comparisonFunc(ingredient_list):
    return len(ingredient_list)


def randomized_greedy_solver(m, n2, n3, n4, pizza_dict, pizza_type_list, choice_function, pool_size, rejection_rate, max_depth):
    solution = []
    total_score = 0
    random.seed()

    # sort the pizze_type_list by ingredient length
    pizza_type_list.sort(key=comparisonFunc)

    # fill orders in the order of n4, n3 and n2
    temp_dict = {2: n2, 3: n3, 4: n4}
    for i in reversed(range(2, 5)):
        while temp_dict[i] > 0 and m >= i:
            # makes sure pool_size <= number of pizzas left
            pool_size = min(pool_size, m)
            score, order = fill_orders(i, pizza_dict, pizza_type_list,
                                       choice_function, pool_size, rejection_rate, max_depth)
            temp_dict[i] -= 1
            m -= i
            solution.append(order)
            total_score += score

    return total_score, solution
