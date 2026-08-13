from pathlib import Path
from . import sprint_common as c
from . import sprint_v09


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
    # Start from the v0.7 package baseline in the workflow, add the useful reality
    # anchors from v0.9, then restore a design-first hierarchy for v0.10.
    sprint_v09.apply(pkg_path)
    c.configure('v0.10', pkg_path)
    c.set_iteration()

    _replace(c.pkg/'proposal.md', '### v0.9｜REALITY-ANCHORED：只有能改变空间判断的资料才进入主叙事',
             '### v0.10｜DESIGN-FIRST + REALITY：现实资料只在改变空间时出现')
    _replace(c.pkg/'proposal.en.md', '### v0.9 | REALITY-ANCHORED: a source enters the design story only if it changes a spatial decision',
             '### v0.10 | DESIGN-FIRST + REALITY: evidence appears only when it changes space')
    _replace(c.pkg/'proposal.md', 'v0.9 是从 v0.7 exact head 分出的 **reality-anchored 并行候选**，不继承 v0.8 的原型收束实验。',
             'v0.10 以获得 86 分的 v0.7 **design-first** 结构为底座，只吸收会改变空间判断的现实锚点；主叙事仍从人的日常任务开始，而不是从证据目录或评分结构开始。')
    _replace(c.pkg/'proposal.en.md', 'v0.9 is a **reality-anchored parallel candidate** branched independently from the v0.7 exact head; it does not inherit the v0.8 prototype-convergence experiment.',
             'v0.10 keeps the **design-first** hierarchy of the 86-point v0.7 baseline and absorbs only reality anchors that change a spatial decision; the story still starts with everyday public tasks, not evidence indexing or scoring structure.')

    for name in ['reference-plot-conditions.json', 'reality-constraint-register.json']:
        _set_variant_json(c.va/name, 'v0.10')

    promises = {
        'schema_version': '1.0',
        'variant': 'v0.10',
        'title_zh': '三条公共城市承诺 / THREE PUBLIC PROMISES',
        'status': 'concept_design_contract',
        'promises': [
            {
                'id': 'PP-01', 'name': 'ARRIVE WITHOUT APP', 'place': '大钟寺 / station-city arrival',
                'ordinary_baseline': '固定双语导视 + 连续步行/无障碍 + 人工换乘帮助',
                'spatial_move': '到达界面清晰、可停留、有人可问；动态设备不占基本路径',
                'optional_ai': '动态多语信息与路径辅助',
                'failure_recovery': 'AI/网络失效后回到实体导视与人工服务',
                'reality_rule': '铁路/道路节点按真实竖向条件分别处理，不用一条通用缝合线代替专业判断'
            },
            {
                'id': 'PP-02', 'name': 'CARE WITHOUT ACCOUNT', 'place': 'AI 原点 / long-term community',
                'ordinary_baseline': '家门—遮阴坐凳—人工照护/服务—公共客厅',
                'spatial_move': '无手机、无账号、拒绝数据处理仍能完成基本照护与公共生活任务',
                'optional_ai': '导航、服务匹配与多语辅助',
                'failure_recovery': '人工窗口、电话/纸质入口和实体路径保持',
                'reality_rule': '京张绿廊侧先保证连续步行、停留与公共首层，设备/物流退后'
            },
            {
                'id': 'PP-03', 'name': 'TEST WITHOUT BLOCKING', 'place': '众智园 / innovation campus',
                'ordinary_baseline': '研究、服务劳动、吃饭休息与普通步行路线先连续',
                'spatial_move': '受控测试口袋与普通公共通行物理分离，可关闭、可撤除',
                'optional_ai': '机器人/设备受控测试与服务辅助',
                'failure_recovery': '测试停止不影响普通通行与基本服务',
                'reality_rule': '公开 FAR/高度只作现实量级参照，不成为提高本案强度或测试扩张的依据'
            }
        ],
        'principle': 'The three promises are memorable public-space tests. AI may enhance them but may not become a precondition for the ordinary task.'
    }
    c.writej(c.va/'public-promises-contract.json', promises)

    zh_cols = [
        ('ARRIVE WITHOUT APP', [('普通城市', '固定双语导视 + 人工换乘 + 连续到达'), ('空间', '站城首层可读、可停留、有人可问'), ('AI OFF', '动态信息失效仍完成到达任务')], '#0f766e'),
        ('CARE WITHOUT ACCOUNT', [('普通城市', '家门 → 遮阴坐凳 → 人工照护 → 公共客厅'), ('空间', '无手机/无账号不降低基本服务'), ('AI OFF', '电话/纸质/人工与实体路径继续工作')], '#2563eb'),
        ('TEST WITHOUT BLOCKING', [('普通城市', '研究/服务/休息/步行路线先连续'), ('空间', '测试口袋与公共通行物理分离'), ('STOP', '测试可关可撤，不占普通城市底座')], '#b45309')
    ]
    en_cols = [
        ('ARRIVE WITHOUT APP', [('Ordinary city', 'fixed bilingual wayfinding + staffed transfer + continuous arrival'), ('Space', 'legible, stayable station-city ground level with a person to ask'), ('AI OFF', 'arrival still works when dynamic information fails')], '#0f766e'),
        ('CARE WITHOUT ACCOUNT', [('Ordinary city', 'home → shade/seating → staffed care → commons'), ('Space', 'no phone/account does not reduce basic service'), ('AI OFF', 'phone/paper/human entry and physical routes remain')], '#2563eb'),
        ('TEST WITHOUT BLOCKING', [('Ordinary city', 'research/work/service/rest/walking stay continuous'), ('Space', 'test pocket is physically separate from public passage'), ('STOP', 'test can close/remove without taking the city base with it')], '#b45309')
    ]
    (c.fig/'three-public-promises.svg').write_text(
        c.svg_shell('v0.10｜三条公共城市承诺', '先把城市任务做成，再让 AI 成为可关闭增强层', zh_cols,
                    '三条承诺是城市设计验收问题，不是营销口号；真实位置、尺寸、工程与许可仍待现场和专业阶段核实。'), encoding='utf-8')
    (c.fig/'three-public-promises.en.svg').write_text(
        c.svg_shell('v0.10 | THREE PUBLIC PROMISES', 'Make the ordinary urban task work first; AI remains a switchable enhancement', en_cols,
                    'These are urban-design acceptance questions, not marketing claims; real location, dimensions, engineering and permits remain pending field/professional verification.'), encoding='utf-8')

    # Rebuild a fixed Review Agent input so the first multimodal packet sees the
    # three human tasks directly, while the detailed v0.7 key-area sections stay intact.
    c.save_png(c.fig/'site-overview.png', '总体范围｜三条公共承诺检查“一脊、六段、六缝、三核”',
               '固定 reviewer 输入：总体结构不是抽象线网，而要让到达、照护、测试三类普通城市任务在 AI-OFF 状态仍成立。', [
        ('南段 / 大钟寺｜ARRIVE', '固定双语导视、连续到达、人工换乘和可停留首层先成立；铁路/道路节点按真实竖向条件分别处理。', 'NO APP'),
        ('中段 / AI 原点｜CARE', '家门—遮阴坐凳—人工照护—公共客厅先成立；绿廊连续步行与公共首层优先，设备退后。', 'NO ACCOUNT'),
        ('北段 / 众智园｜TEST', '研发、服务劳动、吃饭休息和普通步行路线先连续；受控测试与公共通行物理分离。', 'NO BLOCK')],
               'site/key-area geometry 仍为 provisional；图示表达空间任务与优先级，不是官方红线、站口或工程线位。')
    c.save_png(c.fig/'site-overview.en.png', 'Overall scope | Three public promises test the spine, six segments, six stitches and three cores',
               'Fixed reviewer input: the overall structure must let arrival, care and testing work as ordinary urban tasks even in AI-OFF mode.', [
        ('South / Dazhongsi | ARRIVE', 'Fixed bilingual wayfinding, continuous arrival, staffed transfer and a stayable ground level work first; rail/road nodes follow real vertical conditions.', 'NO APP'),
        ('Middle / AI Origin | CARE', 'Home, shade/seating, staffed care and commons work first; continuous green-corridor walking and public frontage take priority over devices.', 'NO ACCOUNT'),
        ('North / Zhongzhiyuan | TEST', 'R&D, service work, meals, rest and ordinary walking remain continuous; controlled testing is physically separate from public passage.', 'NO BLOCK')],
               'Site/key-area geometry remains provisional; this shows spatial tasks and priorities, not official redlines, station exits or engineering alignments.')

    zh_start = '<!-- V010-PROMISES-START -->'
    zh_end = '<!-- V010-PROMISES-END -->'
    zh = f'''{zh_start}\n### v0.10｜三条公共城市承诺：评委先看到城市怎么被人使用\n\nv0.10 不把 v0.7 的设计优先路线改回“证据仪表盘”。它把三处重点区压缩成三个任何人都能追问的空间承诺：**ARRIVE WITHOUT APP、CARE WITHOUT ACCOUNT、TEST WITHOUT BLOCKING**。每条承诺都必须有普通城市底座、明确空间动作、可选 AI、失败恢复和现实约束；任一项缺失，就不算完整。[metric:public_promise_count]\n\n![三条公共城市承诺](assets/figures/three-public-promises.svg)\n\n机器可读合同见 `visual/assets/public-promises-contract.json`。它不是现场达标证明，也不把公开地块强度、控规草案或绿廊个案升级成本案审批条件；它只把这些现实资料放在真正会改变空间判断的位置。\n{zh_end}'''
    c.upsert_before(c.pkg/'proposal.md', zh_start, zh_end, zh, '## 用地、建筑规模与拆改留方案')

    en_start = '<!-- V010-PROMISES-START -->'
    en_end = '<!-- V010-PROMISES-END -->'
    en = f'''{en_start}\n### v0.10 | Three public promises: show how people use the city before showing evidence machinery\n\nv0.10 keeps v0.7's design-first hierarchy and compresses the three key areas into three questions anyone can test: **ARRIVE WITHOUT APP, CARE WITHOUT ACCOUNT, TEST WITHOUT BLOCKING**. Each promise requires an ordinary-city baseline, a spatial move, optional AI, failure recovery and a reality constraint. If one is missing, the urban task is not complete. [metric:public_promise_count]\n\n![Three public promises](assets/figures/three-public-promises.en.svg)\n\nThe machine-readable contract is `visual/assets/public-promises-contract.json`. It is not field evidence and does not upgrade public plot conditions, draft-plan material or a green-corridor case into proposal approvals; those sources appear only where they change a spatial decision.\n{en_end}'''
    c.upsert_before(c.pkg/'proposal.en.md', en_start, en_end, en, '## Land Use, Building Capacity, and Retain-Renovate-Demolish Strategy')

    c.add_metric('public_promise_count', {
        'status': 'known', 'value': 3, 'unit': 'count',
        'source_files': ['visual/assets/public-promises-contract.json', 'assets/figures/three-public-promises.svg', 'assets/figures/site-overview.png'],
        'formula': 'count(PP-01..PP-03)', 'confidence': 'high',
        'assumptions': ['Counts concept design promises, not completed field tests.']
    })
    c.manifest_add('visual/assets/public-promises-contract.json', 'evidence_data')
    c.manifest_add('assets/figures/three-public-promises.svg', 'illustration', 'zh')
    c.manifest_add('assets/figures/three-public-promises.en.svg', 'illustration', 'en', 'assets/figures/three-public-promises.svg')
    c.copyright_note('- `three-public-promises*.svg`, rebuilt `site-overview*.png`, and `visual/assets/public-promises-contract.json`: submission-authored v0.10 design synthesis; no third-party visual asset embedded.')
    c.changelog('''## v0.10 - 2026-08-13\n\n- Returned to the 86-point v0.7 design-first package baseline, then absorbed only the v0.9 reality anchors that materially change spatial decisions.\n- Added three memorable public-space promises: ARRIVE WITHOUT APP, CARE WITHOUT ACCOUNT, and TEST WITHOUT BLOCKING.\n- Rebuilt the fixed `site-overview*.png` reviewer input so the overall structure is read through ordinary urban tasks and AI-OFF recovery rather than a reviewer-facing dashboard.\n- Kept the v0.7 key-area spatial sections, added reality-aware mobility logic, and preserved all provisional/unknown statutory boundaries.''')

    c.finalize_package(
        ('三条公共城市承诺', 'Three public promises', 'three-public-promises.svg'),
        'v010-public-promises',
        'v0.10 首屏｜三条公共城市承诺',
        'v0.10 First screen | Three public promises',
        'three-public-promises.svg',
        'v0.10 design-first'
    )
