# let a gene be[3, 2, 4, 0, 2] where the numbers are index of the pizzas.
# [3, 2, 4, 0, 2] means the combo[3, 2, 4, 0] will be given the the 4 - person team
# since there might not be enough pizzas, we need "empty" pizzas, which will be indexed as -1
# use ordered crossover
# use swapping for mutation
#
# scoring: as usual


class Parent:
    def __init__(self, a):
        self.a = a

    def fun(self):
        print('hey')


class Child(Parent):
    pass


if __name__ == "__main__":
    c = Child(10)
    print(c.a)
    c.fun()
