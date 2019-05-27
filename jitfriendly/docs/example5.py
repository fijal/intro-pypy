import struct


class AccessorOne(object):
    def __init__(self, d):
        self.d = d

    def __getitem__(self, item):
        return self.d[item]

class AccessorTwo(object):
    def __init__(self, d):
        self._d = {}
        for k, v in d.iteritems():
            self._d[k] = struct.pack('iii', v[0], v[1], v[2])

    def __getitem__(self, item):
        return struct.unpack('iii', self._d[item])

d = {}
for i in range(10000000):
    d[str(i)] = (i, i+1, i+2)
a = AccessorOne(d)

del d


import time
t0 = time.time()
for i in range(10):
    for k in range(0, 10000000, 100):
        a[str(k)]
print time.time() - t0
