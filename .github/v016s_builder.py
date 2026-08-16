#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
from reportlab.lib.pagesizes import A0, A3, landscape
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.pdfgen import canvas

REPO = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path.cwd()
ROOT = REPO / "submissions/miyuuteshima984/jingzhang-ai-civic-infrastructure"

BG = "#F5F1E7"
INK = "#203033"
MUTED = "#667477"
GREEN = "#2D6B5E"
GREEN2 = "#74A38F"
ORANGE = "#D26F3C"
BLUE = "#4C7795"
SAND = "#E4D8C4"
WHITE = "#FFFFFF"
LINE = "#C9C1B5"
PALE = "#ECE7DC"


def load_json(rel: str):
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


def save_json(rel: str, data) -> None:
    (ROOT / rel).write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def replace_marker(text: str, start_candidates: list[str], end_candidates: list[str], block: str) -> str:
    for s in start_candidates:
        if s not in text:
            continue
        a = text.index(s)
        for e in end_candidates:
            if e in text[a:]:
                b = text.index(e, a) + len(e)
                return text[:a] + block + text[b:]
    raise RuntimeError(f"marker block not found: {start_candidates}")


def feature_id(f):
    return str(f.get("id") or f.get("properties", {}).get("id") or "")


def metric(value, unit, sources, formula, confidence="high", assumptions=None):
    return {
        "status": "known",
        "value": value,
        "unit": unit,
        "source_files": sources,
        "formula": formula,
        "confidence": confidence,
        "assumptions": assumptions or [],
    }


ZH_CORE = '''<!-- V016-CORE-START -->
## v0.16.s 核心判断｜CLEAN EXIT CITY / 可退出的 AI 城市

**AI 不只要能关闭，还必须能被城市完整地撤走。** v0.15.s 已经证明“普通城市是主机，AI 只能侧挂”；v0.16.s 把“可逆”从一句原则升级为空间生命周期：**BASE CITY → ATTACH → OPERATE → CLEAN EXIT**。[metric:sidecar_lifecycle_stage_count] [metric:clean_exit_host_count]

AI 进入城市时必须同时回答两个问题：它附着在哪里，以及拆掉以后这里恢复成什么普通城市用途。三条 `ROAD-009 / 010 / 011` 在四个生命周期阶段都保持相同 ordinary-city route；变化只发生在九个既有 host 的侧挂层。[metric:clean_exit_restore_use_coverage_ratio] [metric:ai_off_route_preservation_ratio]

| 重点区 | BASE CITY | ATTACH / OPERATE | CLEAN EXIT 后恢复 | 不变的公共承诺 |
| --- | --- | --- | --- | --- |
| 众智园 | 研发首层、吃饭休息、绿脊与开放交流 | `TEST POCKET` 只占侧院/服务边，承担受控测试与临时接口 | 测试撤出后回到普通院落、工作休息与公共交流，不迁移 `ROAD-009` | **TEST WITHOUT BLOCKING** |
| AI 原点 | 住宅、人工帮助、共学、公共首层与社区客厅 | `CARE PORCH` 只增加自愿导航、匹配与照护提示 | 数字层撤出后人工服务、公共首层和社区生活继续成立，不迁移 `ROAD-010` | **CARE WITHOUT ACCOUNT** |
| 大钟寺 | 固定导视、人工问询、普通等候/商业与京张公共界面 | `ARRIVAL SIDECAR` 只增加动态翻译、信息与客流辅助 | 动态层撤出后固定导视和人工服务继续成立，不迁移 `ROAD-011` | **ARRIVE WITHOUT APP** |

九个 sidecar host 都新增 `ordinary_restore_use`、`clean_exit_mode` 与 `field_check_required`；三条 route 新增 `clean_exit_route_preserved=true`。这些都是关系与生命周期语义，不改变建筑、公共空间或道路几何，也不创造第八类 AI 用地。[metric:new_ai_land_use_code_count]

**CLEAN EXIT 不是“AI 关机”。** 关机只证明软件停止；clean exit 还要求临时设备、接口、标识与运营依赖能够撤出，宿主空间重新成为普通城市，并保留人工服务、固定导视、日常路径与公共使用权。真实拆除工艺、消防、市政、产权和设施处置仍须项目阶段确认，本案不虚构工程参数。

大钟寺继续坚持 **REAL LEVEL DATA REQUIRED**：真实站口、竖向高程、桥隧、客流能力、产权与运营主体未确认前，不把 CLEAN EXIT 画成虚构工程线位。[data:geometry/key_areas.geojson#PROV-KEY-003]

![三处重点区从普通城市、AI侧挂到完整退出：主路径与普通城市用途保持连续](assets/figures/key-areas.png)
<!-- V016-CORE-END -->'''

