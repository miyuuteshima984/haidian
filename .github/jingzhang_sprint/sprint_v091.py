from pathlib import Path
from . import sprint_common as c


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
    c.configure('v0.91', pkg_path)
    c.set_iteration()

    # v0.91 is a fresh-PR repair of the reality-anchored line, with one design
    # improvement: reality constraints are tied back to public user journeys.
    _replace(c.pkg/'proposal.md', '### v0.9｜REALITY-ANCHORED：只有能改变空间判断的资料才进入主叙事',
             '### v0.91｜REALITY-ANCHORED：只有能改变空间判断的资料才进入主叙事')
    _replace(c.pkg/'proposal.en.md', '### v0.9 | REALITY-ANCHORED: a source enters the design story only if it changes a spatial decision',
             '### v0.91 | REALITY-ANCHORED: a source enters the design story only if it changes a spatial decision')
    _replace(c.pkg/'proposal.md', 'v0.9 是从 v0.7 exact head 分出的 **reality-anchored 并行候选**，不继承 v0.8 的原型收束实验。',
             'v0.91 延续 v0.9 的 **reality-anchored** 设计线，并把现实约束进一步接回普通人的城市任务；它不把来源数量当成设计质量。')
    _replace(c.pkg/'proposal.en.md', 'v0.9 is a **reality-anchored parallel candidate** branched independently from the v0.7 exact head; it does not inherit the v0.8 prototype-convergence experiment.',
             'v0.91 continues the **reality-anchored** design line and ties each constraint back to an ordinary public task; source count is not treated as design quality.')

    for name in ['reference-plot-conditions.json', 'reality-constraint-register.json']:
        _set_variant_json(c.va/name, 'v0.91')

    bridge = {
        'schema_version': '1.0',
        'variant': 'v0.91',
        'title_zh': '现实约束 → 公共任务 → 空间响应',
        'status': 'design_contract_not_field_result',
        'chains': [
            {
                'id': 'RJ-01',
                'public_task': '跨铁路/到达连续性',
                'reality_anchor': '知春路相关铁路节点存在下穿、不可按通用平交理解的公开约束',
                'spatial_response': '相关缝合表达为竖向连续性待解节点；不虚构桥隧线位',
                'ai_role': '仅可选路径辅助；失效后实体导视与人工帮助仍成竉',
                'boundary': '不声称工程可行性、道路红线或站口位置'
            },
            {
                'id': 'RJ-02',
                'public_task': '沿京张绿廊连续步行与停留',
                'reality_anchor': '官方公开材料要求相关更新界面与京张绿廊衔接并提升空间品质',
                'spatial_response': '连续步行、可停留界面与公共首层优先；设备/物流退后',
                'ai_role': '环境与服务信息可选叠加；不得切断公共通行',
                'boundary': '不外推个案地块控制或产权关系'
            },
            {
                'id': 'RJ-03',
                'public_task': '在真实城市强度下维持日常完整度',
                'reality_anchor': '7 个公开规划条件地块仅提供现实 FAR/高度量级参照',
                'spatial_response': '朼案 approved_* 保持 unknown；概念容量不套用相邻样本',
                'ai_role': 'AI 不成为提高开发强度的理由',
                'boundary': '参照值不是本案控制值'
            }
        ],
        'principle': 'A reality anchor is useful only when it changes a public task or spatial decision without fabricating site facts.'
    }
    c.writej(c.va/'reality-to-public-task-register.json', bridge)

    zh_cols = [
        ('到达不是一条蓝线', [('现实', '下穿条件 → 竖向连续性待解'), ('空间', '实体导视 + 人工帮助先成立'), ('AI', '仅可选路径辅助；失效可退出')], '#0f766e'),
        ('绿廊首先是公共空间', [('现实', '更新界面需与京张绿廊衔接'), ('空间', '连续步行 + 停留 + 公共首层优先'), ('AI/物流', '退到不切断公共通行的位置')], '#2563eb'),
        ('强度参照不是控制值', [('现实', '7 个地块只给量级标尺'), ('空间', '概念容量服从普通城市完整度'), ('边界', 'approved FAR/height 继续 unknown')], '#b45309')
    ]
    en_cols = [
        ('Arrival is not one blue line', [('Reality', 'underpass condition → vertical continuity unresolved'), ('Space', 'fixed wayfinding + staffed help first'), ('AI', 'optional route help; physical fallback remains')], '#0f766e'),
        ('The green corridor is public space first', [('Reality', 'renewal frontage must relate to the green corridor'), ('Space', 'continuous walking + staying + public frontage'), ('AI/logistics', 'sit behind uninterrupted public passage')], '#2563eb'),
        ('Reference intensity is not a control', [('Reality', '7 plots provide scale references only'), ('Space', 'concept capacity serves ordinary city completeness'), ('Boundary', 'approved FAR/height remain unknown')], '#b45309')
    ]
    (c.fig/'reality-to-public-task.svg').write_text(
        c.svg_shell('v0.91｜现实资料必须回到公共任务', '现实约束 → 普通人的任务 → 空间响应 → 可选 AI / 退出', zh_cols,
                    '设计合同，不是现场绩效；不新增官方红线、工程线位、批准强度或机构承诺。'), encoding='utf-8')
    (c.fig/'reality-to-public-task.en.svg').write_text(
        c.svg_shell('v0.91 | Reality evidence must return to a public task', 'reality constraint → ordinary task → spatial response → optional AI / exit', en_cols,
                    'Design contract only; no field performance, official redline, engineering alignment, approved intensity or institutional commitment is claimed.'), encoding='utf-8')

    zh_start = '<!-- V091-PUBLIC-TASK-START -->'
    zh_end = '<!-- V091-PUBLIC-TASK-END -->'
    zh = f'''{zh_start}\n### v0.91｜把现实约束接回普通人的城市任务\n\n这一小步不增加“评审索引”。它只检查三件事：**到达能不能在 AI 失效时继续、绿廊是不是先服务步行与停留、现实强度参照有没有被误写成本案控制值。** 三条链记录于 `visual/assets/reality-to-public-task-register.json`；每条都同时写出普通任务、空间响应、可选 AI 和不可越界的事实边界。[metric:reality_public_task_bridge_count]\n\n![现实约束必须回到公共任务](assets/figures/reality-to-public-task.svg)\n{zh_end}'''
    c.upsert_before(c.pkg/'proposal.md', zh_start, zh_end, zh, '## 用地、建筑规模与拆改留方案')

    en_start = '<!-- V091-PUBLIC-TASK-START -->'
    en_end = '<!-- V091-PUBLIC-TASK-END -->'
    en = f'''{en_start}\n### v0.91 | Tie reality constraints back to ordinary public tasks\n\nThis small revision adds no reviewer dashboard. It tests only three things: **arrival still works when AI fails; the green corridor serves walking and staying before devices; and reality-scale references are not rewritten as proposal controls.** The three chains are machine-readable in `visual/assets/reality-to-public-task-register.json`, each with an ordinary task, spatial response, optional AI and a fact boundary. [metric:reality_public_task_bridge_count]\n\n![Reality constraints must return to public tasks](assets/figures/reality-to-public-task.en.svg)\n{en_end}'''
    c.upsert_before(c.pkg/'proposal.en.md', en_start, en_end, en, '## Land Use, Building Capacity, and Retain-Renovate-Demolish Strategy')

    c.add_metric('reality_public_task_bridge_count', {
        'status': 'known', 'value': 3, 'unit': 'count',
        'source_files': ['visual/assets/reality-to-public-task-register.json', 'assets/figures/reality-to-public-task.svg'],
        'formula': 'count(RJ-01..RJ-03)', 'confidence': 'high',
        'assumptions': ['Counts design-response chains, not completed field observations.']
    })
    c.manifest_add('visual/assets/reality-to-public-task-register.json', 'evidence_data')
    c.manifest_add('assets/figures/reality-to-public-task.svg', 'illustration', 'zh')
    c.manifest_add('assets/figures/reality-to-public-task.en.svg', 'illustration', 'en', 'assets/figures/reality-to-public-task.svg')
    c.copyright_note('- `reality-to-public-task*.svg` and `visual/assets/reality-to-public-task-register.json`: submission-authored v0.91 design synthesis; no third-party visual asset embedded.')
    c.changelog('''## v0.91 - 2026-08-13\n\n- Reissued the reality-anchored line on a fresh PR lifecycle after the prior PR review state became stale following conflict repair.\n- Added a design—not scoring—bridge from three reality anchors to three ordinary public tasks: arrival continuity, green-corridor public life, and non-transfer of reference intensity.\n- Preserved all unknown/provisional boundaries and rebuilt the bilingual first-page package around the public-task bridge.''')
    c.finalize_package(
        ('现实约束 → 公共任务', 'Reality constraints → public tasks', 'reality-to-public-task.svg'),
        'v091-public-task',
        'v0.91 首屏｜现实资料必须回到公共任务',
        'v0.91 First screen | Reality evidence must return to a public task',
        'reality-to-public-task.svg',
        'v0.91 reality-to-public-task'
    )
