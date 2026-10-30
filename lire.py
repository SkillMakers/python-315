import sys
print(sys.version.split()[0])
try:
    print(open("clients.csv").read())
except Exception as e:
    print(type(e).__name__, ":", e)
