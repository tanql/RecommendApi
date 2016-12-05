import math
def average(x):
    if len(x) > 0:
        return float(sum(x)) / len(x)
    else:
        return False
def pearson(x, y):
    assert len(x) == len(y)
    n = len(x)
    assert n > 0
    if x == y:
        return 1
    avg_x = average(x)
    avg_y = average(y)
    diffprod = 0
    xdiff2 = 0
    ydiff2 = 0

    for idx in range(n):
        xdiff = x[idx] - avg_x
        ydiff = y[idx] - avg_y

        diffprod += xdiff * ydiff
        xdiff2 += xdiff * xdiff
        ydiff2 += ydiff * ydiff
    if math.sqrt(xdiff2 * ydiff2)==0:
        return 0
    else:
        return diffprod / math.sqrt(xdiff2 * ydiff2)