import subprocess, sys, time, statistics
py = sys.argv[1]; cmds = {"normal": [py, "outil_normal.py", "--version"], "lazy": [py, "outil_lazy.py", "--version"],
  "normal + -X lazy_imports=all": [py, "-X", "lazy_imports=all", "outil_normal.py", "--version"], "python vide": [py, "-c", "pass"]}
for k, c in cmds.items():
    subprocess.run(c, capture_output=True)
    t = []
    for _ in range(30):
        a = time.perf_counter(); subprocess.run(c, capture_output=True, check=True); t.append((time.perf_counter() - a) * 1000)
    print(f"{k:32} mediane {statistics.median(t):6.1f} ms  min {min(t):6.1f}")
