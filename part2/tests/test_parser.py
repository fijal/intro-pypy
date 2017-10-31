
from asminterp.parser import parse, repr_bytecode

class TestParser(object):
    def test_basic(self):
        input = """
            -constants-
            -code-
            load_integer 0
            store 0
            load 0
            load_integer 1
            add
        """

        p = parse(input)
        exp = [x.strip() for x in input.split("\n")[3:] if x.strip()]
        assert repr_bytecode(p).split("\n") == exp
