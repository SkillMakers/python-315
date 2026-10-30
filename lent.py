import json, time
def charger():
    return [{"id": i, "nom": f"client{i}"} for i in range(300_000)]
def valider(clients):
    return [c for c in clients if c["nom"].startswith("client")]
def exporter(clients):
    return json.dumps(clients)
def attendre():
    time.sleep(1.0)
c = charger(); v = valider(c); attendre(); exporter(v)
