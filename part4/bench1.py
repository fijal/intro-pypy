
from proto.serializer import serialize, unserialize

def bench_unserialize():
    d = {}
    for i in range(100):
        d[str(i) + "foo"] = [1, 2, 3]
    s = serialize(d)
    for i in range(10000):
        unserialize(s)

bench_unserialize()

