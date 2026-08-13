import sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
if str(HERE) not in sys.path: sys.path.insert(0,str(HERE.parent))
from jingzhang_sprint import sprint_common, sprint_v08, sprint_v09

_orig_upsert = sprint_common.upsert_before
def _robust_upsert(path,start,end,block,marker):
    text=Path(path).read_text(encoding='utf-8')
    if marker not in text and marker == '## Land Use, Building Capacity, and Retain-Renovate-Demolish Strategy':
        marker='## Land Use, Building Scale, and Retain-Renovate-Demolish Strategy'
    return _orig_upsert(path,start,end,block,marker)
sprint_common.upsert_before=_robust_upsert

if len(sys.argv)!=3:
    raise SystemExit('usage: sprint_runner.py <v0.8|v0.9> <package>')
variant,pkg=sys.argv[1:]
if variant=='v0.8': sprint_v08.apply(pkg)
elif variant=='v0.9': sprint_v09.apply(pkg)
else: raise SystemExit(f'unknown variant {variant}')
