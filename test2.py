def read_from_file(filename):
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

    # data=[[tomato,olive,onion],[basial,olive,cheese]]
# pizza_dict={ingredients:[list of indices],...}


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


def union_count(set1, set2):
    return len(set1.union(set2))

# data=pizza_type_list


def max2(data):
    max = 0
    choice = {}
    for i in range(0, len(data)):
        for j in range(i + 1, len(data)):
            curr_count = len(set(data[i]).union(set(data[j])))
            if curr_count > max:
                max = curr_count
                choice = [data[i], data[j]]
    return max, choice


def max3(data):
    max = 0
    choice = {}
    for i in range(0, len(data)):
        for j in range(i + 1, len(data)):
            for k in range(j + 1, len(data)):
                curr_count = len(set(data[i]).union(set(data[j]).union(set(data[k]))))
                if curr_count > max:
                    max = curr_count
                    choice = [data[i], data[j], data[k]]
    return max, choice


def max4(data):
    max = 0
    choice = {}
    for i in range(0, len(data)):
        for j in range(i + 1, len(data)):
            for k in range(j + 1, len(data)):
                for w in range(k + 1, len(data)):
                    curr_count = len(set(data[i]).union(
                        set(data[j]).union(set(data[k]).union(set(data[w])))))
                    if curr_count > max:
                        max = curr_count
                        choice = [data[i], data[j], data[k], data[w]]
    return max, choice


# fill best order first
def best_order_first(m, n2, n3, n4, pizza_dict, pizza_type_list):

    # a list of lists of indices, representing the pizzas chosen
    # for example, [[1, 4], [2, 3, 0]] means pizza1 and pizz4 were
    # deliverd to a team of two
    deliveries = []
    while n2 + n3 + n4 > 0:
        if len(pizza_dict) == 0:
            break
        if m <= 1:
            break

        max_2 = 0 if n2 == 0 else max2(pizza_type_list)
        max_3 = 0 if n3 == 0 else max3(pizza_type_list)
        max_4 = 0 if n4 == 0 else max4(pizza_type_list)

        if max_2 + max_3 + max_4 == 0:
            break

        # find the best choice among max_2, max_3 and max_4
        choice = max_2
        options = [max_3, max_4]
        for option in options:
            if option[0] > choice[0]:
                choice = option

        # update the number of orders left
        if choice == max_2:
            n2 -= 1
        elif choice == max_3:
            n3 -= 1
        else:
            n4 -= 1

        # execute the chosen order
        delivery = []
        for type_of_pizza in choice[1]:
            index = pizza_dict[type_of_pizza].pop()
            if len(pizza_dict[type_of_pizza]) == 0:
                pizza_dict.pop(type_of_pizza)
                pizza_type_list.remove(type_of_pizza)
            delivery.append(index)
            m -= 1
        deliveries.append(delivery)

    # print the final result
    print(len(deliveries))
    for delivery in deliveries:
        line = str(len(delivery)) + ' '
        for index in delivery:
            line += str(index)
            line += ' '
        print(line)


if __name__ == "__main__":
    pizza_num = read_from_file("./case2")[0]
    pizza_data = read_from_file("./case2")[2]
    processed_data = data_to_dict(pizza_data)
    num_of_orders = read_from_file("./case2")[1]
    n2 = num_of_orders[0]
    n3 = num_of_orders[1]
    n4 = num_of_orders[2]
    best_order_first(pizza_num, n2, n3, n4, processed_data[0], processed_data[1])
