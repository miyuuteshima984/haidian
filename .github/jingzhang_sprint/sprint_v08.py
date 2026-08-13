from pathlib import Path
from . import sprint_common as c


def apply(pkg_path):
    c.configure('v0.8', pkg_path)
    c.set_iteration()

    zh_start='<!-- V08-PROTOTYPE-START -->'; zh_end='<!-- V08-PROTOTYPE-END -->'
    zh=f'''{zh_start}
### v0.8｜把六类接口收束成一个 1:1 城市原型：C7 CIVIC STATION

v0.8 是从 v0.7 exact head 分出的 **prototype-first 并行候选**。它不再增加新的评分索引，而把已有六类可逆接口收束成一个评委可在一页内读懂、专业团队可在未来按真实条件深化的 1:1 公共空间原型：**C7 CIVIC STATION / 城市完整度站**。它不是一座“AI 亭子”，而是一段普通城市先完整、AI 再进入的空间序列。[metric:flagship_physical_prototype_count]

原型固定为五段：**①普通城市底座**（遮阴、坐凳、连续无障碍、实体双语导视、普通通行）→ **②人工服务层**（无账号窗口、纸质/电话入口、人工接手）→ **③可选 AI 层**（多语问答、路径辅助、服务匹配）→ **④受控测试口袋**（与公共通行物理分离，可封闭、可撤除）→ **⑤ AI-OFF 恢复状态**（设备停机后仍可通行、求助、停留并获得基本服务）。三种运行状态为 DAILY / CONTROLLED TEST / AI-OFF；任何测试不得以牺牲普通通行、无障碍或基本公共服务为代价。[metric:civic_station_operating_state_count]

![C7 CIVIC STATION：一个可关闭、可恢复的 1:1 城市原型](assets/figures/c7-civic-station-prototype.svg)

同一原型在三区采用不同嵌入方式：众智园侧重“研发日常 → 受控测试”，测试口袋必须与服务劳动者和访客的普通路径分离；AI 原点侧重“无手机/照护日常 → 人工服务 → 可选 AI”，拒绝账号不降低基本服务；大钟寺侧重“站城到达 → 实体双语导视 → 人工换乘 → 可选动态信息”，动态系统失效后回到固定路径与人工服务。固定 `key-areas.png` 因此改为直接展示同一原型在三种城市织体中的差异化落位。

### v0.8｜15 个待测槽位：不填现场数值，先把未来验证工作定义清楚

为避免“以后再测”成为空话，三区各预登记五类 observation slot：**到达连续性、无账号/人工等价、无障碍与停留、测试边界、停机恢复与维护**，共 15 个稳定 `observation_id`。[metric:preregistered_observation_slot_count] 当前全部为 `not_measured`，坐标、样本量、阈值、现场读数、许可和责任主体均保持待真实踏勘/专业确认；这是一份现场工作包，不是现场证据。详见 `visual/assets/field-observation-register.json`。

每个槽位只回答四件事：未来要观察什么、由谁确认、什么情况必须停止解释、AI 退出后普通城市功能如何验收。任何未测字段都不得被图纸或指标自动补成“达标”。
{zh_end}'''
    c.upsert_before(c.pkg/'proposal.md',zh_start,zh_end,zh,'## 用地、建筑规模与拆改留方案')

    en_start='<!-- V08-PROTOTYPE-START -->'; en_end='<!-- V08-PROTOTYPE-END -->'
    en=f'''{en_start}
### v0.8 | One 1:1 urban prototype from six interfaces: C7 CIVIC STATION

v0.8 is a **prototype-first parallel candidate** branched from the v0.7 exact head. Instead of adding another reviewer dashboard, it converges the six reversible interfaces into one public-space prototype that can be read on one page and later developed against real site conditions: **C7 CIVIC STATION**. It is not an “AI kiosk”; it is a spatial sequence in which the ordinary city works first and AI enters only as an optional layer. [metric:flagship_physical_prototype_count]

The prototype always has five parts: **(1) ordinary-city base** (shade, seating, continuous accessibility, fixed bilingual wayfinding and ordinary passage) → **(2) staffed service** (no-account counter, paper/telephone entry and human takeover) → **(3) optional AI** (multilingual Q&A, route assistance and service matching) → **(4) controlled test pocket** (physically separated from public passage, closable and removable) → **(5) AI-OFF recovery state** (basic passage, help, staying and service remain available after shutdown). Its three operating states are DAILY / CONTROLLED TEST / AI-OFF. A test may never displace ordinary passage, accessibility or basic public service. [metric:civic_station_operating_state_count]

![C7 CIVIC STATION: one reversible and recoverable 1:1 urban prototype](assets/figures/c7-civic-station-prototype.en.svg)

The same prototype is embedded differently in the three key areas. Zhongzhiyuan separates controlled testing from the ordinary paths of workers and visitors; AI Origin prioritizes no-phone and care journeys before optional AI; Dazhongsi prioritizes fixed bilingual arrival and staffed interchange before dynamic information. The fixed `key-areas.en.png` is rebuilt to show these three distinct embeddings rather than another governance matrix.

### v0.8 | Fifteen preregistered observation slots, with no fabricated field values

Each key area receives five stable observation categories—**arrival continuity, no-account/staffed equivalence, accessibility and staying, test boundary, shutdown/recovery and maintenance**—for 15 `observation_id` values in total. [metric:preregistered_observation_slot_count] All are currently `not_measured`; coordinates, sample sizes, thresholds, field readings, permission and named responsible entities remain pending real survey and professional confirmation. This is a future field-work package, not field evidence. See `visual/assets/field-observation-register.json`.
{en_end}'''
    c.upsert_before(c.pkg/'proposal.en.md',en_start,en_end,en,'## Land Use, Building Capacity, and Retain-Renovate-Demolish Strategy')

    contract={
      'schema_version':'1.0','variant':'v0.8','prototype_id':'C7-CIVIC-STATION-01','status':'concept_not_authorized_not_run',
      'principle_zh':'普通城市先完整，AI只作为可关闭增强层。','principle_en':'The ordinary city works first; AI is only a switchable enhancement layer.',
      'states':['DAILY','CONTROLLED_TEST','AI_OFF'],
      'zones':[
        {'id':'Z1','name_zh':'普通城市底座','requirements':['shade_and_seating','continuous_accessible_route','fixed_bilingual_wayfinding','ordinary_passage']},
        {'id':'Z2','name_zh':'人工服务层','requirements':['no_account_counter','paper_or_phone_entry','human_takeover']},
        {'id':'Z3','name_zh':'可选 AI 层','requirements':['optional_multilingual_assistance','optional_route_help','minimal_data']},
        {'id':'Z4','name_zh':'受控测试口袋','requirements':['physically_separated_from_public_passage','closable','removable','human_stop_right']},
        {'id':'Z5','name_zh':'AI-OFF 恢复状态','requirements':['basic_passage_remains','help_remains','staying_remains','basic_service_remains']}
      ],
      'release_rule':'No controlled test is released if ordinary passage, accessibility, no-account service, human takeover, or physical separation is missing.',
      'evidence_boundary':'No field performance, permit, operator, budget, ownership, or engineering approval is claimed.'
    }
    c.writej(c.va/'c7-civic-station-contract.json',contract)

    areas=[('PROV-KEY-001','众智园','Zhongzhiyuan'),('PROV-KEY-002','AI 原点','AI Origin'),('PROV-KEY-003','大钟寺','Dazhongsi')]
    cats=[('ARRIVAL','到达连续性','arrival continuity'),('NOACCOUNT','无账号/人工等价','no-account/staffed equivalence'),('ACCESS','无障碍与停留','accessibility and staying'),('TESTBOUNDARY','测试边界','test boundary'),('RECOVERY','停机恢复与维护','shutdown recovery and maintenance')]
    slots=[]
    for aid,zh_name,en_name in areas:
        for code,zh_cat,en_cat in cats:
            slots.append({'observation_id':f'OBS-{aid[-3:]}-{code}','key_area_id':aid,'key_area_zh':zh_name,'key_area_en':en_name,'category_zh':zh_cat,'category_en':en_cat,'status':'not_measured','coordinates':None,'sample_size':None,'threshold':None,'field_result':None,'permission':None,'responsible_entity':None,'stop_interpretation_if':['official_geometry_or_real_entrance_not_verified','measurement_protocol_not_frozen','required_human_or_non_ai_baseline_missing'],'recovery_check':'AI-OFF must preserve ordinary passage, help, staying and basic service.'})
    c.writej(c.va/'field-observation-register.json',{'schema_version':'1.0','variant':'v0.8','title_zh':'C7 城市完整度站现场待测登记','status':'pre_registered_not_measured','slot_count':len(slots),'slots':slots,'boundary':'A field-work definition only. It contains no field measurement or authorization.'})

    zh_cols=[('普通城市底座',[('01 遮阴+坐凳','先能停留，再谈交互'),('02 无障碍连续','不靠 AI 修补物理断点'),('03 实体双语导视','无电/无网仍能到达')],'#0f766e'),('人工 + 可选 AI',[('04 无账号窗口','纸质/电话/人工同任务'),('05 可选 AI','最少数据，可拒绝'),('06 人工接手','高风险与失败转人')],'#2563eb'),('受控测试 + 恢复',[('07 测试口袋','与公共通行物理分离'),('08 一键停机','停止权先于扩张'),('09 AI-OFF','基本城市功能仍完整')],'#b45309')]
    en_cols=[('Ordinary-city base',[('01 Shade + seating','Stay first; interact later'),('02 Continuous access','AI cannot patch a physical barrier'),('03 Fixed bilingual wayfinding','Arrival still works offline')],'#0f766e'),('Staffed + optional AI',[('04 No-account counter','Paper/phone/human same task'),('05 Optional AI','Minimal data; refusal allowed'),('06 Human takeover','High-risk or failure goes human')],'#2563eb'),('Controlled test + recovery',[('07 Test pocket','Physically separate from passage'),('08 Immediate stop','Stop right before scaling'),('09 AI-OFF','Basic city function remains')],'#b45309')]
    (c.fig/'c7-civic-station-prototype.svg').write_text(c.svg_shell('C7 CIVIC STATION｜一个 1:1 城市完整度原型','普通城市底座 → 人工服务 → 可选 AI → 受控测试 → AI-OFF 恢复',zh_cols,'概念原型，不代表已选址、获批、建成或现场绩效；所有真实尺寸与工程条件待专业深化。'),encoding='utf-8')
    (c.fig/'c7-civic-station-prototype.en.svg').write_text(c.svg_shell('C7 CIVIC STATION | One 1:1 city-completeness prototype','ordinary city → staffed service → optional AI → controlled test → AI-OFF recovery',en_cols,'Concept prototype only; no site approval, construction, field performance or engineering clearance is claimed.'),encoding='utf-8')

    c.save_png(c.fig/'key-areas.png','三区同一原型，三种城市嵌入','固定 reviewer 输入：不再展示抽象 task cards，而展示 C7 CIVIC STATION 如何进入三种不同城市织体。',[
      ('众智园｜完整创新校园','研发到达、吃饭休息和普通步行先连续；受控机器人/设备测试进入独立口袋，不能占普通通路。','TEST'),
      ('AI 原点｜完整长期社区','家门—遮阴坐凳—人工照护/服务—公共客厅先成立；无手机、拒绝账号仍完成基本任务。','CARE'),
      ('大钟寺｜完整站城生活区','固定双语导视、人工换乘、普通商业与休息先成立；动态 AI 信息失败时回到实体路径。','ARRIVE')],
      '三处仍为 provisional key-area；图示表达任务角色和空间序列，不是站口、地块或工程定位。')
    c.save_png(c.fig/'key-areas.en.png','One prototype, three urban embeddings','Fixed reviewer input: C7 CIVIC STATION is embedded differently in three urban fabrics, not repeated as generic task cards.',[
      ('Zhongzhiyuan | innovation campus','R&D arrival, meals, rest and ordinary walking stay continuous; controlled robot/device tests occupy a separate pocket.','TEST'),
      ('AI Origin | long-term community','Home, shade, seating, staffed care/service and commons work first; no phone or account is required for the basic task.','CARE'),
      ('Dazhongsi | station-city life','Fixed bilingual wayfinding, staffed interchange, ordinary commerce and rest work first; dynamic AI falls back to physical routes.','ARRIVE')],
      'All key-area geometry remains provisional; this shows spatial roles, not station exits, parcels or engineering positions.')

    c.add_metric('flagship_physical_prototype_count',{'status':'known','value':1,'unit':'count','source_files':['proposal.md','visual/assets/c7-civic-station-contract.json','assets/figures/c7-civic-station-prototype.svg'],'formula':'count(C7-CIVIC-STATION-01)','confidence':'high','assumptions':['Internal concept prototype; not a built asset.']})
    c.add_metric('preregistered_observation_slot_count',{'status':'known','value':15,'unit':'count','source_files':['visual/assets/field-observation-register.json'],'formula':'3 key areas * 5 preregistered observation categories','confidence':'high','assumptions':['Counts future observation slots, not completed field observations.']})
    c.add_metric('civic_station_operating_state_count',{'status':'known','value':3,'unit':'count','source_files':['visual/assets/c7-civic-station-contract.json'],'formula':'count(DAILY, CONTROLLED_TEST, AI_OFF)','confidence':'high','assumptions':['Concept operating states.']})
    c.add_assumption({'id':'A-V08-FIELD-009','status':'not_measured','statement':'v0.8 的 15 个 observation slot 只预登记未来现场验证结构，当前没有坐标、样本、阈值、现场绩效、许可或具名责任主体。','impact':'任何图件、指标或评审叙述不得把待测字段自动填成达标或已实施。'})
    c.update_matrices('v0.8 C7 CIVIC STATION 1:1 原型与现场待测登记',['flagship_physical_prototype_count','preregistered_observation_slot_count','civic_station_operating_state_count'])
    for path,role,lang,tr in [('assets/figures/c7-civic-station-prototype.svg','proposal_figure','zh',None),('assets/figures/c7-civic-station-prototype.en.svg','proposal_figure','en','assets/figures/c7-civic-station-prototype.svg'),('visual/assets/c7-civic-station-contract.json','prototype_contract',None,None),('visual/assets/field-observation-register.json','field_observation_register',None,None)]: c.manifest_add(path,role,lang,tr)
    c.copyright_note('- `c7-civic-station-prototype*.svg`、重建的 `key-areas*.png` 与两份 JSON 均由本投稿在 v0.8 内原创生成；未使用第三方照片、Logo、地图瓦片或字体文件。\n- 15 个 observation slot 是未测工作结构，不含个人信息、真实坐标或现场数据。')
    c.changelog('## v0.8 - 2026-08-13\n\n- prototype-first 并行候选：把六类可逆接口收束为一个 C7 CIVIC STATION 1:1 公共原型。\n- 新增 DAILY / CONTROLLED_TEST / AI_OFF 三状态与五段空间合同。\n- 新增三区 × 五类共 15 个 `not_measured` 现场待测槽位，不虚构现场数值。\n- 重建固定 `key-areas*.png`，让 reviewer 输入直接看到同一原型在三种城市织体中的差异化落位。')
    c.finalize_package(('C7 CIVIC STATION 1:1 原型','C7 CIVIC STATION 1:1 prototype','c7-civic-station-prototype.svg'),'v08-civic-station','v0.8 首屏｜C7 CIVIC STATION 1:1 城市原型','v0.8 First screen | C7 CIVIC STATION 1:1 prototype','c7-civic-station-prototype.svg','v0.8 prototype-first')
