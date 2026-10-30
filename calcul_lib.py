import sys, time
def premiers(n):
    c = 0
    for k in range(2, n):
        d = 2
        while d * d <= k:
            if k % d == 0: break
            d += 1
        else:
            c += 1
