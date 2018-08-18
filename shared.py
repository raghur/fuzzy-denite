from ctypes import *

class GoString(Structure):
    _fields_ = [("p", c_char_p), ("n", c_longlong)]


class GoSlice(Structure):
    _fields_ = [("data", POINTER(c_void_p)), ("len", c_longlong), ("cap", c_longlong)]

lib = cdll.LoadLibrary("./fuzzy-denite.so")


s1 = GoString(c_char_p(b"hello"), 5)
s2 = GoString(c_char_p(b"world"), 5)

lib.Bar.restype = c_char_p
rv = lib.Bar(s1)

print("From go: ", rv)

# print(s1, s2)
# d = GoSlice((c_void_p * 2) (cast(pointer(s1), c_void_p), cast(pointer(s2),
#                                                                c_void_p)), 2, 2)
s3 = c_char_p(b"hello")
s4 = c_char_p(b"world")
d = GoSlice( (c_void_p * 2) (cast(s3, c_void_p), cast(s4, c_void_p)), 2, 2)

print(d)
lib.Foo.argtypes = [GoSlice, GoSlice]
lib.Foo.restype = c_longlong
rv = GoSlice( (c_void_p * 10)(None), 10, 10)
c = lib.Foo(d, rv)
print(c)
for i in range(0, c):
    # vptr = cast(r.data[i], POINTER(GoString))
    vptr = cast(rv.data[i], c_char_p)
    print(vptr.value)
    # v = vptr.contents
    # print(v.p)

