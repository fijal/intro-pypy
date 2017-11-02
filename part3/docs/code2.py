
""" Example - moving between layers
"""

from rpython.rtyper.lltypesystem import lltype, rffi
from rpython.rtyper.annlowlevel import llstr, hlstr

x = "foo"
print x
llx = llstr(x)
print llx
llx.chars[2] = 'X'
print hlstr(llx)
