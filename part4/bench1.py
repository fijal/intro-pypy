
from proto.serializer import serialize, unserialize

def bench_serialize():
    d = {}
    l = [None]
    for i in range(100):
        d[str(i) + "foo"] = "foobarbaz" * 20
    for i in range(100000):
        l[0] = serialize(d)

def bench_unserialize():
    d = {}
    l = [None]
    for i in range(100):
        d[str(i) + "foo"] = "foobarbaz" * 20
    s = serialize(d)
    for i in range(100000):
        l[0] = unserialize(s)

def bench_access():
    d = {}
    l = [None, None, None]
    for i in range(100):
        d[str(i) + "foo"] = "foobarbaz" * 20
    s = serialize(d)
    u = unserialize(s)
    for i in range(10000000):
        l[0] = u["13foo"]
        l[1] = u["14foo"]
        l[2] = u["15foo"]


bench_unserialize()
#bench_access()
#bench_serialize()
