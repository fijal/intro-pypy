
from asminterp.model import Integer

OPCODES = [
    'load_integer',
    'load_constant',
    'load',
    'store',
    'add',
    'sub',
    'lt',
    'jump_if_false',
    'jump_if_true',
    'jump',
    'discard',
    'print',
]

ARGNUM = [
    1,
    1,
    1,
    1,
    0,
    0,
    0,
    2,
    2,
    1,
    0,
    0,
]

LOOKUP = {}
for i, opcode in enumerate(OPCODES):
    LOOKUP[opcode] = i
    globals()[opcode.upper()] = i
del i, opcode

class Bytecode(object):
    def __init__(self, bc, consts):
        self.bc = bc
        self.consts = consts

class Parser(object):
    def __init__(self):
        self.l = []
        self.consts = []

    def feed(self, i, line):
        elems = line.split(" ")
        if len(elems) == 1:
            arg0 = 0
            arg1 = 0
        elif len(elems) == 2:
            arg0 = int(elems[1])
            arg1 = 0
        else:
            arg0 = int(elems[1])
            arg1 = int(elems[2])
        self.l.extend([chr(LOOKUP[elems[0]]), chr(arg0), chr(arg1)])

    def add_constant(self, i, line):
        assert i == len(self.consts)
        tp, val = line.split(" ", 2)
        assert tp == "int"
        self.consts.append(Integer(int(val)))

    def build(self):
        return Bytecode("".join(self.l), self.consts)

def repr_bytecode(bytecode):
    i = 0
    lines = []
    bc = bytecode.bc
    while i < len(bc):
        nxt = ord(bc[i])
        if ARGNUM[nxt] > 0:
            arg0 = ord(bc[i + 1])
            if ARGNUM[nxt] > 1:
                arg1 = ord(bc[i + 2])
                lines.append("%s %s %s" % (OPCODES[nxt], arg0, arg1))
            else:
                lines.append("%s %s" % (OPCODES[nxt], arg0))
        else:
            lines.append(OPCODES[nxt])
        i += 3
    return "\n".join(lines)

def parse(code):
    lines = [x.strip() for x in code.split("\n") if x.strip()]
    p = Parser()
    assert lines[0] == '-constants-'
    code_line = 0
    while lines[code_line] != '-code-':
        code_line += 1
    for item in range(1, code_line):
        p.add_constant(item - 1, lines[item])
    for item in range(code_line + 1, len(lines)):
        p.feed(item, lines[item])
    return p.build()