EN_CORE = '''<!-- V016-CORE-START -->
## v0.16.s Core Judgment | CLEAN EXIT CITY

**AI must not only switch off; the city must be able to remove it cleanly.** v0.15.s established that the ordinary city is the host and AI is only a sidecar. v0.16.s turns reversibility into a spatial lifecycle: **BASE CITY → ATTACH → OPERATE → CLEAN EXIT**. [metric:sidecar_lifecycle_stage_count] [metric:clean_exit_host_count]

Every AI attachment must answer two questions at entry: where does it attach, and what ordinary-city use returns after removal? `ROAD-009 / 010 / 011` remain the same ordinary civic routes across all four lifecycle stages. Only the lateral layer on nine existing hosts changes. [metric:clean_exit_restore_use_coverage_ratio] [metric:ai_off_route_preservation_ratio]

| Key area | BASE CITY | ATTACH / OPERATE | Restored after CLEAN EXIT | Invariant public promise |
| --- | --- | --- | --- | --- |
| Zhongzhiyuan | R&D ground floors, food/rest, green spine and public exchange | `TEST POCKET` stays at side yards/service edges for bounded tests and temporary interfaces | removal restores ordinary courtyards, work/rest and public exchange without relocating `ROAD-009` | **TEST WITHOUT BLOCKING** |
| AI Origin | homes, human help, shared learning, public ground floors and civic commons | `CARE PORCH` adds only opt-in navigation, matching and care prompts | removal leaves staffed service, public ground floors and community life intact without relocating `ROAD-010` | **CARE WITHOUT ACCOUNT** |
| Dazhongsi | fixed wayfinding, staffed help, ordinary waiting/retail and the Jing-Zhang public interface | `ARRIVAL SIDECAR` adds only dynamic translation, information and crowd assistance | removal leaves fixed wayfinding and human service intact without relocating `ROAD-011` | **ARRIVE WITHOUT APP** |

All nine sidecar hosts receive `ordinary_restore_use`, `clean_exit_mode` and `field_check_required`; the three routes receive `clean_exit_route_preserved=true`. These are relationship and lifecycle semantics only. They do not change building, public-space or road geometry and they create no eighth AI land-use class. [metric:new_ai_land_use_code_count]

**CLEAN EXIT is more than AI OFF.** Switching off proves software stops. Clean exit additionally requires temporary equipment, interfaces, signs and operating dependencies to be removable so the host returns to ordinary city use with human service, fixed wayfinding, everyday routes and public access intact. Real de-installation methods, fire safety, utilities, ownership and asset disposal remain project-stage questions rather than fabricated engineering parameters.

Dazhongsi remains **REAL LEVEL DATA REQUIRED**. Until real station entrances, levels, bridges/tunnels, passenger capacity, ownership and operating roles are verified, clean exit is not drawn as a fake engineering alignment. [data:geometry/key_areas.geojson#PROV-KEY-003]

![Three key areas from base city to AI sidecar to clean exit: ordinary routes and uses remain continuous](assets/figures/key-areas.en.png)
<!-- V016-CORE-END -->'''

ZH_LIFECYCLE = '''<!-- V016-LIFECYCLE-START -->
### v0.16.s｜四步空间生命周期：BASE CITY → ATTACH → OPERATE → CLEAN EXIT

这四步不是新的治理状态机，而是每一个 sidecar 都必须通过的**空间交接顺序**。`BASE CITY` 先确认普通城市可独立工作；`ATTACH` 只允许侧向、可识别、可拆除的新增层；`OPERATE` 要保留人工接管和普通路径；`CLEAN EXIT` 则必须把宿主交还给普通用途，并留下可复核的退出记录。[metric:sidecar_lifecycle_stage_count]

| 生命周期 | 空间问题 | 众智园 | AI 原点 | 大钟寺 |
| --- | --- | --- | --- | --- |
| BASE CITY | 没有 AI 时这里是什么？ | 普通研发/工作院落 + 公共绿脊 | 住宅 + 人工服务 + 社区公共首层 | 固定导视 + 人工帮助 + 等候/商业 |
| ATTACH | AI 从哪里进入且不占主路？ | 测试侧院 / 服务边 | 公共首层 / 照护门廊 | 到达侧带 / 信息界面 |
| OPERATE | 运行时什么不能被 AI 接管？ | `ROAD-009` 与普通工作/休息链 | `ROAD-010`、人工帮助与无账号入口 | `ROAD-011`、固定导视与人工问询 |
| CLEAN EXIT | 拆除后如何恢复普通城市？ | 撤设备与临时接口，恢复院落/公共交流 | 撤数字接口，保留人工服务和公共首层 | 撤动态层，保留固定导视、人工帮助与普通等候 |

每个 host 的 `ordinary_restore_use` 都是定性空间用途，不声称现场已具备或已完成改造；每次真实 attach / clean exit 前后都需要现场核验。这样，“可逆”不再靠未来承诺，而是在设计时就预留了退出后的城市状态。[metric:clean_exit_restore_use_coverage_ratio]
<!-- V016-LIFECYCLE-END -->'''

