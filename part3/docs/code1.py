
""" This is calling things directly, but we can as well
translate it down to direct C calls
"""

from rpython.rtyper.lltypesystem import lltype, rffi

S = lltype.GcStruct('foo', ('x', lltype.Signed), ('y', lltype.Float))
s = lltype.malloc(S)
s.x = 13

CA = rffi.CArray(lltype.Signed) # CArray, no length known
ca = lltype.malloc(CA, 13, flavor='raw')
ca[5] = 13
print ca
# we don't know the length
