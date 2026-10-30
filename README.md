# Python 3.15 : les nouveautés — le banc d'essai de la vidéo

Les scripts de la vidéo **ItSkillsMaker** « Python 3.15 : les nouveautés expliquées (et ce qui casse) » :
👉 https://youtu.be/USvD92hHtTE

Chaque chiffre de la vidéo vient de ces scripts. Les résultats complets, avec la machine et les versions,
sont dans [MESURES.md](MESURES.md).

## Les scripts

| Sujet | Scripts |
|---|---|
| UTF-8 par défaut (PEP 686) : ce qui casse | `ecrire_311.py` (écrit `clients.csv` en cp1252), `lire.py`, `ecrire_lire_315.py`, `lire_rapport.py` |
| Lazy imports (PEP 810) | `outil_normal.py`, `outil_lazy.py`, `chrono.py` (30 lancements, médiane), `piege_lazy.py`, `lazy_fonction.py`, `lazy_try.py` |
| Profileur `profiling.sampling` | `lent.py` |
| JIT et free-threading | `calcul.py`, `calcul_lib.py`, `threads.py`, `json_bench.py` |
| Messages d'erreur | `e.py` |

## Lancer

Il faut Python 3.15 (et 3.15t, la version sans GIL, pour `threads.py`). Sous Windows avec le gestionnaire `py` :

```bash
py install 3.15
py -3.15 outil_lazy.py --version
py -3.15 chrono.py python3.15     # compare import normal et lazy import (argument : la commande du Python a mesurer, ex. le chemin de python.exe)
py -3.15 piege_lazy.py         # l'erreur tombe a la premiere utilisation, pas au demarrage
```

Pour le piège de l'encodage, il faut une version avant 3.15 sous Windows : `py -3.11 ecrire_311.py` puis `py -3.15 lire.py`.
