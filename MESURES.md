# Banc Python 3.15 — mesures du 2026-10-24

Machine : Windows 11, 8 cœurs logiques. Pythons : **3.15.1** (`pymanager install 3.15`, build du 21/10/2026),
**3.15.1 free-threaded** (`pymanager install 3.15t`), **3.11.9** (la 3.14 installée est cassée sur cette
machine, d'où la comparaison avec 3.11 ; sur l'encodage, toutes les versions avant 3.15 se comportent pareil).
Scripts dans ce dossier. `PYTHONIOENCODING=utf-8` pour l'affichage.

## UTF-8 par défaut (PEP 686)

| Test | Résultat |
|---|---|
| `locale.getpreferredencoding(False)` sous 3.11 | `cp1252` |
| 3.15 : `sys.flags.utf8_mode` / `locale.getencoding()` | `1` / `cp1252` |
| `clients.csv` écrit par 3.11 sans `encoding=` (`Hélène;Besançon`) puis lu par 3.11 | correct |
| … lu par **3.15** | **`UnicodeDecodeError: 'utf-8' codec can't decode byte 0xe9 in position 12: invalid continuation byte`** |
| … `csv.reader` sous 3.15 | même `UnicodeDecodeError` |
| … 3.15 avec `-X utf8=0` | correct |
| … 3.15 avec `encoding="locale"` | correct |
| `rapport.txt` écrit par **3.15** (`Total : 1 250 € — validé`) lu par 3.11 | **`'Total : 1 250 â‚¬ â€” validÃ©'`**, sans aucune erreur |
| 3.11 `-X warn_default_encoding` | `EncodingWarning: 'encoding' argument not specified`, avec fichier et ligne |

## Lazy imports (PEP 810)

Outil en ligne de commande qui importe 12 modules (`asyncio json argparse logging sqlite3 csv decimal
http.client urllib.request email.mime.multipart xml.dom.minidom unittest`) et ne fait que `--version`.
30 lancements, médiane :

| Variante | Médiane | Min |
|---|---|---|
| `import` normal | **614,5 ms** | 540,3 |
| `lazy import` | **95,2 ms** | 78,7 |
| normal + `-X lazy_imports=all` | 94,2 ms | 84,8 |
| `python -c pass` (Python vide) | 96,4 ms | 82,7 |

`-X importtime` : 240 modules chargés en normal, 29 en lazy.
Pièges vérifiés : `lazy import modul_inexistant` → le programme démarre et affiche, l'erreur
`ModuleNotFoundError` tombe **à la première utilisation**, dans la fonction ;
`SyntaxError: lazy import not allowed inside functions` ; `… not allowed inside try/except blocks`.

## frozendict, sentinel, compréhensions, erreurs, strptime

- `frozendict(host="localhost", port=5432)` : `isinstance(cfg, dict)` → **False** ; hashable (clé de dict OK,
  ordre des clés indifférent) ; `cfg["port"] = 1` → `TypeError: 'frozendict' object does not support item
  assignment` ; `cfg | {"port": 6543}` → nouveau `frozendict`.
- `json.loads(..., object_pairs_hook=frozendict, array_hook=tuple)` → `frozendict({'a': (1, 2)})`.
- `MISSING = sentinel("MISSING")` : repr `MISSING`, identité conservée par `copy.deepcopy`, vrai en booléen.
- `[*L for L in [[1, 2], [3, 4], [5]]]` → `[1, 2, 3, 4, 5]` ; `{**d for d in dicts}` → `{'a': 3, 'b': 2}`.
- Messages (3.15 / 3.11) : `.push` → `Did you mean '.append'?` ; `{}.put` → `Use d[k] = v.` ;
  `'abc'.toUpperCase()` → `Did you mean '.upper'?` ; `O().area` → `Did you mean '.inner.area' instead of '.area'?`.
  3.11 : message nu à chaque fois.
- `datetime.strptime("15/03", "%d/%m")` : 3.11 → `1900-03-15 00:00:00` ; 3.15 → **`ValueError: Day of month
  directive '%d' may not be used without a year directive. …`**.
- `re.prefixmatch(r"\d+", "42 ans")` → match `'42'`.

## Profileur `profiling.sampling` (Tachyon)

`python -m profiling.sampling run lent.py` (charger 300 000 dicts, filtrer, `sleep(1)`, `json.dumps`) :
2 164 échantillons en 2,16 s, ~1 000 échantillons/s. `attendre` 54,1 %, `charger` 25,5 %,
`JSONEncoder.iterencode` 16,6 %, `valider` 3,4 %. Sous-commandes : `run`, `attach <PID>`, `dump <PID>`,
`replay` ; `--live`.

## JIT et free-threading

Boucle CPU pure (nombres premiers < 300 000, 3 lancements) :

| Python | Temps |
|---|---|
| 3.11.9 | 3,76 · 3,13 · 3,05 s |
| 3.15.1, JIT désactivé (défaut) | 2,43 · 1,64 · 1,70 s |
| 3.15.1, `PYTHON_JIT=1` | **1,00 · 0,99 · 0,94 s** |
| 3.15.1t (sans GIL), 1 thread | 1,78 s |

`sys._jit.is_available()` → True sur le binaire Windows officiel ; `is_enabled()` → False par défaut.
Charge `json.dumps/loads` (150 × 2 000 objets) : 1,08 / 1,07 s et 1,19 / 1,21 s, **aucun gain du JIT**
(le travail est dans le code C de `json`).
Doc officielle : +7-8 % en moyenne géométrique (pyperformance, x86-64 Linux), de −15 % à +100 % selon le cas.

4 calculs (premiers < 150 000), séquentiel puis 4 threads :

| Build | Séquentiel | 4 threads | Gain |
|---|---|---|---|
| 3.15.1 (GIL) | 2,42 / 2,50 s | 2,41 / 2,41 s | ×1,01 / ×1,03 |
| 3.15.1t (sans GIL) | 2,47 / 2,50 s | 1,28 / 1,21 s | **×1,93 / ×2,07** |
