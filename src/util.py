def parse(filename):
    pizza_data = []
    first_line = True

    f = open(filename, "r")
    for line in f:
        line = line.rstrip('\n')
        if first_line:
            first_line_data = line.split(' ')
            m = int(first_line_data[0])
            n2 = int(first_line_data[1])
            n3 = int(first_line_data[2])
            n4 = int(first_line_data[3])
            first_line = False
        else:
            ingredients = line.split(' ')[1:]
            pizza_data.append(ingredients)
    pizza_num = m
    num_of_orders = [n2, n3, n4]
    return pizza_num, num_of_orders, pizza_data


def data_to_dict(data):
    pizza_dict = {}
    pizza_type_list = []
    for i, ingredients in enumerate(data):
        pizza = tuple(sorted(ingredients))
        if pizza not in pizza_dict:
            pizza_dict[pizza] = []
            pizza_type_list.append(pizza)
        pizza_dict[pizza].append(i)
    return pizza_dict, pizza_type_list


# solution has the form [[score1, pizza1, pizza2],
#[score2, pizza3, pizza4, pizza5]]
def score(solution):
    total = 0
    for i in range(0, len(solution)):
        total += solution[i][0] * solution[i][0]
    return total


def score_minimal_solver(solution, pizza_data):
    total = 0
    for combo in solution:
        if len(combo) == 2:
            score = len(set(pizza_data[combo[0]]).union(set(pizza_data[combo[1]])))
        if len(combo) == 3:
            score = len((set(pizza_data[combo[0]]).union(
                set(pizza_data[combo[1]]))).union(set(pizza_data[combo[2]])))
        if len(combo) == 4:
            score = len(((set(pizza_data[combo[0]]).union(set(pizza_data[combo[1]]))).union(
                pizza_data[combo[2]])).union(set(pizza_data[combo[3]])))
        total += score * score
    return total


def write(solution):
    print(len(solution))
    for delivery in solution:
        line = str(len(delivery) - 1) + ' '
        for index in delivery[1:]:
            line += str(index)
            line += ' '
        print(line)
    print(score(solution))


def write_minimal(solution, pizza_data):
    print(len(solution))
    for delivery in solution:
        line = str(len(delivery)) + ' '
        for index in delivery:
            line += str(index)
            line += ' '
        print(line)
    print(score_minimal_solver(solution, pizza_data))