EN_LIFECYCLE = '''<!-- V016-LIFECYCLE-START -->
### v0.16.s | Four-Step Spatial Lifecycle: BASE CITY → ATTACH → OPERATE → CLEAN EXIT

These four steps are not another governance state machine. They are the **spatial handover sequence** every sidecar must satisfy. `BASE CITY` proves the ordinary city works independently; `ATTACH` permits only a lateral, legible and removable layer; `OPERATE` preserves human takeover and ordinary routes; `CLEAN EXIT` returns the host to ordinary use and leaves reviewable exit evidence. [metric:sidecar_lifecycle_stage_count]

| Lifecycle | Spatial question | Zhongzhiyuan | AI Origin | Dazhongsi |
| --- | --- | --- | --- | --- |
| BASE CITY | What is here without AI? | ordinary R&D/work courtyard + public green spine | homes + staffed service + public ground floor | fixed wayfinding + staffed help + waiting/retail |
| ATTACH | Where can AI enter without occupying the main route? | test side yard / service edge | public ground floor / care porch | arrival side band / information interface |
| OPERATE | What may AI never take over? | `ROAD-009` and ordinary work/rest chain | `ROAD-010`, human help and account-free entry | `ROAD-011`, fixed wayfinding and staffed help |
| CLEAN EXIT | What ordinary city returns after removal? | remove equipment/interfaces; restore courtyard/public exchange | remove digital interface; retain staffed service and public ground floor | remove dynamic layer; retain fixed wayfinding, help and ordinary waiting |

Each host's `ordinary_restore_use` is a qualitative spatial use, not a claim that field conditions are already built or verified. Real attachment and exit require before/after field checks. Reversibility therefore becomes a designed return state rather than a future promise. [metric:clean_exit_restore_use_coverage_ratio]
<!-- V016-LIFECYCLE-END -->'''


def update_proposals():
    for rel, core, lifecycle, lang in [
        ("proposal.md", ZH_CORE, ZH_LIFECYCLE, "zh"),
        ("proposal.en.md", EN_CORE, EN_LIFECYCLE, "en"),
    ]:
        p = ROOT / rel
        text = p.read_text(encoding="utf-8")
        text = re.sub(r'iteration:\s*"v0\.15"', 'iteration: "v0.16"', text, count=1)
        text = text.replace('"version": "v0.15.s"', '"version": "v0.16.s"')
        text = text.replace("v0.15.s｜AI SIDECAR CITY / AI 侧挂城市", "v0.16.s｜CLEAN EXIT CITY / 可退出的 AI 城市")
        text = text.replace("v0.15.s Core Judgment | AI SIDECAR CITY", "v0.16.s Core Judgment | CLEAN EXIT CITY")
        text = replace_marker(
            text,
            ["<!-- V015-CORE-START -->", "<!-- V016-CORE-START -->"],
            ["<!-- V015-CORE-END -->", "<!-- V016-CORE-END -->"],
            core,
        )
        if "<!-- V015-SIDECAR-START -->" in text:
            text = replace_marker(text, ["<!-- V015-SIDECAR-START -->"], ["<!-- V015-SIDECAR-END -->"], lifecycle)
        elif "<!-- V016-LIFECYCLE-START -->" in text:
            text = replace_marker(text, ["<!-- V016-LIFECYCLE-START -->"], ["<!-- V016-LIFECYCLE-END -->"], lifecycle)
        else:
            anchor = "## 用地、建筑规模与拆改留方案" if lang == "zh" else "## Land Use, Building Scale, and Retain-Renovate-Demolish Strategy"
            if anchor not in text:
                raise RuntimeError(f"lifecycle insertion anchor missing in {rel}")
            text = text.replace(anchor, lifecycle + "\n\n" + anchor, 1)
        p.write_text(text, encoding="utf-8")


def update_agent_and_changelog():
    agent = load_json("agent.json")
    agent["version"] = "v0.16.s"
    agent["authorship_note_zh"] = "由 GitHub 用户 miyuuteshima984 提出 C7 城市完整度、不绕行城市路径、AI 侧挂与可完整退出的迭代目标，并持续审阅；ChatGPT（GPT-5.6 Sol）负责 v0.16.s CLEAN EXIT CITY 的空间生命周期构建、机器证据、图件/报告重组与验证工程。最终方案由人类参与者决定并提交。"
    save_json("agent.json", agent)
    cp = ROOT / "changelog.md"
    text = cp.read_text(encoding="utf-8")
    block = """\n## v0.16 - 2026-08-16\n\n- CLEAN EXIT CITY：把 v0.15.s 的可逆 sidecar 升级为 BASE CITY → ATTACH → OPERATE → CLEAN EXIT 四步空间生命周期。\n- 九个既有 sidecar host 写入 ordinary_restore_use / clean_exit_mode / field_check_required；三条 invariant routes 在完整生命周期内保持不变。\n- phasing 增加 clean-exit 交接规则，不改变任何 phase polygon 或锁定面积指标。\n- 重建 key-area lifecycle hero、metrics evidence、双语 visual 与 A3/A0，令“AI 如何进入并完整退出城市”直接进入 Review Agent 多模态首屏。\n- 不新增 AI 用地，不虚构站口、高差、桥隧、净宽、吞吐、FAR、高度或已确认运营主体。\n"""
    if "## v0.16 - 2026-08-16" not in text:
        text = text.rstrip() + "\n" + block
    cp.write_text(text, encoding="utf-8")


