
Serialization protocol:

32bit int: "i" + four bytes of integer
bytestring: "s" + four bytes of length + string contents
list: "l" + four bytes of length + put together items one after another
dict: "d" + four bytes of length + put together interwinded key and value

no unicode, we're in the 90s
