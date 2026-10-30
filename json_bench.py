import json, time, sys
data = [{"id": i, "nom": f"client{i}", "ville": "Lyon", "total": i * 1.5} for i in range(2000)]
t = time.perf_counter()
for _ in range(150): json.loads(json.dumps(data))
print(f"jit={sys._jit.is_enabled()} json {time.perf_counter()-t:.2f} s")
