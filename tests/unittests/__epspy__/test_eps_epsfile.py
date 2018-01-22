## NOTE: THIS FILE IS GENERATED BY EPSCRIPT! DO NOT MODITY
from eudplib import *

def _IGVA(vList, exprListGen):
    def _():
        exprList = exprListGen()
        SetVariables(vList, exprList)
    EUDOnStart(_)

def _CGFW(exprf, retn):
    rets = [ExprProxy(None) for _ in range(retn)]
    def _():
        vals = exprf()
        for ret, val in zip(rets, vals):
            ret._value = val
    EUDOnStart(_)
    return rets

def _ARR(items):
    k = EUDArray(len(items))
    for i, item in enumerate(items):
        k[i] = item
    return k

def _SRET(v, klist):
    return List2Assignable([v[k] for k in klist])

def _SV(dL, sL):
    [d << s for d, s in zip(FlattenList(dL), FlattenList(sL))]

class _ATTW:
    def __init__(self, obj, attrName):
        self.obj = obj
        self.attrName = attrName
    def __lshift__(self, r):
        setattr(self.obj, self.attrName, r)

class _ARRW:
     def __init__(self, obj, index):
         self.obj = obj
         self.index = index
     def __lshift__(self, r):
         self.obj[self.index] = r

def _L2V(l):
    ret = EUDVariable()
    if EUDIf()(l):
        ret << 1
    if EUDElse()():
        ret << 0
    EUDEndIf()
    return ret

def _MVAR(vs):
    return List2Assignable([
        v.makeL() if IsEUDVariable(v) else EUDVariable() << v
        for v in FlattenList(vs)])

def _LSH(l, r):
    if IsEUDVariable(l):  return f_bitlshift(l, r)
    else: return l << r

## NOTE: THIS FILE IS GENERATED BY EPSCRIPT! DO NOT MODITY

# (Line 1) function square();
# (Line 3) const a = [
# (Line 4) square(1),
# (Line 5) square(2),
# (Line 6) square(3),
# (Line 7) square(4),
# (Line 8) square(5)
# (Line 9) ];
a = _CGFW(lambda: [_ARR(FlattenList([f_square(1), f_square(2), f_square(3), f_square(4), f_square(5)]))], 1)[0]
# (Line 11) function square(x) {
@EUDFunc
def f_square(x):
    # (Line 12) const z = EUDVArray(5)();
    z = EUDVArray(5)()
    # (Line 13) return x * x; // + z.k;
    EUDReturn(x * x)
    # (Line 14) }
    # (Line 16) function constv_thing() {

@EUDFunc
def f_constv_thing():
    # (Line 17) return a[0] + a[1] + a[2] + a[3] + a[4];
    EUDReturn(a[0] + a[1] + a[2] + a[3] + a[4])
    # (Line 18) }
