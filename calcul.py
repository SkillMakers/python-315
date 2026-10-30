# Charge CPU pure : nombres premiers par divisions successives
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
    return c
t = time.perf_counter(); r = premiers(300_000); dt = time.perf_counter() - t
jit = sys._jit.is_enabled() if hasattr(sys, "_jit") else None
print(f"{sys.version.split()[0]} jit={jit} resultat={r} {dt:.2f} s")
