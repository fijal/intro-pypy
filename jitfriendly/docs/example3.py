
def f(a):
    return a + 3

def test():
    s = 0
    for i in range(1000000):
        s += f(i)

if __name__ == '__main__':
    import time
    t0 = time.time()
    test()
    print time.time() - t0