def update_geometry():
    lifecycle = ["base_city", "attach_optional", "operate_reviewable", "clean_exit_restore"]
    bmap = {
        "BLDG-012": ("test_pocket", "ordinary R&D/work ground floor and courtyard edge", "remove temporary test/service interfaces; return edge to ordinary work and public access"),
        "BLDG-013": ("test_pocket", "ordinary enterprise/public service entry", "remove replaceable interface; retain ordinary service entry and public access"),
        "BLDG-007": ("care_porch", "account-free home access and ordinary public-ground-floor use", "remove digital prompts; retain home access and ordinary public ground floor"),
        "BLDG-009": ("care_porch", "shared learning and staffed human help", "remove optional navigation/matching layer; retain learning and staffed help"),
        "BLDG-001": ("arrival_sidecar", "ordinary station-city support frontage", "remove dynamic layer; retain ordinary frontage and staffed service role subject to real station data"),
        "BLDG-002": ("arrival_sidecar", "ordinary waiting/retail and public interface", "remove dynamic layer; retain ordinary waiting/retail interface subject to real station data"),
    }
    pmap = {
        "PUBLIC-006": ("test_pocket", "ordinary campus courtyard/public exchange", "remove temporary test elements; restore courtyard/public exchange"),
        "PUBLIC-004": ("care_porch", "ordinary civic commons, seating and human help interface", "remove digital layer; retain ordinary commons and human help"),
        "PUBLIC-001": ("arrival_sidecar", "ordinary public arrival/waiting interface with fixed wayfinding", "remove dynamic layer; retain fixed wayfinding, staffed help and ordinary waiting subject to real station data"),
    }
    for rel, mapping in [("geometry/buildings.geojson", bmap), ("geometry/public_space.geojson", pmap)]:
        data = load_json(rel)
        seen = set()
        for f in data["features"]:
            fid = feature_id(f)
            if fid not in mapping:
                continue
            seen.add(fid)
            typ, restore, mode = mapping[fid]
            pr = f.setdefault("properties", {})
            pr["ai_sidecar_type"] = typ
            pr["sidecar_lifecycle"] = lifecycle
            pr["ordinary_restore_use"] = restore
            pr["clean_exit_required"] = True
            pr["clean_exit_mode"] = mode
            pr["field_check_required"] = True
            pr["host_geometry_changes_for_sidecar"] = False
            pr["lifecycle_reality_boundary"] = "conceptual spatial lifecycle; real installation/removal method, ownership, fire safety, utilities and permits require project-stage verification"
        missing = set(mapping) - seen
        if missing:
            raise RuntimeError(f"missing lifecycle hosts in {rel}: {sorted(missing)}")
        save_json(rel, data)

    roads = load_json("geometry/roads.geojson")
    rtypes = {"ROAD-009":"test_pocket", "ROAD-010":"care_porch", "ROAD-011":"arrival_sidecar"}
    seen = set()
    for f in roads["features"]:
        fid = feature_id(f)
        if fid not in rtypes:
            continue
        seen.add(fid)
        pr = f.setdefault("properties", {})
        pr["ai_sidecar_type"] = rtypes[fid]
        pr["sidecar_lifecycle"] = lifecycle
        pr["route_geometry_changes_when_ai_on"] = False
        pr["clean_exit_route_preserved"] = True
        pr["clean_exit_route_rule"] = "ordinary route geometry and public task chain remain invariant from base city through clean exit"
        pr["field_check_required"] = True
    if set(rtypes) - seen:
        raise RuntimeError("missing invariant routes")
    save_json("geometry/roads.geojson", roads)

    ph = load_json("geometry/phasing.geojson")
    for f in ph["features"]:
        pr = f.setdefault("properties", {})
        pr["sidecar_lifecycle_required"] = lifecycle
        pr["clean_exit_required"] = True
        pr["ordinary_city_baseline_required_before_ai_attachment"] = True
        pr["phase_geometry_changes_for_lifecycle"] = False
        pr["clean_exit_evidence"] = "before/after field check + host restore-use confirmation + unresolved project-stage constraints recorded"
    save_json("geometry/phasing.geojson", ph)


def update_metrics():
    data = load_json("metrics.json")
    m = data.setdefault("metrics", {})
    m["sidecar_lifecycle_stage_count"] = metric(4, "count", ["proposal.md", "geometry/buildings.geojson", "geometry/public_space.geojson", "geometry/phasing.geojson"], "count(base_city, attach_optional, operate_reviewable, clean_exit_restore)", assumptions=["Internal spatial lifecycle, not an approved project procedure."])
    m["clean_exit_host_count"] = metric(9, "count", ["geometry/buildings.geojson", "geometry/public_space.geojson"], "count(selected sidecar hosts with clean_exit_required=true)", assumptions=["Counts conceptual host relationships; no installed AI asset is claimed."])
    m["clean_exit_restore_use_coverage_ratio"] = metric(1.0, "ratio", ["geometry/buildings.geojson", "geometry/public_space.geojson"], "hosts with non-empty ordinary_restore_use / clean_exit_host_count", assumptions=["Coverage proves design documentation only; field restoration performance is not measured."])
    m["clean_exit_route_preservation_ratio"] = metric(1.0, "ratio", ["geometry/roads.geojson"], "invariant civic routes with clean_exit_route_preserved=true / 3", assumptions=["Conceptual route geometry only; not an engineering alignment."])
    # Preserve the two central v0.15.s invariants explicitly.
    if "new_ai_land_use_code_count" in m:
        m["new_ai_land_use_code_count"]["value"] = 0
    if "ai_off_route_preservation_ratio" in m:
        m["ai_off_route_preservation_ratio"]["value"] = 1.0
    save_json("metrics.json", data)


