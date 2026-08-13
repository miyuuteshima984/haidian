from pathlib import Path
from . import sprint_common as c
from . import sprint_v010


def _replace(path, old, new):
    p = Path(path)
    text = p.read_text(encoding='utf-8')
    if old in text:
        text = text.replace(old, new, 1)
    p.write_text(text, encoding='utf-8')


def _set_variant_json(path, variant):
    p = Path(path)
    if not p.is_file():
        return
    obj = c.readj(p)
    obj['variant'] = variant
    c.writej(p, obj)


def apply(pkg_path):
    # v0.11 is a meaningful continuation of the proven v0.7 design-first line:
    # keep v0.10's three public promises, then make one ordinary day the master
    # spatial test. AI must be removable at every step without breaking the loop.
    sprint_v010.apply(pkg_path)
    c.configure('v0.11', pkg_path)
    c.set_iteration()

    _replace(c.pkg/'proposal.md',
             '### v0.10｜DESIGN-FIRST + REALITY：现实资料只在改变空间时出现',
             '### v0.11｜JING-ZHANG DAILY LOOP：把完整城市做成一条日常闭环')
    _replace(c.pkg/'proposal.en.md',
             '### v0.10 | DESIGN-FIRST + REALITY: evidence appears only when it changes space',
             '### v0.11 | JING-ZHANG DAILY LOOP: make the complete city legible as one everyday loop')
    _replace(c.pkg/'proposal.md',
             'v0.10 以获得 86 分的 v0.7 **design-first** 结构为底座，只吸收会改变空间判断的现实锚点；主叙事仍从人的日常任务开始，而不是从证据目录或评分结构开始。',
             'v0.11 继续沿用获得 86 分的 v0.7 **design-first** 结构：把三条公共承诺串成一条普通人的日常城市闭环。现实资料仍只在改变空间判断时出现，AI 在每一步都只能是可关闭增强层。')
    _replace(c.pkg/'proposal.en.md',
             "v0.10 keeps the **design-first** hierarchy of the 86-point v0.7 baseline and absorbs only reality anchors that change a spatial decision; the story still starts with everyday public tasks, not evidence indexing or scoring structure.",
             "v0.11 continues the **design-first** hierarchy of the 86-point v0.7 baseline and connects the three public promises into one ordinary daily urban loop. Reality evidence still appears only where it changes space, and AI remains a switchable enhancement at every step.")

    for name in ['reference-plot-conditions.json', 'reality-constraint-register.json', 'public-promises-contract.json']:
        _set_variant_json(c.va/name, 'v0.11')

    loop = {
        'schema_version': '1.0',
        'variant': 'v0.11',
        'title_zh': '京张日常城市环 / JING-ZHANG DAILY LOOP',
        'status': 'concept_design_contract',
        'stage_count': 6,
        'sequence': [
            {
                'id': 'DL-01', 'stage': 'HOME / 家门',
                'ordinary_baseline': '可识别门址、普通步行出口、电话/纸质/人工服务入口',
                'optional_ai': '照护提醒、无障碍路径与服务匹配',
                'human_fallback': '不登录、不授权数据也可通过实体路径、电话或人工继续',
                'spatial_test': '离家第一步不依赖 App 或账号'
            },
            {
                'id': 'DL-02', 'stage': 'STREET / 街道',
                'ordinary_baseline': '连续人行、过街、遮阴坐凳、静态导视',
                'optional_ai': '动态无障碍/拥挤提示',
                'human_fallback': '实体导视和可见公共设施保持',
                'spatial_test': '设备关闭后仍能走、等、问路和休息'
            },
            {
                'id': 'DL-03', 'stage': 'GREEN CORRIDOR / 绿廊',
                'ordinary_baseline': '连续公共通行与停留界面优先',
                'optional_ai': '环境信息、维护提示与个性化路线',
                'human_fallback': '公共路径不因感知/物流/机器人模块中断',
                'spatial_test': 'AI/物流模块退后，不占连续公共通道'
            },
            {
                'id': 'DL-04', 'stage': 'STATION / 到达与换乘',
                'ordinary_baseline': '固定双语导视、连续无障碍到达、人工换乘帮助',
                'optional_ai': '动态多语信息与路径辅助',
                'human_fallback': '网络失效后回到实体导视与人工服务',
                'spatial_test': 'ARRIVE WITHOUT APP'
            },
            {
                'id': 'DL-05', 'stage': 'SERVICE · WORK · LEARN / 服务·工作·学习',
                'ordinary_baseline': '人工窗口、普通商业/服务、工作学习与公共客厅先成立',
                'optional_ai': '服务匹配、翻译、受控机器人/设备测试',
                'human_fallback': 'CARE WITHOUT ACCOUNT；测试停止不影响普通服务',
                'spatial_test': 'TEST WITHOUT BLOCKING'
            },
            {
                'id': 'DL-06', 'stage': 'RETURN / 返回',
                'ordinary_baseline': '用同一套实体城市底座回到社区与家门',
                'optional_ai': '可选回程辅助',
                'human_fallback': 'AI-OFF 时六步仍可闭合',
                'spatial_test': '一天不是单点 Demo；完整性必须在往返链上成立'
            }
        ],
        'acceptance_rule': 'AI-OFF is not an exception state: all six ordinary tasks must still form a complete daily loop.',
        'evidence_boundary': 'This is a concept-level spatial contract, not measured travel-time, field completion, official routing, approval or operational performance evidence.'
    }
    c.writej(c.va/'daily-loop-contract.json', loop)

    zh_cols = [
        ('1 家门 → 2 街道', [('HOME', '门址/实体出口/电话或人工入口先成立'), ('STREET', '人行、过街、遮阴坐凳、静态导视连续'), ('AI OFF', '不用 App 仍能离家、走路、休息、问路')], '#0f766e'),
        ('3 绿廊 → 4 站城', [('GREEN', '公共通行与停留优先，设备/物流退后'), ('STATION', '固定双语导视 + 无障碍到达 + 人工换乘'), ('AI OFF', '动态信息失效，实体路径和人工帮助仍在')], '#2563eb'),
        ('5 服务/工作/学习 → 6 返回', [('SERVICE', '人工窗口、普通服务、工作学习与公共客厅先成立'), ('RETURN', '同一实体底座完成回程，不把城市做成单点 Demo'), ('AI OFF', '六步仍闭合：NO APP · NO ACCOUNT · NO BLOCK')], '#b45309')
    ]
    en_cols = [
        ('1 HOME → 2 STREET', [('HOME', 'address, physical exit and phone/human entry work first'), ('STREET', 'walking, crossing, shade/seating and static wayfinding stay continuous'), ('AI OFF', 'leave home, walk, rest and ask without an app')], '#0f766e'),
        ('3 GREEN → 4 STATION', [('GREEN', 'public passage and staying come first; devices/logistics sit back'), ('STATION', 'fixed bilingual wayfinding + accessible arrival + staffed transfer'), ('AI OFF', 'physical route and people remain when dynamic information fails')], '#2563eb'),
        ('5 SERVICE/WORK/LEARN → 6 RETURN', [('SERVICE', 'staffed service, ordinary work/learning and commons work first'), ('RETURN', 'the same physical city base completes the trip home; not a one-point demo'), ('AI OFF', 'all six steps still close: NO APP · NO ACCOUNT · NO BLOCK')], '#b45309')
    ]
    (c.fig/'jingzhang-daily-loop.svg').write_text(
        c.svg_shell('v0.11｜JING-ZHANG DAILY LOOP', '家门 → 街道 → 绿廊 → 站城 → 服务/工作/学习 → 返回；AI-OFF 仍然闭合', zh_cols,
                    '这是日常空间验收合同，不是实测通勤时间、官方路线、审批或运营绩效证明。'), encoding='utf-8')
    (c.fig/'jingzhang-daily-loop.en.svg').write_text(
        c.svg_shell('v0.11 | JING-ZHANG DAILY LOOP', 'Home → street → green corridor → station → service/work/learn → return; the loop still closes in AI-OFF', en_cols,
                    'This is an everyday spatial acceptance contract, not measured travel time, official routing, approval or operating-performance evidence.'), encoding='utf-8')

    # Make one fixed Review Agent input carry the daily loop while preserving its
    # mobility/blue-green meaning instead of replacing it with a reviewer dashboard.
    c.save_png(c.fig/'mobility-bluegreen.png', '慢行与蓝绿系统｜京张日常城市环',
               '六步日常链把慢行、绿廊、站城和公共服务连成闭环；AI 只增强信息，不成为通行前提。', [
        ('HOME → STREET', '连续人行、过街、遮阴坐凳与静态导视先成立；不用 App 仍能离家、走路、停留和问路。', 'BASELINE'),
        ('GREEN → STATION', '绿廊公共通行与停留优先；固定双语导视、无障碍到达和人工换乘先于动态设备。', 'NO APP'),
        ('SERVICE → RETURN', '人工服务、工作学习和公共客厅可直接使用；测试停止不阻断普通任务，回程仍用同一实体底座。', 'AI OFF')],
               '路径为概念级任务链，不是官方线路、站口、工程线位或实测时耗；site/key-area geometry 仍为 provisional。')
    c.save_png(c.fig/'mobility-bluegreen.en.png', 'Mobility + blue-green system | Jing-Zhang Daily Loop',
               'Six everyday steps connect walking, green corridor, station-city arrival and public service; AI enhances information but is never a mobility precondition.', [
        ('HOME → STREET', 'Continuous walking, crossing, shade/seating and static wayfinding work first; leaving, walking, staying and asking do not require an app.', 'BASELINE'),
        ('GREEN → STATION', 'Public passage/staying on the green corridor come first; fixed bilingual wayfinding, accessible arrival and staffed transfer precede dynamic devices.', 'NO APP'),
        ('SERVICE → RETURN', 'Staffed service, work/learning and commons remain directly usable; stopping a test does not block ordinary tasks, and the physical base carries the trip home.', 'AI OFF')],
               'This is a concept task chain, not an official route, station exit, engineering alignment or measured travel time; site/key-area geometry remains provisional.')

    zh_start = '<!-- V011-DAILY-LOOP-START -->'
    zh_end = '<!-- V011-DAILY-LOOP-END -->'
    zh = f'''{zh_start}\n### v0.11｜京张日常城市环：不是六个 Demo，而是一整天仍能回家\n\n把 v0.10 的三条公共承诺再收紧成一条可追问的日常链：**家门 → 街道 → 绿廊 → 站城 → 服务/工作/学习 → 返回**。六步都先写普通城市底座，再写可选 AI、人工兜底与 AI-OFF；只有六步在 AI 关闭后仍能闭合，才算“城市完整”。[metric:daily_loop_stage_count]\n\n![京张日常城市环](assets/figures/jingzhang-daily-loop.svg)\n\n这条环不是官方线路、精确通勤时间或已实施服务证明。它把 ARRIVE WITHOUT APP、CARE WITHOUT ACCOUNT、TEST WITHOUT BLOCKING 从三个口号变成同一天里的连续空间验收问题。机器可读合同见 `visual/assets/daily-loop-contract.json`。\n{zh_end}'''
    c.upsert_before(c.pkg/'proposal.md', zh_start, zh_end, zh, '## 用地、建筑规模与拆改留方案')

    en_start = '<!-- V011-DAILY-LOOP-START -->'
    en_end = '<!-- V011-DAILY-LOOP-END -->'
    en = f'''{en_start}\n### v0.11 | Jing-Zhang Daily Loop: not six demos, but one whole day that can still get home\n\nv0.11 tightens the three public promises into one testable sequence: **home → street → green corridor → station → service/work/learn → return**. Every step states the ordinary-city baseline first, then optional AI, human fallback and AI-OFF. The city is complete only if all six steps still close when AI is off. [metric:daily_loop_stage_count]\n\n![Jing-Zhang Daily Loop](assets/figures/jingzhang-daily-loop.en.svg)\n\nThis is not an official route, measured travel time or proof of an implemented service. It turns ARRIVE WITHOUT APP, CARE WITHOUT ACCOUNT and TEST WITHOUT BLOCKING into continuous spatial acceptance questions within one ordinary day. The machine-readable contract is `visual/assets/daily-loop-contract.json`.\n{en_end}'''
    c.upsert_before(c.pkg/'proposal.en.md', en_start, en_end, en, '## Land Use, Building Capacity, and Retain-Renovate-Demolish Strategy')

    c.add_metric('daily_loop_stage_count', {
        'status': 'known', 'value': 6, 'unit': 'count',
        'source_files': ['visual/assets/daily-loop-contract.json', 'assets/figures/jingzhang-daily-loop.svg', 'assets/figures/mobility-bluegreen.png'],
        'formula': 'count(DL-01..DL-06)', 'confidence': 'high',
        'assumptions': ['Counts concept-design stages, not measured trips or completed field tests.']
    })
    c.manifest_add('visual/assets/daily-loop-contract.json', 'evidence_data')
    c.manifest_add('assets/figures/jingzhang-daily-loop.svg', 'illustration', 'zh')
    c.manifest_add('assets/figures/jingzhang-daily-loop.en.svg', 'illustration', 'en', 'assets/figures/jingzhang-daily-loop.svg')
    c.copyright_note('- `jingzhang-daily-loop*.svg`, rebuilt `mobility-bluegreen*.png`, and `visual/assets/daily-loop-contract.json`: submission-authored v0.11 design synthesis; no third-party visual asset embedded.')
    c.changelog('''## v0.11 - 2026-08-13\n\n- Continued the 86-point v0.7 design-first line and kept v0.10's three public promises.\n- Added the six-stage JING-ZHANG DAILY LOOP: home → street → green corridor → station → service/work/learn → return.\n- Required ordinary-city baseline, optional AI, human fallback and AI-OFF continuity at every stage; the loop must still close with AI off.\n- Rebuilt the fixed `mobility-bluegreen*.png` reviewer input around the everyday loop while preserving the reality-aware public-passage priority and provisional geometry boundary.''')

    for name in ['visual/index.html', 'visual/index.en.html']:
        p = c.pkg/name
        s = p.read_text(encoding='utf-8').replace('v0.10 design-first', 'v0.11 daily-loop design-first')
        p.write_text(s, encoding='utf-8')

    c.finalize_package(
        ('京张日常城市环', 'Jing-Zhang Daily Loop', 'jingzhang-daily-loop.svg'),
        'v011-daily-loop',
        'v0.11 首屏｜京张日常城市环',
        'v0.11 First screen | Jing-Zhang Daily Loop',
        'jingzhang-daily-loop.svg',
        'v0.11 daily-loop design-first'
    )
