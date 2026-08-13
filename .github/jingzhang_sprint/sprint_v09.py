from pathlib import Path
from . import sprint_common as c


def source(sid,title,url,publisher,usage,limitations,coverage,extra=None):
    rec={'id':sid,'url':url,'source_type':'official_public','usage':usage,'provenance':'政府/公共资源交易平台公开原件或正式公开页面。','accessed_or_snapshot_date':'2026-08-13','rights_and_reuse':'政府公开信息；仅做事实摘录、设计约束和来源链接，不复制官方图形商标。','limitations':limitations,'permitted_use':'只用于明确写出的现实参照或设计响应，不外推审批、权属或本案控制值。','publisher':publisher,'collection_method':'从官方公开页面核对；与公开原件字段交叉检查。','geographic_temporal_coverage':coverage,'transformations':'转写为本包 reality-constraint register，并将可支撑的事实翻译为空间响应；来源等级不升级。','title':title}
    if extra: rec.update(extra)
    return rec


def apply(pkg_path):
    c.configure('v0.9', pkg_path)
    c.set_iteration()
    sid_plan='HD00-1601-DRAFT-RESPONSE-V09'; sid_lanjing='HD-LANJINGLIJIA-INTEGRATED-RESPONSE-V09'; sid_plots='HD-PLOT-CONDITIONS-REFERENCE-V09'
    c.add_source(source(sid_plan,'京张铁路遗址公园沿线（人工智能创新街区重点地区）街区控规草案公示采信情况通告','https://ghzrzyw.beijing.gov.cn/chengxiangguihua/ghlgg/hd_ghlgg/202502/t20250207_4005553.html','北京市规划和自然资源委员会海淀分局','确认知春路相关铁路节点的官方草案阶段空间约束：该段知春路下穿铁路、不具备平交条件，并采用分离式立交思路预留联通条件。','仍为控规草案公示采信阶段公开信息，不是本案可直接采用的最终工程线位、道路红线或已批控制指标。','京张铁路遗址公园沿线人工智能创新街区重点地区；公开日期 2025-02-08。'))
    c.add_source(source(sid_lanjing,'蓝景丽家项目规划综合实施方案公示采信情况通告','https://ghzrzyw.beijing.gov.cn/chengxiangguihua/ghlgg/hd_ghlgg/202506/t20250606_4107444.html','北京市规划和自然资源委员会海淀分局','作为现实界面参照：相关商业商务规划应与东侧京张铁路绿廊衔接并提升空间品质。','个案采信结论不等于本方案地块条件，不得外推容积率、高度、权属或工程许可。','蓝景丽家城市更新相关范围；公开日期 2025-06。'))
    c.add_source(source(sid_plots,'总体设计范围内三份建设项目规划条件原件（7 个规划地块）','https://ggzyfw.beijing.gov.cn/zpgcrgg/20251231/5391270.html','北京市公共资源交易服务平台 / 北京市规划和自然资源委员会海淀分局','给本方案强度与高度讨论提供“现实标尺”，仅作不可外推的参照样本。','七宗是逐地块已批条件，不是总体设计范围控制值；不得把 2.20–5.00 FAR、24–80m 高度或其他指标转写为本案地块控制。','蓝景丽家、五塔寺、学院路北端 7 个公开地块；2018–2025 规划条件。',{'related_urls':['https://ggzyfw.beijing.gov.cn/zpgcrgg/20260108/5398628.html','https://ggzyfw.beijing.gov.cn/zpgcrgg/20231219/4281039.html']}))

    c.writej(c.va/'reference-plot-conditions.json',{'schema_version':'1.0','variant':'v0.9','title_zh':'7 个公开建设项目规划条件的现实参照（不可外推）','status':'official_public_reference_only','transcription_rule':'Only values explicitly written in published planning-condition originals are retained; null stays null. No value is transferred to proposal parcels.','plots':[
      {'plot_id':'HD00-1603-01','project':'蓝景丽家','far':2.45,'height_m':60,'density_pct':None,'green_ratio_min_pct':25},
      {'plot_id':'HD00-1603-03A','project':'蓝景丽家','far':2.2,'height_m':24,'density_pct':None,'green_ratio_min_pct':None},
      {'plot_id':'HD00-2002-10','project':'五塔寺','far':4.2,'height_m':45,'density_pct':None,'green_ratio_min_pct':10},
      {'plot_id':'学院路北端A','project':'学院路北端','far':5.0,'height_m':80,'density_pct':40,'green_ratio_min_pct':30},
      {'plot_id':'学院路北端B','project':'学院路北端','far':3.5,'height_m':80,'density_pct':35,'green_ratio_min_pct':35},
      {'plot_id':'学院路北端C','project':'学院路北端','far':3.5,'height_m':80,'density_pct':35,'green_ratio_min_pct':35},
      {'plot_id':'学院路北端J','project':'学院路北端','far':3.5,'height_m':80,'density_pct':45,'green_ratio_min_pct':35}],
      'summary':{'plot_count':7,'far_range':[2.2,5.0],'height_m_range':[24,80],'density_given_count':4,'green_ratio_given_count':6},'scope_limit':'Reality reference only. These values are NOT proposal controls and are never transferred to conceptual parcels.'})

    rules=[
      {'rule_id':'RR-01','anchor':'知春路下穿铁路 / no at-grade condition','source_id':sid_plan,'design_response_zh':'知春路缝合不再画成通用平交横穿；表达为“竖向连续性待解节点”，地面步行连续、上下层关系、无障碍和工程方案必须由后续专业设计核实。','what_is_not_claimed':'No bridge/tunnel alignment, road redline or engineering feasibility is claimed.'},
      {'rule_id':'RR-02','anchor':'京张绿廊东侧界面','source_id':sid_lanjing,'design_response_zh':'绿廊侧首先保持连续步行、公共首层和可停留界面；AI设备、物流和服务模块退到不切断公共通行的位置。','what_is_not_claimed':'No parcel ownership or approved frontage design is claimed.'},
      {'rule_id':'RR-03','anchor':'7 个公开地块规划条件','source_id':sid_plots,'design_response_zh':'FAR、高度、密度和绿地率只作为现实量级参照；本案 `approved_*` 指标继续 unknown，概念建筑不因邻近样本自动获得同样指标。','what_is_not_claimed':'Reference values are not proposal controls.'},
      {'rule_id':'RR-04','anchor':'控规仍处草案/推进审批语境','source_id':sid_plan,'design_response_zh':'所有“控制”图面保持概念建议/待确认；不把草案采信通告写成已生效法定控规。','what_is_not_claimed':'No statutory approval is claimed.'},
      {'rule_id':'RR-05','anchor':'official geometry / approved controls future trigger','source_id':'BOUNDARY-SOURCE','design_response_zh':'一旦组织方发布 official site/key-area polygons 或可适用的批准控制条件，统一重算 geometry、metrics、五张固定图、HTML 与四份 PDF；禁止局部手工平移制造“更真实”假象。','what_is_not_claimed':'Current provisional geometry remains unchanged.'}]
    c.writej(c.va/'reality-constraint-register.json',{'schema_version':'1.0','variant':'v0.9','title_zh':'现实约束 → 空间设计响应登记','status':'design_response_not_approval','rules':rules,'principle':'A source matters here only if it changes a spatial decision or makes an unknown more precise without fabricating it.'})

    zh_start='<!-- V09-REALITY-START -->'; zh_end='<!-- V09-REALITY-END -->'
    zh=f'''{zh_start}
### v0.9｜REALITY-ANCHORED：只有能改变空间判断的资料才进入主叙事

v0.9 是从 v0.7 exact head 分出的 **reality-anchored 并行候选**，不继承 v0.8 的原型收束实验。它把“来源更多”改成更窄的规则：**一条现实资料只有在改变断面、界面、节点或 unknown 的表达方式时，才进入设计主叙事。** 本轮登记 3 组官方公开现实锚点，并形成 5 条可检查的设计响应。[metric:official_constraint_anchor_count] [metric:design_response_rule_count]

![现实约束如何改变空间设计，而不是变成参考文献堆](assets/figures/reality-constraint-design-response.svg)

**第一条是知春路。** 海淀规自部门公开的控规草案采信通告明确，该铁路节点处知春路属于下穿段、不具备平交条件，并以分离式立交思路预留联通条件。[source:HD00-1601-DRAFT-RESPONSE-V09] 因此本案不再把六条东西缝合都画成同一种“地面横穿”：知春路改成**竖向连续性待解节点**，后续必须核实地面步行连续、上下层关系、无障碍和工程条件；当前不画桥隧线位、不声称工程可行。

**第二条是京张绿廊界面。** 蓝景丽家相关官方规划综合实施方案采信信息要求其商业商务规划与东侧京张铁路绿廊衔接并提升空间品质。[source:HD-LANJINGLIJIA-INTEGRATED-RESPONSE-V09] 本案据此把绿廊侧的优先级写得更硬：连续步行、可停留公共界面和人优先首层在前，AI 设备、物流与可替换服务模块不得切断公共通行。该个案不被外推为本案地块条件。

**第三条是现实强度标尺。** 三份公开《建设项目规划条件》覆盖 7 个地块，公开 FAR 参照为 2.20–5.00、建筑限高参照为 24–80m，部分地块另有密度与绿地率条件。[source:HD-PLOT-CONDITIONS-REFERENCE-V09] 这些数值只回答“现实里已经出现过什么量级”，绝不回答“本案应该批多少”。因此 `approved_floor_area_ratio`、`approved_building_height_m` 等继续保持 unknown，概念建筑也不套用任何相邻样本。[metric:reference_plot_condition_count]

五条设计响应完整记录于 `visual/assets/reality-constraint-register.json`。本轮固定 `mobility-bluegreen.png` 重建为不同类型的现实接口：普通缝合、下穿节点竖向连续性、绿廊人优先界面、站城到达与 official-data 重算触发器，不再用同一种蓝色虚线代表所有问题。
{zh_end}'''
    c.upsert_before(c.pkg/'proposal.md',zh_start,zh_end,zh,'## 用地、建筑规模与拆改留方案')

    en_start='<!-- V09-REALITY-START -->'; en_end='<!-- V09-REALITY-END -->'
    en=f'''{en_start}
### v0.9 | REALITY-ANCHORED: a source enters the design story only if it changes a spatial decision

v0.9 is a **reality-anchored parallel candidate** branched independently from the v0.7 exact head; it does not inherit the v0.8 prototype-convergence experiment. It applies a narrower rule: a public source enters the main design narrative only when it changes a section, interface, node, or the precision of an unknown. This round registers three official-public reality anchors and five explicit design-response rules. [metric:official_constraint_anchor_count] [metric:design_response_rule_count]

![How reality constraints change spatial design rather than becoming a bibliography](assets/figures/reality-constraint-design-response.en.svg)

**Zhichun Road:** the official public response to the draft control plan records this railway-related segment as underpassing the railway and unsuitable for an at-grade junction. [source:HD00-1601-DRAFT-RESPONSE-V09] The proposal therefore stops drawing every east-west stitch as the same surface crossing. Zhichun Road becomes a **vertical-continuity problem to be resolved**, with pedestrian continuity, level changes, accessibility and engineering conditions left for professional verification. No bridge/tunnel alignment or feasibility is claimed.

**Jing-Zhang green edge:** the official planning-response material for Lanjinglijia calls for integration with the Jing-Zhang railway green corridor and improved spatial quality. [source:HD-LANJINGLIJIA-INTEGRATED-RESPONSE-V09] The design response is people-first: continuous walking, staying and public frontage precede AI equipment, logistics and replaceable service modules. The case is not transferred as a parcel control.

**Reality scale references:** three published planning-condition documents cover seven plots, with reference FAR values of 2.20–5.00 and reference height controls of 24–80 m; some also publish density and green-ratio conditions. [source:HD-PLOT-CONDITIONS-REFERENCE-V09] These values answer only “what has appeared in approved plot conditions nearby”; they do not answer “what this proposal should receive”. Proposal `approved_*` metrics remain unknown. [metric:reference_plot_condition_count]

All five response rules are machine-readable in `visual/assets/reality-constraint-register.json`. The fixed `mobility-bluegreen.en.png` is rebuilt to distinguish ordinary stitching, the underpass/vertical-continuity condition, people-first green-corridor frontage, station-city arrival, and the future official-data recomputation trigger.
{en_end}'''
    c.upsert_before(c.pkg/'proposal.en.md',en_start,en_end,en,'## Land Use, Building Capacity, and Retain-Renovate-Demolish Strategy')

    zh_cols=[('节点不是一种',[('知春路','下穿铁路 → 竖向连续性待解'),('普通缝合','只表达连接需求，不造工程线位'),('站城到达','固定导视+人工服务先成立')],'#0f766e'),('界面有优先级',[('京张绿廊','连续步行与停留优先'),('公共首层','人优先、可读、可进入'),('AI/物流模块','退到不切断公共通行的位置')],'#2563eb'),('数值只作标尺',[('7 个地块','FAR 2.20–5.00 仅现实参照'),('高度 24–80m','不转写为本案控制'),('official 到位','整包重算，不手工平移')],'#b45309')]
    en_cols=[('Nodes are not identical',[('Zhichun Road','underpass → vertical continuity problem'),('ordinary stitch','connection need, not engineered alignment'),('station-city arrival','fixed wayfinding + staffed service first')],'#0f766e'),('Interfaces have priority',[('Jing-Zhang green edge','continuous walking and staying first'),('public ground floor','people-first, legible and enterable'),('AI/logistics modules','sit behind uninterrupted public passage')],'#2563eb'),('Numbers are references',[('7 public plots','FAR 2.20–5.00 = reality scale only'),('height 24–80m','never transferred as proposal control'),('official data trigger','recompute whole package; no manual shift')],'#b45309')]
    (c.fig/'reality-constraint-design-response.svg').write_text(c.svg_shell('REALITY → DESIGN｜现实资料必须改变空间判断','3 组官方现实锚点 → 5 条设计响应；unknown 仍然可以是正确答案',zh_cols,'v0.9 并行候选：来源不按数量加分，只按是否改变设计判断进入主叙事。'),encoding='utf-8')
    (c.fig/'reality-constraint-design-response.en.svg').write_text(c.svg_shell('REALITY → DESIGN | Public evidence must change a spatial decision','3 official-public anchors → 5 design responses; unknown can remain the correct answer',en_cols,'v0.9 parallel candidate: sources enter the main narrative only when they change a design decision.'),encoding='utf-8')

    c.save_png(c.fig/'mobility-bluegreen.png','慢行与蓝绿系统｜不同现实条件，不同空间响应','固定 reviewer 输入：不再把六条缝合画成同一种线。现实资料只在能改变断面/节点判断时进入。',[
      ('普通东西缝合','保留“需要连接”的关系；真实道路红线、过街方式和宽度待核。','LINK'),
      ('知春路节点','官方草案采信：下穿铁路、不宜平交 → 设计任务改为竖向连续性与无障碍。','LEVEL'),
      ('京张绿廊界面','连续步行、停留与公共首层优先；AI设备/物流不得切断公共通行。','EDGE'),
      ('站城到达','固定双语导视 + 人工服务先成立；动态信息只增强。','ARRIVE')],
      '全部线位仍为概念关系；不声称道路红线、桥隧方案、站口位置、工程可行性或已批控规。')
    c.save_png(c.fig/'mobility-bluegreen.en.png','Mobility + blue-green | different reality, different spatial response','Fixed reviewer input: east-west links are no longer drawn as one generic condition. Public evidence matters only when it changes a spatial decision.',[
      ('Ordinary stitch','Keep the need to connect; redline, crossing form and width remain pending.','LINK'),
      ('Zhichun node','Official draft response: underpass / no at-grade condition → solve vertical continuity and accessibility.','LEVEL'),
      ('Jing-Zhang green edge','Continuous walking, staying and public frontage first; AI/logistics cannot cut passage.','EDGE'),
      ('Station-city arrival','Fixed bilingual wayfinding + staffed service first; dynamic information only enhances.','ARRIVE')],
      'All alignments remain conceptual relationships; no road redline, bridge/tunnel scheme, station exit, feasibility or approved control plan is claimed.')

    c.add_metric('official_constraint_anchor_count',{'status':'known','value':3,'unit':'count','source_files':['sources.json','visual/assets/reality-constraint-register.json'],'formula':'count of three v0.9 official-public reality anchor groups','confidence':'high','assumptions':['Counts source groups used for design response; not approvals.']})
    c.add_metric('reference_plot_condition_count',{'status':'known','value':7,'unit':'count','source_files':['visual/assets/reference-plot-conditions.json'],'formula':'count of public plot-condition reference records','confidence':'high','assumptions':['Reference records only; values are not transferred to proposal parcels.']})
    c.add_metric('design_response_rule_count',{'status':'known','value':5,'unit':'count','source_files':['visual/assets/reality-constraint-register.json'],'formula':'count(RR-01..RR-05)','confidence':'high','assumptions':['Internal design-response rules.']})
    c.add_assumption({'id':'A-V09-REFERENCE-009','status':'official_reference_not_transferable','statement':'v0.9 引入的 7 个地块规划条件只作现实尺度参照；控规采信通告仍是草案阶段公开信息。','impact':'本案 approved FAR/height 等继续 unknown；任何参照值不得外推为本案地块指标、工程方案或审批状态。'})
    c.update_matrices('v0.9 现实约束 → 空间设计响应',['official_constraint_anchor_count','reference_plot_condition_count','design_response_rule_count'],[sid_plan,sid_lanjing,sid_plots])
    for path,role,lang,tr in [('assets/figures/reality-constraint-design-response.svg','proposal_figure','zh',None),('assets/figures/reality-constraint-design-response.en.svg','proposal_figure','en','assets/figures/reality-constraint-design-response.svg'),('visual/assets/reality-constraint-register.json','reality_constraint_register',None,None),('visual/assets/reference-plot-conditions.json','reference_plot_conditions',None,None)]: c.manifest_add(path,role,lang,tr)
    c.copyright_note('- `reality-constraint-design-response*.svg` 与重建的 `mobility-bluegreen*.png` 为 v0.9 原创图解，不复制官方图件。\n- `reference-plot-conditions.json` 只转录政府公开原件中的数值字段并明确不可外推；官方网页/原件链接保留在 `sources.json`。')
    c.changelog('## v0.9 - 2026-08-13\n\n- reality-anchored 并行候选：只把能改变空间判断的公开原始证据放入主叙事。\n- 新增 3 组官方现实锚点与 5 条“现实约束 → 空间响应”规则。\n- 登记 7 个公开规划条件地块作不可外推的现实强度参照；本案 approved FAR/height 继续 unknown。\n- 重建固定 `mobility-bluegreen*.png`，区分普通缝合、知春路竖向连续性、绿廊人优先界面和站城到达。')
    c.finalize_package(('现实约束 → 空间设计响应','Reality constraints → spatial design response','reality-constraint-design-response.svg'),'v09-reality-anchored','v0.9 首屏｜现实约束如何改变空间设计','v0.9 First screen | How reality constraints change spatial design','reality-constraint-design-response.svg','v0.9 reality-anchored')