def update_contract():
    data = load_json("visual/assets/public-promises-contract.json")
    data["schema_version"] = "1.6"
    data["variant"] = "v0.16.s"
    data["title_zh"] = "可退出的AI城市 / CLEAN EXIT CITY"
    data["status"] = "concept_spatial_sidecar_with_clean_exit_lifecycle"
    data["principle"] = "AI must not only switch off; every sidecar must carry a spatial return state for the ordinary city."
    data["lifecycle"] = ["base_city", "attach_optional", "operate_reviewable", "clean_exit_restore"]
    for c in data.get("contracts", []):
        c["lifecycle"] = data["lifecycle"]
        c["clean_exit_required"] = True
        if c.get("sidecar_type") == "test_pocket":
            c["ordinary_restore_use"] = "ordinary campus courtyard, work/rest edge and public exchange"
        elif c.get("sidecar_type") == "care_porch":
            c["ordinary_restore_use"] = "account-free public ground floor, staffed human help and civic commons"
        else:
            c["ordinary_restore_use"] = "fixed wayfinding, staffed help and ordinary waiting/retail; real station levels remain required"
        c["clean_exit_evidence"] = ["before/after field check", "host restore-use confirmation", "unresolved project-stage constraints recorded"]
    save_json("visual/assets/public-promises-contract.json", data)


def update_matrices():
    lifecycle_metrics = ["sidecar_lifecycle_stage_count", "clean_exit_host_count", "clean_exit_restore_use_coverage_ratio", "clean_exit_route_preservation_ratio"]
    for rel in ["compliance_matrix.json", "design_depth_matrix.json", "standard_matrix.json"]:
        data = load_json(rel)
        def walk(x):
            if isinstance(x, dict):
                for k, v in list(x.items()):
                    if isinstance(v, str):
                        v = v.replace("v0.15.s 核心判断｜AI SIDECAR CITY / AI 侧挂城市", "v0.16.s 核心判断｜CLEAN EXIT CITY / 可退出的 AI 城市")
                        v = v.replace("v0.15.s Core Judgment | AI SIDECAR CITY", "v0.16.s Core Judgment | CLEAN EXIT CITY")
                        x[k] = v
                    elif k == "metrics" and isinstance(v, list) and any(s in v for s in ["ai_sidecar_type_count", "ai_sidecar_host_feature_count", "ai_off_route_preservation_ratio"]):
                        for mm in lifecycle_metrics:
                            if mm not in v:
                                v.append(mm)
                    else:
                        walk(v)
            elif isinstance(x, list):
                for item in x:
                    walk(item)
        walk(data)
        save_json(rel, data)


