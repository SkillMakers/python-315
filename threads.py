import sys, time
from concurrent.futures import ThreadPoolExecutor
from calcul_lib import premiers
N = 4
t = time.perf_counter(); [premiers(150_000) for _ in range(N)]; seq = time.perf_counter() - t
t = time.perf_counter()
with ThreadPoolExecutor(N) as ex: list(ex.map(premiers, [150_000]*N))
par = time.perf_counter() - t
gil = sys._is_gil_enabled() if hasattr(sys, "_is_gil_enabled") else True
print(f"{sys.version.split()[0]} gil={gil} sequentiel {seq:.2f} s  4 threads {par:.2f} s  gain x{seq/par:.2f}")
