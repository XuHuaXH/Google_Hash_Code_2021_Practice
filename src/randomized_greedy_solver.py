

def comparisonFunc(ingredient_list):
    return len(ingredient_list)


def plain_greedy_fill_orders(num_of_orders_left, order_size, pizza_dict, pizza_type_list):
    order = []
    num_of_ingredients = 0
    ingredients_union = {}

    while len(order) < order_size:
        chosen_pizza = pizza_type_list[0]
        ingredients_union.union(set(chosen_pizza)
        index=pizza_dict[chosen_pizza].pop()
        order.push(index)
        if len(pizza_dict[chosen_pizza]) == 0:
            pizza_dict.pop(chosen_pizza)
            pizza_type_list.remove(chosen_pizza)
    num_of_ingredients=len(ingredients_union)
    order.insert(0, num_of_ingredients)
    return order



def urandom_greedy_fill_orders(num_of_orders_left, order_size, pizza_dict, pizza_type_list):
    order=[]
    num_of_ingredients=0

    # TODO

def random_reject_greedy_fill_orders(num_of_orders_left, order_size, pizza_dict, pizza_type_list):
    order=[]
    num_of_ingredients=0

    # TODO




#
def randomized_greedy_solver(m, n2, n3, n4, pizza_dict, pizza_type_list):
    solution=[]

    # sort the pizze_type_list by ingredient length
    pizza_type_list.sort(key=comparisonFunc)

    # fill orders in the order of n4, n3 and n2
    while n4 > 0 and m >= 4:
        order=plain_greedy_fill_orders(n4, 4, pizza_dict, pizza_type_list)
        n4 -= 1
        m -= 4
        solution.push(order)

    while n3 > 0 and m >= 3:
        order=plain_greedy_fill_orders(n4, 3, pizza_dict, pizza_type_list)
        n4 -= 1
        m -= 3
        solution.push(order)

    while n2 > 0 and m >= 2:
        order=plain_greedy_fill_orders(n4, 2, pizza_dict, pizza_type_list)
        n4 -= 1
        m -= 2
        solution.push(order)

    return solution
