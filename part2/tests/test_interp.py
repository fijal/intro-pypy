
from asminterp import interp1, interp2, interp3
from asminterp.parser import parse

from rpython.jit.metainterp.test.support import LLJitMixin

class BaseTestInterp(object):
    def interp(self, p):
        self.printed = []
        def print_fn(arg):
            self.printed.append(arg)
        return self._interp(parse(p), print_fn)

    def test_return_1(self):
        self.interp("""
            -constants-
            -code-
            load_integer 13
            print
            """)
        assert self.printed == ["13"]

    def test_loop(self):
        self.interp("""
            -constants-
            int 100
            -code-
            load_constant 0
            store 0
            load 0
            jump_if_false 9
            load 0
            load_integer 1
            sub
            store 0
            jump 2
            load 0
            print
            """)
        assert self.printed == ['0']

class TestInterp1(BaseTestInterp):
    _interp = staticmethod(interp1.interp)

class TestInterp2(BaseTestInterp):
    _interp = staticmethod(interp2.interp)

class TestInterp3(BaseTestInterp):
    _interp = staticmethod(interp3.interp)

class BaseTestJitInterp(LLJitMixin):
    def interp(self, p):
        def print_fn(arg):
            pass

        strings = [p, ""]

        def f(arg):
            self._interp(parse(strings[arg]), print_fn)

        self.meta_interp(f, [0], listops=True)

    def test_loop(self):
        self.interp("""
            -constants-
            int 100
            -code-
            load_constant 0
            store 0
            load 0
            jump_if_false 9
            load 0
            load_integer 1
            sub
            store 0
            jump 2
            load 0
            print
            """)

class TestJitInterp1(BaseTestJitInterp):
    _interp = staticmethod(interp1.interp)

class TestJitInterp2(BaseTestJitInterp):
    _interp = staticmethod(interp2.interp)

class TestJitInterp3(BaseTestJitInterp):
    _interp = staticmethod(interp3.interp)
