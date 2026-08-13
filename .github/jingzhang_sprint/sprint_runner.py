import sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
if str(HERE) not in sys.path: sys.path.insert(0,str(HERE.parent))
from jingzhang_sprint import sprint_v08, sprint_v09

if len(sys.argv)!=3:
    raise SystemExit('usage: sprint_runner.py <v0.8|v0.9> <package>')
variant,pkg=sys.argv[1:]
if variant=='v0.8': sprint_v08.apply(pkg)
elif variant=='v0.9': sprint_v09.apply(pkg)
else: raise SystemExit(f'unknown variant {variant}')
