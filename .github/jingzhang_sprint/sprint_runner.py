import sys, subprocess
from pathlib import Path
HERE=Path(__file__).resolve().parent
if str(HERE) not in sys.path: sys.path.insert(0,str(HERE.parent))
from jingzhang_sprint import sprint_common, sprint_v08, sprint_v09, sprint_v091, sprint_v010

_orig_upsert = sprint_common.upsert_before
def _robust_upsert(path,start,end,block,marker):
    text=Path(path).read_text(encoding='utf-8')
    if marker not in text and marker == '## Land Use, Building Capacity, and Retain-Renovate-Demolish Strategy':
        marker='## Land Use, Building Scale, and Retain-Renovate-Demolish Strategy'
    return _orig_upsert(path,start,end,block,marker)
sprint_common.upsert_before=_robust_upsert

_orig_matrix = sprint_common.update_matrices
def _exact_matrix(section,mids,sids=()):
    if section.startswith('v0.8 '): section='v0.8｜把六类接口收束成一个 1:1 城市原型：C7 CIVIC STATION'
    if section.startswith('v0.9 '): section='v0.9｜REALITY-ANCHORED：只有能改变空间判断的资料才进入主叙事'
    if section.startswith('v0.10 '): section='v0.10｜三条公共城市承诺：评委先看到城市怎么被人使用'
    return _orig_matrix(section,mids,sids)
sprint_common.update_matrices=_exact_matrix

_orig_manifest_add=sprint_common.manifest_add
def _schema_role_manifest_add(path,role,language=None,translation_of=None):
    role_map={
        'prototype_contract':'evidence_data',
        'field_observation_register':'evidence_data',
        'reality_constraint_register':'evidence_data',
        'reference_plot_conditions':'evidence_data',
    }
    return _orig_manifest_add(path,role_map.get(role,role),language,translation_of)
sprint_common.manifest_add=_schema_role_manifest_add

_orig_run=sprint_common.subprocess.run
def _verbose_run(args,*a,**kw):
    is_sc=isinstance(args,(list,tuple)) and any('self_check_submission.py' in str(x) for x in args)
    if not is_sc: return _orig_run(args,*a,**kw)
    opts=dict(kw); wanted=opts.pop('check',False)
    res=_orig_run(args,*a,check=False,**opts)
    print('SELF_CHECK_STDOUT_START')
    print(res.stdout or '')
    print('SELF_CHECK_STDOUT_END')
    print('SELF_CHECK_STDERR_START')
    print(res.stderr or '')
    print('SELF_CHECK_STDERR_END')
    if wanted and res.returncode:
        raise subprocess.CalledProcessError(res.returncode,args,output=res.stdout,stderr=res.stderr)
    return res
sprint_common.subprocess.run=_verbose_run

if len(sys.argv)!=3:
    raise SystemExit('usage: sprint_runner.py <v0.8|v0.9|v0.91|v0.10> <package>')
variant,pkg=sys.argv[1:]
if variant=='v0.8': sprint_v08.apply(pkg)
elif variant=='v0.9': sprint_v09.apply(pkg)
elif variant=='v0.91': sprint_v091.apply(pkg)
elif variant=='v0.10': sprint_v010.apply(pkg)
else: raise SystemExit(f'unknown variant {variant}')
