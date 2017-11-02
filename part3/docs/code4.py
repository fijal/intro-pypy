from rpython.rtyper.lltypesystem import lltype, rffi, llmemory
from rpython.rlib.rgc import pin, unpin
from rpython.rtyper.annlowlevel import llstr
from rpython.rtyper.lltypesystem.rstr import STR
from rpython.rlib.objectmodel import keepalive_until_here

from cffi import FFI

ffi = FFI()

s = "foo"
if pin(s): # will always succeed untranslated
    print "pinned"
    ll_s = llstr(s) # does not make a copy - just different types, same
    # data, if translated
    adr = llmemory.cast_ptr_to_adr(ll_s)
    adr = adr + llmemory.offsetof(STR, 'chars') + llmemory.itemoffsetof(STR.chars)
    i = rffi.cast(lltype.Signed, adr) # hard cast to int - only low level

    # for test only
    print repr(ffi.string(ffi.cast("char*", i)))
    # end of test

    keepalive_until_here(s) # probably unpin would keep it alive, but better safe then sorry
    unpin(s)
else:
    # do a copy anyway
    pass
