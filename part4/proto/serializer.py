
import struct

def serialize(d):
    if isinstance(d, str):
        return "s" + struct.pack("i", len(d)) + d
    elif isinstance(d, int):
        return "i" + struct.pack("i", d)
    elif isinstance(d, list):
        return "l" + struct.pack("i", len(d)) + "".join([serialize(elem) for elem in d])
    elif isinstance(d, dict):
        return "d" + struct.pack("i", len(d)) + "".join([
            (serialize(k) + serialize(v)) for k, v in d.iteritems()])
    else:
        raise Exception("cannot serialize object %r" % d)

def _unserialize(msg):
    if msg[0] == "s":
        lgt, = struct.unpack("i", msg[1:5])
        return msg[5:5 + lgt], 5 + lgt
    elif msg[0] == "i":
        v, = struct.unpack("i", msg[1:5])
        return v, 5
    elif msg[0] == "l":
        num_items, = struct.unpack("i", msg[1:5])
        pos = 5
        r = []
        for i in range(num_items):
            v, new_pos = _unserialize(msg[pos:])
            pos += new_pos
            r.append(v)
        return r, pos
    elif msg[0] == "d":
        num_items, = struct.unpack("i", msg[1:5])
        pos = 5
        r = {}
        for i in range(num_items):
            k, new_pos = _unserialize(msg[pos:])
            pos += new_pos
            v, new_pos = _unserialize(msg[pos:])
            pos += new_pos
            r[k] = v
        return r, pos
    else:
        raise Exception("Cannot unserialize, unknown marker %s" % msg[0])

def unserialize(msg):
    return _unserialize(msg)[0]