def fonts():
    candidates = [
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    reg = next((p for p in candidates if Path(p).is_file()), candidates[-1])
    bold = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
    if not Path(bold).is_file():
        bold = reg
    return reg, bold


def draw_wrapped(draw, xy, text, font, fill, width_chars, spacing=8):
    x, y = xy
    lines = []
    for para in str(text).split("\n"):
        while len(para) > width_chars:
            lines.append(para[:width_chars])
            para = para[width_chars:]
        lines.append(para)
    draw.multiline_text((x,y), "\n".join(lines), font=font, fill=fill, spacing=spacing)


def lifecycle_figure(lang="zh"):
    reg, bold = fonts()
    F = lambda n, b=False: ImageFont.truetype(bold if b else reg, n)
    im = Image.new("RGB", (1800, 1260), BG)
    d = ImageDraw.Draw(im)
    title = "可退出的 AI 城市 / CLEAN EXIT CITY" if lang == "zh" else "CLEAN EXIT CITY / AI WITH A SPATIAL RETURN STATE"
    sub = "BASE CITY → ATTACH → OPERATE → CLEAN EXIT：AI 撤出后，普通城市回到原位" if lang == "zh" else "BASE CITY → ATTACH → OPERATE → CLEAN EXIT: the ordinary city returns after AI removal"
    d.text((70,55), title, font=F(58,True), fill=INK)
    d.text((72,130), sub, font=F(27), fill=MUTED)
    states = ["BASE CITY", "AI SIDECAR", "CLEAN EXIT"]
    sx = [500, 910, 1320]
    for x, s in zip(sx, states):
        d.rounded_rectangle((x-165,190,x+165,245), 18, fill=WHITE, outline=LINE, width=2)
        d.text((x,218), s, font=F(23,True), fill=INK, anchor="mm")
    rows = [
        ("众智园 / Zhongzhiyuan", "ROAD-009", "TEST POCKET", "研发/工作 + 绿脊 + 交流" if lang=="zh" else "R&D/work + green spine + exchange", "恢复普通院落与公共交流" if lang=="zh" else "restore ordinary courtyard + exchange"),
        ("AI 原点 / AI Origin", "ROAD-010", "CARE PORCH", "住宅 + 人工帮助 + 公共首层" if lang=="zh" else "homes + human help + public ground floor", "保留人工服务与无账号入口" if lang=="zh" else "retain staffed service + account-free entry"),
        ("大钟寺 / Dazhongsi", "ROAD-011", "ARRIVAL SIDECAR", "固定导视 + 人工帮助 + 等候" if lang=="zh" else "fixed signs + staffed help + waiting", "保留固定导视与普通到达" if lang=="zh" else "retain fixed signs + ordinary arrival"),
    ]
    y0s = [300, 605, 910]
    for (name, rid, sidecar, base, restore), y in zip(rows, y0s):
        d.rounded_rectangle((65,y-15,300,y+230), 24, fill=WHITE, outline=LINE, width=2)
        d.text((90,y+20), name, font=F(27,True), fill=INK)
        d.text((90,y+62), rid, font=F(22,True), fill=GREEN)
        draw_wrapped(d,(90,y+105),base,F(20),MUTED,13,6)
        for idx, x in enumerate(sx):
            d.rounded_rectangle((x-170,y-15,x+170,y+230), 24, fill=WHITE, outline=LINE, width=2)
            # invariant route
            d.line((x-125,y+128,x+125,y+128), fill=GREEN, width=10)
            for bx in [x-105,x-30,x+55]:
                d.rounded_rectangle((bx,y+62,bx+52,y+110),10,fill=SAND,outline=LINE,width=1)
            if idx == 0:
                label = "普通城市先成立" if lang=="zh" else "ordinary city first"
                d.text((x,y+28), label, font=F(18,True), fill=GREEN, anchor="mm")
            elif idx == 1:
                d.rounded_rectangle((x+78,y+50,x+143,y+118),14,fill=ORANGE)
                d.line((x+110,y+118,x+110,y+128), fill=ORANGE, width=5)
                d.text((x,y+28), sidecar, font=F(18,True), fill=ORANGE, anchor="mm")
                d.text((x,y+180), "主路不动 / route fixed" if lang=="zh" else "route stays fixed", font=F(17), fill=MUTED, anchor="mm")
            else:
                d.rounded_rectangle((x+78,y+50,x+143,y+118),14,outline=GREEN2,width=3)
                d.line((x+85,y+58,x+136,y+110), fill=GREEN2, width=3)
                d.line((x+136,y+58,x+85,y+110), fill=GREEN2, width=3)
                d.text((x,y+28), "退出后恢复" if lang=="zh" else "ordinary use restored", font=F(18,True), fill=GREEN, anchor="mm")
                draw_wrapped(d,(x-145,y+160),restore,F(16),MUTED,21,4)
        d.text((325,y+105), "→", font=F(40,True), fill=ORANGE)
    d.line((70,1205,1730,1205),fill=LINE,width=2)
    foot = "同一条 ordinary route 穿过全部生命周期；CLEAN EXIT 不是关机，而是空间交还。" if lang=="zh" else "The same ordinary route survives every lifecycle stage; CLEAN EXIT is spatial handback, not merely shutdown."
    d.text((70,1220), foot, font=F(21,True), fill=INK)
    return im


def metrics_figure(lang="zh"):
    reg, bold = fonts(); F=lambda n,b=False: ImageFont.truetype(bold if b else reg,n)
    im=Image.new("RGB",(1800,1120),BG); d=ImageDraw.Draw(im)
    title="v0.16.s 证据面板｜可退出，而不是可关机" if lang=="zh" else "v0.16.s EVIDENCE | REMOVABLE, NOT MERELY SWITCHABLE"
    d.text((70,55),title,font=F(50,True),fill=INK)
    cards=[
        ("4","生命周期阶段" if lang=="zh" else "lifecycle stages","BASE → ATTACH → OPERATE → EXIT"),
        ("9","可退出宿主" if lang=="zh" else "clean-exit hosts","6 buildings + 3 public spaces"),
        ("100%","恢复用途覆盖" if lang=="zh" else "restore-use coverage","ordinary_restore_use documented"),
        ("100%","主路径保留" if lang=="zh" else "route preservation","ROAD-009 / 010 / 011 invariant"),
        ("0","新增 AI 用地" if lang=="zh" else "new AI land-use codes","AI remains a sidecar"),
    ]
    x=70
    for val,lab,note in cards:
        w=322
        d.rounded_rectangle((x,165,x+w,390),26,fill=WHITE,outline=LINE,width=2)
        d.text((x+25,195),val,font=F(54,True),fill=GREEN)
        d.text((x+25,275),lab,font=F(22,True),fill=INK)
        draw_wrapped(d,(x+25,320),note,F(16),MUTED,30,4)
        x += w+22
    d.text((70,465),"LOCKED CITY METRICS / 锁定城市指标",font=F(28,True),fill=INK)
    locked=[("Site / 总体", "11,412,825.386 sqm"),("Green ratio / 绿地率","0.195008"),("Public-space ratio / 公共空间率","0.033824"),("Green area / 绿地面积","2,225,592.728 sqm"),("Public space / 公共空间","386,029.358 sqm"),("Building footprint / 建筑基底","1,024,945.371 sqm")]
    for i,(a,b) in enumerate(locked):
        col=i%3; row=i//3; xx=70+col*565; yy=525+row*145
        d.rounded_rectangle((xx,yy,xx+530,yy+115),20,fill=PALE,outline=LINE,width=1)
        d.text((xx+20,yy+18),a,font=F(18,True),fill=MUTED)
        d.text((xx+20,yy+55),b,font=F(25,True),fill=INK)
    d.rounded_rectangle((70,850,1730,1020),24,fill=WHITE,outline=LINE,width=2)
    msg=("REALITY BOUNDARY：以上 4/9/100% 是提交包内的设计合同覆盖率，不是现场实施绩效。真实安装、拆除、消防、市政、产权与运营必须另行核验。" if lang=="zh" else "REALITY BOUNDARY: 4 / 9 / 100% describe design-contract coverage inside this package, not field performance. Real installation, removal, fire safety, utilities, ownership and operations require separate verification.")
    draw_wrapped(d,(100,885),msg,F(22),INK,100,8)
    return im


def save_figures():
    out=ROOT/"assets/figures"
    lifecycle_figure("zh").save(out/"key-areas.png")
    lifecycle_figure("en").save(out/"key-areas.en.png")
    metrics_figure("zh").save(out/"metrics-evidence.png")
    metrics_figure("en").save(out/"metrics-evidence.en.png")


def visual_html(lang="zh"):
    zh=lang=="zh"
    title="京张城市完整度 v0.16.s｜可退出的 AI 城市" if zh else "JING-ZHANG CITY COMPLETENESS v0.16.s | CLEAN EXIT CITY"
    thesis="AI 不只要能关闭，还必须能被城市完整地撤走。" if zh else "AI must not only switch off; the city must be able to remove it cleanly."
    desc="普通城市先成立；AI 只侧挂；退出后，主路径、人工服务、固定导视与普通用途回到原位。" if zh else "The ordinary city works first; AI attaches laterally; after exit, routes, human service, fixed wayfinding and ordinary uses remain."
    cards=[
        ("ROAD-009 · TEST POCKET","众智园：撤出测试接口，恢复普通院落、工作休息与公共交流。" if zh else "Zhongzhiyuan: remove test interfaces and restore ordinary courtyard, work/rest and exchange."),
        ("ROAD-010 · CARE PORCH","AI 原点：撤出数字层，保留人工帮助、无账号入口与公共首层。" if zh else "AI Origin: remove the digital layer; retain staffed help, account-free entry and public ground floor."),
        ("ROAD-011 · ARRIVAL SIDECAR","大钟寺：撤出动态层，保留固定导视、人工问询与普通等候；REAL LEVEL DATA REQUIRED。" if zh else "Dazhongsi: remove dynamic layer; retain fixed signs, staffed help and ordinary waiting; REAL LEVEL DATA REQUIRED."),
    ]
    cardhtml="".join(f'<article class="card"><h3>{a}</h3><p>{b}</p></article>' for a,b in cards)
    alts=("三处重点区 AI 生命周期图","证据与锁定指标","总体城市结构","用地结构","慢行与蓝绿网络") if zh else ("AI lifecycle across three key areas","Evidence and locked metrics","Overall city structure","Land-use structure","Mobility and blue-green network")
    return f'''<!doctype html><html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{title}</title><style>
:root{{--bg:#f5f1e7;--ink:#203033;--muted:#667477;--green:#2d6b5e;--orange:#d26f3c;--line:#c9c1b5;--white:#fff}}*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--ink);font-family:Arial,"Noto Sans CJK SC",sans-serif;line-height:1.55}}main{{max-width:1480px;margin:auto;padding:42px}}header{{display:grid;grid-template-columns:1.25fr .75fr;gap:28px;align-items:end;border-bottom:2px solid var(--ink);padding-bottom:26px}}.tag{{letter-spacing:.08em;color:var(--green);font-weight:700}}h1{{font-size:58px;line-height:1.05;margin:10px 0 18px}}.thesis{{font-size:28px;font-weight:700;margin:0 0 10px}}.desc{{font-size:19px;color:var(--muted);margin:0}}.rule{{background:var(--ink);color:white;border-radius:24px;padding:26px}}.rule strong{{display:block;color:#f0d9c9;font-size:22px;margin-bottom:8px}}.hero{{margin:30px 0 24px;background:white;border:1px solid var(--line);border-radius:26px;padding:18px}}img{{width:100%;height:auto;display:block;border-radius:16px}}.cards{{display:grid;grid-template-columns:repeat(3,1fr);gap:18px;margin:20px 0 34px}}.card{{background:white;border:1px solid var(--line);border-radius:22px;padding:22px}}.card h3{{font-size:20px;color:var(--orange);margin:0 0 10px}}.card p{{margin:0;color:var(--muted)}}h2{{font-size:30px;margin:40px 0 18px}}.grid{{display:grid;grid-template-columns:1fr 1fr;gap:22px}}figure{{margin:0;background:white;border:1px solid var(--line);padding:15px;border-radius:22px}}figcaption{{font-size:15px;color:var(--muted);padding:10px 5px 0}}footer{{margin-top:36px;border-top:1px solid var(--line);padding-top:20px;color:var(--muted);font-size:14px}}@media(max-width:900px){{header,.cards,.grid{{grid-template-columns:1fr}}h1{{font-size:40px}}main{{padding:22px}}}}</style></head><body><main><header><section><div class="tag">v0.16.s · CLEAN EXIT CITY</div><h1>{title}</h1><p class="thesis">{thesis}</p><p class="desc">{desc}</p></section><aside class="rule"><strong>BASE CITY → ATTACH → OPERATE → CLEAN EXIT</strong>{'CLEAN EXIT 不是“关机”，而是把空间交还给普通城市。' if zh else 'CLEAN EXIT is not shutdown; it is spatial handback to the ordinary city.'}</aside></header><section class="hero"><img src="../assets/figures/key-areas{'.en' if not zh else ''}.png" alt="{alts[0]}"></section><section class="cards">{cardhtml}</section><h2>{'机器证据：退出以后城市还剩什么' if zh else 'Machine Evidence: What Remains After Exit'}</h2><figure><img src="../assets/figures/metrics-evidence{'.en' if not zh else ''}.png" alt="{alts[1]}"></figure><h2>{'城市底盘仍然是主角' if zh else 'The Ordinary City Remains the Host'}</h2><section class="grid"><figure><img src="../assets/figures/site-overview{'.en' if not zh else ''}.png" alt="{alts[2]}"><figcaption>{alts[2]}</figcaption></figure><figure><img src="../assets/figures/land-use-structure{'.en' if not zh else ''}.png" alt="{alts[3]}"><figcaption>{alts[3]}</figcaption></figure><figure><img src="../assets/figures/mobility-bluegreen{'.en' if not zh else ''}.png" alt="{alts[4]}"><figcaption>{alts[4]}</figcaption></figure><figure><img src="../assets/figures/key-areas{'.en' if not zh else ''}.png" alt="{alts[0]}"><figcaption>ROAD-009 / 010 / 011</figcaption></figure></section><footer>{'Reality boundary：site / key-area geometry 仍为 provisional；不虚构站口、高差、桥隧、工程净宽、吞吐量、法定 FAR/高度或已确认实施主体。' if zh else 'Reality boundary: site/key-area geometry remains provisional; no station entrance, level, bridge/tunnel, engineering clearance, throughput, statutory FAR/height or confirmed implementation actor is fabricated.'}</footer></main></body></html>'''


def write_visuals():
    (ROOT/"visual/index.html").write_text(visual_html("zh"),encoding="utf-8")
    (ROOT/"visual/index.en.html").write_text(visual_html("en"),encoding="utf-8")


def build_pdf(path: Path, page_size, lang="zh"):
    zh=lang=="zh"
    try:
        pdfmetrics.registerFont(UnicodeCIDFont("STSong-Light"))
    except Exception:
        pass
    font="STSong-Light" if zh else "Helvetica"
    bold=font if zh else "Helvetica-Bold"
    c=canvas.Canvas(str(path),pagesize=landscape(page_size))
    W,H=landscape(page_size)
    pages=[
        ("CLEAN EXIT CITY / 可退出的 AI 城市" if zh else "CLEAN EXIT CITY", ROOT/"assets/figures"/("key-areas.png" if zh else "key-areas.en.png")),
        ("普通城市底盘 / ORDINARY CITY HOST" if zh else "ORDINARY CITY HOST", ROOT/"assets/figures"/("site-overview.png" if zh else "site-overview.en.png")),
        ("证据与退出合同 / EVIDENCE + EXIT CONTRACT" if zh else "EVIDENCE + EXIT CONTRACT", ROOT/"assets/figures"/("metrics-evidence.png" if zh else "metrics-evidence.en.png")),
        ("用地结构 / LAND USE" if zh else "LAND USE", ROOT/"assets/figures"/("land-use-structure.png" if zh else "land-use-structure.en.png")),
        ("慢行与蓝绿 / MOBILITY + BLUE-GREEN" if zh else "MOBILITY + BLUE-GREEN", ROOT/"assets/figures"/("mobility-bluegreen.png" if zh else "mobility-bluegreen.en.png")),
    ]
    for title,img in pages:
        c.setFillColorRGB(0.965,0.945,0.905); c.rect(0,0,W,H,fill=1,stroke=0)
        c.setFillColorRGB(0.12,0.19,0.20); c.setFont(bold,24 if page_size==A3 else 44); c.drawString(38,H-48,title)
        c.setFont(font,10 if page_size==A3 else 18); c.setFillColorRGB(0.35,0.43,0.44); c.drawRightString(W-38,H-44,"v0.16.s · BASE → ATTACH → OPERATE → CLEAN EXIT")
        iw,ih=Image.open(img).size; maxw=W-76; maxh=H-100; scale=min(maxw/iw,maxh/ih); dw,dh=iw*scale,ih*scale
        c.drawImage(ImageReader(str(img)),(W-dw)/2,(H-dh)/2-18,width=dw,height=dh,preserveAspectRatio=True,mask="auto")
        c.showPage()
    c.save()


def write_pdfs():
    build_pdf(ROOT/"drawings/a3-booklet.pdf",A3,"zh")
    build_pdf(ROOT/"drawings/a3-booklet.en.pdf",A3,"en")
    build_pdf(ROOT/"drawings/a0-boards.pdf",A0,"zh")
    build_pdf(ROOT/"drawings/a0-boards.en.pdf",A0,"en")


def main():
    if not ROOT.is_dir():
        raise SystemExit(f"submission missing: {ROOT}")
    update_proposals()
    update_agent_and_changelog()
    update_geometry()
    update_metrics()
    update_contract()
    update_matrices()
    save_figures()
    write_visuals()
    write_pdfs()
    print("v0.16.s CLEAN EXIT CITY build: DONE")


if __name__ == "__main__":
    main()
