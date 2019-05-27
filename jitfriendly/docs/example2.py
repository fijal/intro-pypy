
def gen_func(arg):
    def func(a):
        return a + arg

a_1 = gen_func(1)
a_2 = gen_func(2)
a_3 = gen_func(3) # same as RPython!
