from pycsp3 import *

n = 10
x = VarArray(size=n, dom=range(n))
satisfy(
    Cardinality(x, occurrences={i: x[i] for i in range(n)}),
    [
        Sum(x) == n,
        Sum((i - 1) * x[i] for i in range(n)) == 0
    ]
)
