# fill orders in reverse order of the input list of pizzas
# fill all the 2-pizza orders first and then 3 and last 4


def minimal_solver(m, n2, n3, n4, pizza_data):
    deliveries = []
    while n2 > 0:
        if m >= 2:
            delivery = [m - 1, m - 2]
            deliveries.append(delivery)
            m -= 2
        else:
            break
        n2 -= 1
    while n3 > 0:
        if m >= 3:
            delivery = [m - 1, m - 2, m - 3]
            deliveries.append(delivery)
            m -= 3
        else:
            break
        n3 -= 1
    while n4 > 0:
        if m >= 4:
            delivery = [m - 1, m - 2, m - 3, m - 4]
            deliveries.append(delivery)
            m -= 4
        else:
            break
        n4 -= 1
    return deliveries
