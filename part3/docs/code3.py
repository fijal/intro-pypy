from _example import ffi, lib

def f():
    for i in range(100000):
        p = lib.getpwuid(0)
        assert ffi.string(p.pw_name) == b'root'

f()
