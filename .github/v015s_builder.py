#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
from reportlab.lib.pagesizes import A0, A3, landscape
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

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


def load_json(rel: str):
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


def save_json(rel: str, data) -> None:
    (ROOT / rel).write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def replace_marker_block(text: str, starts: list[str], ends: list[str], new_block: str) -> str:
    for start, end in zip(starts, ends):
        if start in text and end in text:
            a = text.index(start)
            b = text.index(end, a) + len(end)
            return text[:a] + new_block + text[b:]
    raise RuntimeError(f"marker block not found: {starts}")


def replace_once(text: str, pattern: str, replacement: str, label: str) -> str:
    updated, count = re.subn(pattern, replacement, text, count=1, flags=re.S)
    if count != 1:
        raise RuntimeError(f"expected one replacement for {label}, got {count}")
    return updated


ZH_CORE = r'''<!-- V015-CORE-START -->
## v0.15.s 核心判断｜AI SIDECAR CITY / AI 侧挂城市

**普通城市是主机，AI 只能侧挂。** v0.14.s 已经证明三条 ordinary civic route 在 AI 关闭时仍然成立；v0.15.s 进一步把 AI 的实体落点写进既有建筑、公共空间与路线属性，而不是再创造一层“AI 专用城市”。[metric:invariant_civic_route_count] [metric:ai_sidecar_type_count]

**AI OFF = 完整城市；AI ON = 完整城市 + 可逆侧挂能力。** ROAD-009 / 010 / 011 的几何在 ON/OFF 两态保持不变，变化只发生在主路径侧边的测试、照护与到达接口。[metric:ai_off_route_preservation_ratio] [metric:new_ai_land_use_code_count]

| 重点区 | 普通城市主机 | AI sidecar | 机器可读宿主 | 拆掉 sidecar 后 |
| --- | --- | --- | --- | --- |
| 众智园 / `ROAD-009` | 研发首层—吃饭休息—公共绿脊—开放交流 | **TEST POCKET / 测试侧院**：受控测试、临时设备、可替换服务接口退到主路侧边 | `BLDG-012` + `BLDG-013` + `PUBLIC-006` | 工作、休息与公共交流仍沿同一路线完成 |
| AI 原点 / `ROAD-010` | 居住—遮阴停留—人工帮助/共学—社区客厅 | **CARE PORCH / 照护门廊**：自愿导航、服务匹配、照护提示附着于公共首层与社区界面 | `BLDG-007` + `BLDG-009` + `PUBLIC-004` | 不登录、不授权数据仍可到达人、服务与公共生活 |
| 大钟寺 / `ROAD-011` | 到达—固定导视—人工问询—普通等候/商业—京张公共界面 | **ARRIVAL SIDECAR / 到达侧带**：动态翻译、信息提示与客流辅助只做增强 | `BLDG-001` + `BLDG-002` + `PUBLIC-001` | 不用 App、动态信息失效时仍能识路、求助、等待和离开 |

九个宿主 feature 只新增语义属性，不改 Polygon；三条路线只新增 sidecar 关系，不改 LineString。因此 site、green、public-space、building-footprint 六项锁定面积指标不因本轮发生变化。[metric:ai_sidecar_host_feature_count] [metric:sidecar_host_public_space_count]

大钟寺仍坚持 **REAL LEVEL DATA REQUIRED**：当前 sidecar 只是关系型到达界面，不虚构真实站口、高差、桥隧、通廊净宽、吞吐量或运营承诺。[data:geometry/key_areas.geojson#PROV-KEY-003]

![AI OFF 与 AI ON 使用同一座城市：三条主路不动，sidecar 只在侧边出现](assets/figures/key-areas.png)
<!-- V015-CORE-END -->'''

EN_CORE = r'''<!-- V015-CORE-START -->
## v0.15.s Core Judgment | AI SIDECAR CITY

**The ordinary city is the host. AI is only a sidecar.** v0.14.s established three ordinary civic routes that survive AI shutdown. v0.15.s now writes the physical AI attachment points into existing building, public-space and route attributes instead of inventing an AI-only city layer. [metric:invariant_civic_route_count] [metric:ai_sidecar_type_count]

**AI OFF = a complete city; AI ON = the same complete city plus reversible sidecar capability.** The geometry of ROAD-009 / 010 / 011 is identical in both states. Only lateral test, care and arrival interfaces change. [metric:ai_off_route_preservation_ratio] [metric:new_ai_land_use_code_count]

| Key area | Ordinary-city host | AI sidecar | Machine-readable hosts | After the sidecar is removed |
| --- | --- | --- | --- | --- |
| Zhongzhiyuan / `ROAD-009` | R&D ground floor - food/rest - green spine - public exchange | **TEST POCKET**: controlled tests, temporary equipment and replaceable service interfaces stay beside the ordinary route | `BLDG-012` + `BLDG-013` + `PUBLIC-006` | Work, rest and public exchange continue on the same route |
| AI Origin / `ROAD-010` | Home - shade/stay - human help/learning - civic commons | **CARE PORCH**: opt-in navigation, service matching and care prompts attach to public ground floors and community interfaces | `BLDG-007` + `BLDG-009` + `PUBLIC-004` | Refusing login or data consent still reaches people, services and common life |
| Dazhongsi / `ROAD-011` | Arrival - fixed wayfinding - staffed help - ordinary waiting/retail - Jing-Zhang public interface | **ARRIVAL SIDECAR**: dynamic translation, information and crowd assistance remain enhancements only | `BLDG-001` + `BLDG-002` + `PUBLIC-001` | Without an app or dynamic information, visitors can still orient, ask, wait and leave |

The nine host features receive semantic properties only; their polygons do not change. The three routes receive sidecar relationships only; their LineStrings do not change. The six locked area metrics therefore remain untouched by this iteration. [metric:ai_sidecar_host_feature_count] [metric:sidecar_host_public_space_count]

Dazhongsi remains **REAL LEVEL DATA REQUIRED**. The sidecar is a relationship-based arrival interface, not a fabricated station entrance, level, bridge/tunnel, corridor width, throughput or operating commitment. [data:geometry/key_areas.geojson#PROV-KEY-003]

![AI OFF and AI ON use the same city: invariant routes stay fixed while sidecars appear laterally](assets/figures/key-areas.en.png)
<!-- V015-CORE-END -->'''

ZH_KEY_AREAS = {
    "z": "**众智园：完整创新校园 + TEST POCKET / 测试侧院。** 科研、中试、孵化和企业服务仍是核心，但普通工作、吃饭休息、公共绿脊和开放交流必须先形成同一条可读的日常链。`ROAD-009` 是不依赖 AI 的普通主路；`BLDG-012`、`BLDG-013` 与 `PUBLIC-006` 作为 sidecar 宿主，只承担可关闭的测试、临时设备和可替换服务接口。真实测试边界、净距、速度、急停、许可与安全性能均须现场调查和专业审查后确定，本案不预设工程数值。[data:geometry/roads.geojson#ROAD-009] [data:geometry/buildings.geojson#BLDG-012] [data:geometry/public_space.geojson#PUBLIC-006]",
    "o": "**AI 原点社区：完整长期社区 + CARE PORCH / 照护门廊。** 住宅、共学、人工帮助、普通商业、绿地和社区客厅构成无需账号即可完成的日常链。`ROAD-010` 保持为 ordinary-city route；`BLDG-007`、`BLDG-009` 与 `PUBLIC-004` 的公共首层/公共界面承载自愿导航、服务匹配和照护提示。真实无障碍尺寸、服务半径、人员配置与响应时间必须由现场和运营资料确认；本案只锁定“拒绝登录或数据授权时，同一实体路径仍能到达人和服务”。[data:geometry/roads.geojson#ROAD-010] [data:geometry/buildings.geojson#BLDG-007] [data:geometry/public_space.geojson#PUBLIC-004]",
    "d": "**大钟寺：完整站城到达 + ARRIVAL SIDECAR / 到达侧带。** 普通到达、固定导视、人工问询、等候/商业和京张公共界面构成主机；动态翻译、信息提示和客流辅助只从侧边增强 `ROAD-011`。`BLDG-001`、`BLDG-002` 与 `PUBLIC-001` 是概念级宿主关系。由于 `PROV-KEY-003` 存在已知绝对位置风险，真实站口、高差、桥隧、竖向交通、通廊净宽、客流能力和权属运营全部标记为 **REAL LEVEL DATA REQUIRED**，不以概念图代替工程证据。[data:geometry/roads.geojson#ROAD-011] [data:geometry/public_space.geojson#PUBLIC-001] [data:geometry/key_areas.geojson#PROV-KEY-003]",
}

EN_KEY_AREAS = {
    "z": "**Zhongzhiyuan: complete innovation campus + TEST POCKET.** Research, pilot work, incubation and enterprise services remain central, but ordinary work, food/rest, the public green spine and open exchange must first form one legible daily chain. `ROAD-009` is the AI-independent host route. `BLDG-012`, `BLDG-013` and `PUBLIC-006` are sidecar hosts for stoppable tests, temporary equipment and replaceable service interfaces only. Real test boundaries, clearances, speeds, emergency-stop design, permits and safety performance require field survey and professional review; this proposal does not pre-set engineering values. [data:geometry/roads.geojson#ROAD-009] [data:geometry/buildings.geojson#BLDG-012] [data:geometry/public_space.geojson#PUBLIC-006]",
    "o": "**AI Origin Community: complete long-term neighborhood + CARE PORCH.** Homes, shared learning, human help, ordinary retail, green space and civic commons form an account-free everyday chain. `ROAD-010` remains the ordinary-city host route. Public-ground-floor and commons interfaces in `BLDG-007`, `BLDG-009` and `PUBLIC-004` host opt-in navigation, service matching and care prompts. Real accessibility dimensions, service catchments, staffing and response times require field and operating evidence; the proposal fixes only the rule that refusing login or data consent still reaches people and services on the same physical route. [data:geometry/roads.geojson#ROAD-010] [data:geometry/buildings.geojson#BLDG-007] [data:geometry/public_space.geojson#PUBLIC-004]",
    "d": "**Dazhongsi: complete station-city arrival + ARRIVAL SIDECAR.** Ordinary arrival, fixed wayfinding, staffed help, waiting/retail and the Jing-Zhang public interface form the host. Dynamic translation, information and crowd assistance remain lateral enhancements to `ROAD-011`. `BLDG-001`, `BLDG-002` and `PUBLIC-001` are conceptual host relationships only. Because `PROV-KEY-003` has a known absolute-location risk, real station entrances, levels, bridges/tunnels, vertical circulation, corridor widths, passenger capacity, ownership and operations remain **REAL LEVEL DATA REQUIRED** rather than being fabricated from concept geometry. [data:geometry/roads.geojson#ROAD-011] [data:geometry/public_space.geojson#PUBLIC-001] [data:geometry/key_areas.geojson#PROV-KEY-003]",
}

ZH_SIDECAR_SECTION = r'''<!-- V015-SIDECAR-START -->
### v0.15.s｜AI SIDECAR CITY：让 AI 有空间，但没有城市主权

v0.15.s 不新增第四条路线，也不创造“AI 专用用地”。它把 v0.7 的六类可逆 AI 城市形态原型重新归并成三个可读的 sidecar：**TEST POCKET、CARE PORCH、ARRIVAL SIDECAR**。普通城市空间是 host；AI 只改变侧向接口、公共首层关系和可替换服务节点。[metric:ai_sidecar_type_count] [metric:new_ai_land_use_code_count]

| Sidecar | 对应可逆原型 | 宿主 feature | AI OFF | AI ON 的实体变化 | 删除测试 |
| --- | --- | --- | --- | --- | --- |
| TEST POCKET | 受控测试口袋 + 可替换服务节点 | `BLDG-012` / `BLDG-013` / `PUBLIC-006` | 工作、休息、绿脊、交流连续 | 侧院/服务边出现可关闭测试与临时设备接口 | 删除接口，不迁移 `ROAD-009` |
| CARE PORCH | 人优先公共首层 + 无障碍/人工求助节点 | `BLDG-007` / `BLDG-009` / `PUBLIC-004` | 居住、人工帮助、共学、公共客厅连续 | 公共首层增加自愿导航/服务匹配提示 | 删除接口，不要求账号、不迁移 `ROAD-010` |
| ARRIVAL SIDECAR | 连续站城到达界面 + 固定/人工基线 | `BLDG-001` / `BLDG-002` / `PUBLIC-001` | 固定导视、人工问询、等候/商业连续 | 侧带增加动态翻译与信息辅助 | 关闭动态层，不迁移 `ROAD-011` |

第六类“可回退空间版本链”成为三个 sidecar 的共同实施方法：**观察 → 小范围样段 → 公共/专业复核 → 合并或回退**。它不是软件状态机，而是对可拆构件、公共首层接口、测试边界和导视层级的物理版本管理。[metric:ai_sidecar_host_feature_count]

#### 两条实施路径保持不变
**路径 A｜低扰动可逆动作**：遮阴、座椅、固定导视、人工帮助界面、可拆测试边界、模块化服务节点，可进入现场调查—样段—复核—扩大/撤回的渐进流程。**路径 B｜正式项目依赖动作**：建筑规模、站城竖向、市政容量、道路工程、消防、文保、权属等，必须等待真实项目生成、专业设计与行政许可。[metric:implementation_path_count]

责任仍只写到“拟议角色”级。大钟寺竖向连续性继续标记 **REAL LEVEL DATA REQUIRED**，不虚构桥隧、站口、多层甲板或工程通廊参数。
<!-- V015-SIDECAR-END -->'''

EN_SIDECAR_SECTION = r'''<!-- V015-SIDECAR-START -->
### v0.15.s | AI SIDECAR CITY: give AI space without giving it urban sovereignty

v0.15.s adds neither a fourth route nor an AI-only land-use category. It regroups the six reversible AI urban-form prototypes from v0.7 into three legible sidecars: **TEST POCKET, CARE PORCH, and ARRIVAL SIDECAR**. Ordinary urban space is the host; AI changes only lateral interfaces, public-ground-floor relationships and replaceable service nodes. [metric:ai_sidecar_type_count] [metric:new_ai_land_use_code_count]

| Sidecar | Reversible prototypes | Host features | AI OFF | Physical AI ON delta | Removal test |
| --- | --- | --- | --- | --- | --- |
| TEST POCKET | bounded test pocket + replaceable service node | `BLDG-012` / `BLDG-013` / `PUBLIC-006` | work, rest, green spine and public exchange remain continuous | stoppable test and temporary-equipment interfaces appear at side yards/service edges | remove the interface without relocating `ROAD-009` |
| CARE PORCH | people-first public ground floor + accessible/human help node | `BLDG-007` / `BLDG-009` / `PUBLIC-004` | home, human help, learning and civic commons remain continuous | opt-in navigation/service-matching prompts attach to public ground floors | remove the interface without login and without relocating `ROAD-010` |
| ARRIVAL SIDECAR | continuous arrival interface + fixed/human baseline | `BLDG-001` / `BLDG-002` / `PUBLIC-001` | fixed wayfinding, staffed help and ordinary waiting/retail remain continuous | dynamic translation and information assistance appear laterally | switch off the dynamic layer without relocating `ROAD-011` |

The sixth prototype, the reversible spatial version chain, becomes a shared implementation method for all three sidecars: **observe → bounded sample → public/professional review → merge or roll back**. It manages detachable components, public-ground-floor interfaces, test boundaries and wayfinding layers as physical versions rather than as a software state machine. [metric:ai_sidecar_host_feature_count]

#### Two implementation paths remain
**Path A | low-disturbance reversible actions:** shade, seating, fixed wayfinding, staffed-help interfaces, detachable test boundaries and modular service nodes can move through field survey, sample, review and expand/withdraw cycles. **Path B | formal-project-dependent actions:** building capacity, station-city vertical circulation, utilities, road engineering, fire safety, heritage and ownership require real project evidence, professional design and approval. [metric:implementation_path_count]

Responsibility remains at proposed-role level only. Dazhongsi vertical continuity stays **REAL LEVEL DATA REQUIRED**; no bridge/tunnel, station entrance, multi-level deck or engineering corridor parameter is fabricated.
<!-- V015-SIDECAR-END -->'''


def update_proposals() -> None:
    zh_path = ROOT / "proposal.md"
    en_path = ROOT / "proposal.en.md"
    zh = zh_path.read_text(encoding="utf-8")
    en = en_path.read_text(encoding="utf-8")

    zh = zh.replace('summary: "以城市完整度作为百年京张AI创新带的空间审查方法：七项普通城市能力先形成长期底盘；v0.14.s 用三条机器可读的不绕行主路径把众智园、AI原点与大钟寺的日常城市链写进真实方案几何，AI只能作为侧挂、可选、可退出的空间接口进入。"',
                    'summary: "以城市完整度作为百年京张AI创新带的空间审查方法：v0.15.s 将普通城市视为主机、AI视为可逆 sidecar；三条不绕行主路保持不变，测试、照护和到达增强只附着于九个既有建筑/公共空间宿主，不创造AI专用用地。"')
    zh = zh.replace('iteration: "v0.14"', 'iteration: "v0.15"', 1)
    en = en.replace('summary: "City Completeness keeps seven ordinary-city capabilities as the durable base. v0.14.s writes three machine-readable invariant civic routes into the proposal geometry for Zhongzhiyuan, AI Origin and Dazhongsi; AI may enter only as optional, lateral and reversible spatial interfaces."',
                    'summary: "City Completeness treats the ordinary city as the host and AI as a reversible sidecar. v0.15.s keeps three invariant routes fixed while test, care and arrival enhancements attach only to nine existing building/public-space hosts, with no AI-only land-use category."')
    en = en.replace('iteration: "v0.14"', 'iteration: "v0.15"', 1)

    zh = replace_marker_block(zh, ["<!-- V014-CORE-START -->", "<!-- V015-CORE-START -->"], ["<!-- V014-CORE-END -->", "<!-- V015-CORE-END -->"], ZH_CORE)
    en = replace_marker_block(en, ["<!-- V014-CORE-START -->", "<!-- V015-CORE-START -->"], ["<!-- V014-CORE-END -->", "<!-- V015-CORE-END -->"], EN_CORE)

    zh = replace_once(zh, r"\*\*众智园：.*?\[data:geometry/key_areas\.geojson#PROV-KEY-001\]", ZH_KEY_AREAS["z"], "ZH Zhongzhiyuan detail")
    zh = replace_once(zh, r"\*\*AI 原点社区：.*?\[data:geometry/key_areas\.geojson#PROV-KEY-002\]", ZH_KEY_AREAS["o"], "ZH AI Origin detail")
    zh = replace_once(zh, r"\*\*大钟寺：.*?\[depth:three_key_area_detailed_design\]", ZH_KEY_AREAS["d"] + " [depth:three_key_area_detailed_design]", "ZH Dazhongsi detail")

    en = replace_once(en, r"\*\*Zhongzhiyuan:.*?\[data:geometry/key_areas\.geojson#PROV-KEY-001\]", EN_KEY_AREAS["z"], "EN Zhongzhiyuan detail")
    en = replace_once(en, r"\*\*AI Origin Community:.*?\[data:geometry/key_areas\.geojson#PROV-KEY-002\]", EN_KEY_AREAS["o"], "EN AI Origin detail")
    en = replace_once(en, r"\*\*Dazhongsi:.*?\[depth:three_key_area_detailed_design\]", EN_KEY_AREAS["d"] + " [depth:three_key_area_detailed_design]", "EN Dazhongsi detail")

    zh = replace_marker_block(zh, ["<!-- V012-CONTRACTS-START -->", "<!-- V015-SIDECAR-START -->"], ["<!-- V012-CONTRACTS-END -->", "<!-- V015-SIDECAR-END -->"], ZH_SIDECAR_SECTION)
    en = replace_marker_block(en, ["<!-- V012-CONTRACTS-START -->", "<!-- V015-SIDECAR-START -->"], ["<!-- V012-CONTRACTS-END -->", "<!-- V015-SIDECAR-END -->"], EN_SIDECAR_SECTION)

    zh = zh.replace(
        "AI 对城市形态的影响被压缩为六类可逆空间原型：测试口袋、无障碍求助节点、连续站城到达界面、可替换小型服务节点、人优先的公共首层，以及“观察—小范围原型—公共/专业复核—合并或回退”的可回退空间版本链。这回答的是 AI 如何改变空间组织和规划方法，而不是如何给既有空间附加更多数字界面。",
        "AI 对城市形态的影响仍由六类可逆空间原型承担：测试口袋、无障碍/人工求助节点、连续站城到达界面、可替换服务节点、人优先公共首层，以及可回退空间版本链。v0.15.s 进一步把前五类归并成 TEST POCKET、CARE PORCH、ARRIVAL SIDECAR 三种可读接口，并把宿主 feature 写进 geometry；第六类则成为三个 sidecar 共用的物理版本管理方法。这样 AI 的空间增量可以被定位、关闭、拆除和复核，而普通城市主机不必重画。[metric:ai_sidecar_type_count] [metric:ai_sidecar_host_feature_count]"
    )
    en = en.replace(
        "The spatial effect of AI is reduced to six reversible prototypes: test pockets, accessible help nodes, continuous station-city arrival interfaces, replaceable small service nodes, people-first public ground floors, and a reversible spatial version chain—observe, bounded prototype, public/professional review, merge or rollback. This answers how AI changes spatial organization and planning method rather than merely attaching more digital interfaces to existing space.",
        "AI still changes urban form through six reversible prototypes: test pockets, accessible/human help nodes, continuous station-city arrival interfaces, replaceable service nodes, people-first public ground floors, and a reversible spatial version chain. v0.15.s regroups the first five into three legible interfaces—TEST POCKET, CARE PORCH and ARRIVAL SIDECAR—and writes their host features into geometry; the sixth becomes their shared physical version-management method. AI's spatial delta can therefore be located, switched off, removed and reviewed without redrawing the ordinary-city host. [metric:ai_sidecar_type_count] [metric:ai_sidecar_host_feature_count]"
    )

    forbidden_zh = ["3.5m", "2.0m", "1.8m", "400m", "气动升降桩", "多层立体站城甲板", "$\\ge 4.5", "$\\ge 2.5"]
    forbidden_en = ["3.5m", "2.0m", "1.8m", "400m", "+15cm", "retractable bollards", "multi-level transit deck", "$\\ge 4.5", "$\\ge 2.5"]
    for token in forbidden_zh:
        if token in zh:
            raise RuntimeError(f"unsupported precision remains in ZH proposal: {token}")
    for token in forbidden_en:
        if token in en:
            raise RuntimeError(f"unsupported precision remains in EN proposal: {token}")

    zh_path.write_text(zh, encoding="utf-8")
    en_path.write_text(en, encoding="utf-8")


def update_geometry() -> None:
    building_map = {
        "BLDG-012": ("ROAD-009", "test_pocket", "research_ground_floor_host", "ordinary research/work entry remains available", "stoppable test or sensing interface attaches at the service edge"),
        "BLDG-013": ("ROAD-009", "test_pocket", "replaceable_service_host", "enterprise/public service entry remains ordinary", "replaceable test/service module may attach without occupying the route"),
        "BLDG-007": ("ROAD-010", "care_porch", "residential_public_ground_floor_host", "home access and ordinary ground-floor use remain account-free", "opt-in service matching or care prompt may attach at the public interface"),
        "BLDG-009": ("ROAD-010", "care_porch", "human_help_learning_host", "shared learning and human help remain available", "optional navigation/service prompts may attach without becoming a gate"),
        "BLDG-001": ("ROAD-011", "arrival_sidecar", "heritage_orientation_host", "heritage/public orientation remains readable with static information", "dynamic translation or interpretation may supplement the fixed layer"),
        "BLDG-002": ("ROAD-011", "arrival_sidecar", "waiting_retail_host", "ordinary waiting/retail remains usable", "dynamic arrival information may attach laterally to the public ground floor"),
    }
    public_map = {
        "PUBLIC-006": ("ROAD-009", "test_pocket", "bounded_public_test_edge", "public exchange remains open with testing off", "temporary controlled-test interface may occupy only a lateral pocket"),
        "PUBLIC-004": ("ROAD-010", "care_porch", "community_help_commons", "community commons and human help remain account-free", "opt-in navigation/care prompts may attach to a staffed interface"),
        "PUBLIC-001": ("ROAD-011", "arrival_sidecar", "fixed_wayfinding_arrival_commons", "fixed wayfinding and human help remain the baseline", "dynamic translation/information may supplement but not replace the baseline"),
    }
    for rel, mapping in [("geometry/buildings.geojson", building_map), ("geometry/public_space.geojson", public_map)]:
        data = load_json(rel)
        seen = set()
        for feat in data.get("features", []):
            fid = str(feat.get("id") or feat.get("properties", {}).get("id"))
            if fid not in mapping:
                continue
            route, sidecar, role, off, delta = mapping[fid]
            props = feat.setdefault("properties", {})
            props.update({
                "civic_route_id": route,
                "ai_sidecar_type": sidecar,
                "ai_sidecar_host_role": role,
                "ai_off_baseline": off,
                "ai_on_delta": delta,
                "reversibility": "remove_sidecar_without_relocating_ordinary_route",
                "evidence_boundary": "conceptual spatial relationship only; field, operating and engineering evidence required before implementation",
            })
            seen.add(fid)
        missing = set(mapping) - seen
        if missing:
            raise RuntimeError(f"missing sidecar hosts in {rel}: {sorted(missing)}")
        save_json(rel, data)

    roads = load_json("geometry/roads.geojson")
    route_map = {
        "ROAD-009": ("test_pocket", ["BLDG-012", "BLDG-013", "PUBLIC-006"]),
        "ROAD-010": ("care_porch", ["BLDG-007", "BLDG-009", "PUBLIC-004"]),
        "ROAD-011": ("arrival_sidecar", ["BLDG-001", "BLDG-002", "PUBLIC-001"]),
    }
    seen = set()
    for feat in roads.get("features", []):
        fid = str(feat.get("id") or feat.get("properties", {}).get("id"))
        if fid not in route_map:
            continue
        sidecar, hosts = route_map[fid]
        props = feat.setdefault("properties", {})
        props.update({
            "ai_sidecar_type": sidecar,
            "ai_sidecar_host_ids": hosts,
            "ai_off_state": "ordinary_route_geometry_unchanged",
            "ai_on_delta": "sidecar_interfaces_only_route_geometry_unchanged",
            "route_geometry_changes_when_ai_on": False,
            "sidecar_policy": "AI may attach laterally but may not become a gate or reroute the ordinary journey",
        })
        seen.add(fid)
    if set(route_map) != seen:
        raise RuntimeError(f"missing invariant routes: {sorted(set(route_map)-seen)}")
    save_json("geometry/roads.geojson", roads)


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


def update_metrics() -> None:
    data = load_json("metrics.json")
    m = data.setdefault("metrics", {})
    m["ai_sidecar_type_count"] = metric(3, "count", ["proposal.md", "geometry/buildings.geojson", "geometry/public_space.geojson"], "count(test_pocket, care_porch, arrival_sidecar)", assumptions=["Internal design typologies, not statutory land-use or building categories."])
    m["ai_sidecar_host_feature_count"] = metric(9, "count", ["geometry/buildings.geojson", "geometry/public_space.geojson"], "count(features with ai_sidecar_type among selected v0.15.s hosts)", assumptions=["Counts conceptual host relationships only; no field-installed AI interface is claimed."])
    m["sidecar_host_public_space_count"] = metric(3, "count", ["geometry/public_space.geojson"], "count(PUBLIC-001, PUBLIC-004, PUBLIC-006 as sidecar hosts)", assumptions=["Conceptual public-space host relations only."])
    m["ai_off_route_preservation_ratio"] = metric(1.0, "ratio", ["geometry/roads.geojson", "proposal.md"], "invariant routes whose geometry is unchanged between AI OFF and AI ON / 3", assumptions=["Design-rule test; not a field performance claim."])
    m["new_ai_land_use_code_count"] = metric(0, "count", ["geometry/land_use.geojson", "proposal.md"], "count(land-use codes created solely for AI in v0.15.s)", assumptions=["AI is represented as an optional interface layer, not a new statutory land-use class."])
    save_json("metrics.json", data)


def update_contract() -> None:
    data = {
        "schema_version": "1.5",
        "variant": "v0.15.s",
        "title_zh": "AI侧挂城市 / AI SIDECAR CITY",
        "status": "concept_spatial_sidecar_with_evidence_boundaries",
        "principle": "The ordinary city is the host. AI is only a reversible sidecar.",
        "off_on_rule": "AI OFF is a complete city; AI ON is the same city plus lateral reversible capability. Ordinary route geometry does not change.",
        "contracts": [
            {
                "id": "ASC-01",
                "place": "众智园 / Zhongzhiyuan",
                "ordinary_route_id": "ROAD-009",
                "sidecar_type": "test_pocket",
                "host_feature_ids": ["BLDG-012", "BLDG-013", "PUBLIC-006"],
                "ai_off": "work, meal/rest, green spine and public exchange remain continuous",
                "ai_on_delta": "stoppable test, temporary equipment and replaceable service interfaces attach at side yards/service edges",
                "remove_test": "remove the sidecar without relocating ROAD-009",
                "evidence_required": ["field survey of entrances/desire lines", "professional safety review for any real test interface"],
                "reality_boundary": "No lane width, speed, emergency-stop timing, bollard design or permit is claimed."
            },
            {
                "id": "ASC-02",
                "place": "AI 原点 / AI Origin",
                "ordinary_route_id": "ROAD-010",
                "sidecar_type": "care_porch",
                "host_feature_ids": ["BLDG-007", "BLDG-009", "PUBLIC-004"],
                "ai_off": "home, human help, shared learning and civic commons remain account-free",
                "ai_on_delta": "opt-in navigation, service matching and care prompts attach to public-ground-floor/community interfaces",
                "remove_test": "remove the sidecar without login requirements or relocating ROAD-010",
                "evidence_required": ["accessibility survey", "service capacity and operating-role confirmation"],
                "reality_boundary": "No service radius, accessibility dimension, staffing level or response-time performance is claimed."
            },
            {
                "id": "ASC-03",
                "place": "大钟寺 / Dazhongsi",
                "ordinary_route_id": "ROAD-011",
                "sidecar_type": "arrival_sidecar",
                "host_feature_ids": ["BLDG-001", "BLDG-002", "PUBLIC-001"],
                "ai_off": "fixed wayfinding, staffed help, ordinary waiting/retail and the Jing-Zhang public interface remain usable",
                "ai_on_delta": "dynamic translation, information and crowd assistance attach laterally",
                "remove_test": "switch off dynamic information without relocating ROAD-011",
                "evidence_required": ["verified station entrances and real level data", "passenger-flow, ownership and operating evidence before engineering design"],
                "reality_boundary": "PROV-KEY-003 has known absolute-location risk; no station entrance, bridge/tunnel, level, corridor width or throughput is claimed."
            }
        ]
    }
    save_json("visual/assets/public-promises-contract.json", data)


def add_unique(arr, values):
    if not isinstance(arr, list):
        return
    for value in values:
        if value not in arr:
            arr.append(value)


def update_matrices() -> None:
    old14_zh = "v0.14.s 核心判断｜INVARIANT CIVIC ROUTES / 不绕行的 AI 城市"
    new15_zh = "v0.15.s 核心判断｜AI SIDECAR CITY / AI 侧挂城市"
    old14_en = "v0.14.s Core Judgment | INVARIANT CIVIC ROUTES"
    new15_en = "v0.15.s Core Judgment | AI SIDECAR CITY"

    for rel in ["design_depth_matrix.json", "compliance_matrix.json"]:
        data = load_json(rel)
        items = data.get("items", data.get("requirements", []))
        if not isinstance(items, list):
            raise RuntimeError(f"unexpected matrix schema: {rel}")
        for item in items:
            if not isinstance(item, dict):
                continue
            for key in ["proposal_sections", "report_sections"]:
                sections = item.get(key)
                if not isinstance(sections, list):
                    continue
                cleaned = []
                for sec in sections:
                    if not isinstance(sec, str):
                        cleaned.append(sec); continue
                    if "v0.13.g" in sec or "DUAL-TRACK SPATIAL CONTRACTS" in sec:
                        continue
                    if sec == old14_zh:
                        sec = new15_zh
                    if sec == old14_en:
                        sec = new15_en
                    if sec not in cleaned:
                        cleaned.append(sec)
                item[key] = cleaned

            iid = str(item.get("item_id") or item.get("requirement_id") or item.get("id") or "")
            title = " ".join(str(item.get(k, "")) for k in ["title_zh", "title_en", "title", "requirement"])
            sections_text = " ".join(str(x) for key in ["proposal_sections", "report_sections"] for x in (item.get(key) or []) if isinstance(x, str))
            relevant = any(token in (iid + " " + title + " " + sections_text) for token in ["overall_spatial", "three_key_area", "重点区域", "Key Areas", "traffic", "交通", "AI", "blue_green", "公共空间", "urban form", "城市形态"])
            if relevant:
                add_unique(item.setdefault("geometry_refs", []), ["geometry/roads.geojson", "geometry/buildings.geojson", "geometry/public_space.geojson"])
                add_unique(item.setdefault("metric_refs", []), ["ai_sidecar_type_count", "ai_sidecar_host_feature_count", "ai_off_route_preservation_ratio", "new_ai_land_use_code_count"])
                if rel == "design_depth_matrix.json":
                    add_unique(item.setdefault("proposal_sections", []), [new15_zh])
                else:
                    add_unique(item.setdefault("report_sections", []), [new15_zh])
                key = "evidence_summary_zh"
                if isinstance(item.get(key), str) and "v0.15.s" not in item[key]:
                    item[key] += " v0.15.s 将 AI 空间增量写成三个可逆 sidecar，并把九个宿主 feature 与三条不绕行路线建立机器可读关系；AI ON/OFF 不改普通路线几何，也不新增 AI 专用用地。"
        save_json(rel, data)


def find_font(bold=False):
    candidates = [
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc" if bold else "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for p in candidates:
        if Path(p).is_file():
            return p
    raise RuntimeError("no usable font found")

FONT_REG = None
FONT_BOLD = None

def font(size, bold=False):
    global FONT_REG, FONT_BOLD
    if FONT_REG is None:
        FONT_REG = find_font(False)
        FONT_BOLD = find_font(True)
    return ImageFont.truetype(FONT_BOLD if bold else FONT_REG, size=size)


def text(draw, xy, value, size, fill=INK, bold=False, anchor=None, spacing=8, align="left"):
    draw.multiline_text(xy, value, font=font(size, bold), fill=fill, anchor=anchor, spacing=spacing, align=align)


def rr(draw, box, fill, outline=None, width=2, radius=24):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def arrow(draw, a, b, fill=GREEN, width=8):
    draw.line([a, b], fill=fill, width=width)
    x2, y2 = b; x1, y1 = a
    import math
    ang = math.atan2(y2-y1, x2-x1)
    s = 18
    pts = [(x2, y2), (x2-s*math.cos(ang-0.55), y2-s*math.sin(ang-0.55)), (x2-s*math.cos(ang+0.55), y2-s*math.sin(ang+0.55))]
    draw.polygon(pts, fill=fill)


def base_canvas(title, subtitle):
    im = Image.new("RGB", (1800, 1100), BG)
    d = ImageDraw.Draw(im)
    text(d, (70, 62), title, 56, bold=True)
    text(d, (70, 135), subtitle, 27, fill=MUTED)
    d.line((70, 190, 1730, 190), fill=INK, width=3)
    return im, d


def draw_site(lang):
    zh = lang == "zh"
    im, d = base_canvas("AI SIDECAR CITY / AI 侧挂城市" if zh else "AI SIDECAR CITY", "普通城市是主机，AI 只能侧挂。" if zh else "The ordinary city is the host. AI is only a reversible sidecar.")
    rr(d, (70, 230, 1030, 1015), WHITE, LINE)
    text(d, (110, 270), "一脊 · 六段 · 六缝 · 三核" if zh else "ONE SPINE · SIX SEGMENTS · SIX STITCHES · THREE CORES", 30, bold=True)
    x = 550
    d.line((x, 330, x, 920), fill=GREEN, width=24)
    for i in range(6):
        y = 360 + i*95
        d.line((250, y, 850, y), fill=BLUE if i % 2 else GREEN2, width=5)
        text(d, (205, y), str(i+1), 22, fill=MUTED, anchor="rm")
    nodes = [(440, 400, "大钟寺" if zh else "DAZHONGSI", "ROAD-011", "ARRIVAL SIDECAR"), (650, 620, "AI 原点" if zh else "AI ORIGIN", "ROAD-010", "CARE PORCH"), (760, 820, "众智园" if zh else "ZHONGZHIYUAN", "ROAD-009", "TEST POCKET")]
    for y, cx, name, rid, sc in nodes:
        pass
    nodes = [(400, "大钟寺" if zh else "DAZHONGSI", "ROAD-011", "ARRIVAL SIDECAR"), (620, "AI 原点" if zh else "AI ORIGIN", "ROAD-010", "CARE PORCH"), (820, "众智园" if zh else "ZHONGZHIYUAN", "ROAD-009", "TEST POCKET")]
    for y, name, rid, sc in nodes:
        d.ellipse((x-28, y-28, x+28, y+28), fill=INK)
        d.line((x-200, y, x+200, y), fill=ORANGE, width=10)
        rr(d, (x+230, y-48, x+435, y+48), "#F3DDCF", ORANGE, radius=18)
        text(d, (x+250, y-19), sc, 19, bold=True)
        text(d, (x-420, y-28), name, 25, bold=True)
        text(d, (x-420, y+8), rid + " · AI dependency = none", 17, fill=MUTED)
    text(d, (120, 955), "AI OFF / ON：三条主路位置不变；变化只发生在橙色侧挂接口。" if zh else "AI OFF / ON: all three host routes stay fixed; only the orange sidecar interfaces change.", 22, fill=GREEN, bold=True)

    rr(d, (1070, 230, 1730, 1015), WHITE, LINE)
    text(d, (1110, 270), "HOST → SIDECAR RULE" if not zh else "主机 → 侧挂规则", 32, bold=True)
    rows = [
        ("ROAD-009", "TEST POCKET", "工作/休息/公共交流" if zh else "work / rest / public exchange"),
        ("ROAD-010", "CARE PORCH", "居住/人工帮助/社区生活" if zh else "home / human help / common life"),
        ("ROAD-011", "ARRIVAL SIDECAR", "固定导视/人工问询/等候" if zh else "fixed signs / staffed help / waiting"),
    ]
    y=350
    for rid, sc, baseline in rows:
        rr(d, (1110, y, 1690, y+150), "#FAF8F2", LINE, radius=18)
        text(d, (1140, y+24), rid, 22, bold=True, fill=GREEN)
        text(d, (1140, y+58), baseline, 21)
        text(d, (1140, y+99), "+ " + sc, 22, bold=True, fill=ORANGE)
        y += 175
    text(d, (1110, 895), "3 sidecar types · 9 host features\n0 new AI land-use codes · route preservation = 1.0", 23, bold=True)
    text(d, (1110, 970), "REAL LEVEL DATA REQUIRED @ Dazhongsi" if not zh else "大钟寺：REAL LEVEL DATA REQUIRED", 19, fill=BLUE, bold=True)
    return im


def draw_landuse(lang):
    zh = lang == "zh"
    im, d = base_canvas("C7 LAND-USE HOST / C7 用地主机" if zh else "C7 LAND-USE HOST", "AI 不是第八种用地；sidecar 附着在普通城市功能上。" if zh else "AI is not an eighth land-use category; sidecars attach to ordinary urban functions.")
    labels = [("HOME", "居"), ("LEARN", "学"), ("CARE", "护"), ("MOVE", "行"), ("GREEN", "绿"), ("WORK", "工"), ("COMMON LIFE", "交")]
    x0=85; y0=270; w=220; h=210; gap=18
    for i,(en,cn) in enumerate(labels):
        x=x0+i*(w+gap)
        rr(d,(x,y0,x+w,y0+h),WHITE,LINE,radius=20)
        text(d,(x+22,y0+30),en,24,bold=True,fill=GREEN)
        text(d,(x+w-24,y0+34),cn,38,bold=True,fill=INK,anchor="ra")
        sub = ["homes", "learning", "human care", "ordinary mobility", "public green", "research/work", "commons"] [i]
        if zh: sub = ["长期居住", "学校/共学", "人工照护", "普通交通", "公共绿地", "科研/工作", "公共生活"][i]
        text(d,(x+22,y0+110),sub,22,fill=MUTED)
    text(d,(85,540),"SIDEcars attach across C7 without replacing C7" if not zh else "SIDECAR 跨 C7 附着，但不替代 C7",30,bold=True)
    cards=[("TEST POCKET","WORK + COMMON LIFE","众智园" if zh else "ZHONGZHIYUAN"),("CARE PORCH","HOME + CARE + LEARN","AI 原点" if zh else "AI ORIGIN"),("ARRIVAL SIDECAR","MOVE + COMMON LIFE","大钟寺" if zh else "DAZHONGSI")]
    y=610
    for i,(sc,c7,place) in enumerate(cards):
        x=85+i*555
        rr(d,(x,y,x+515,y+250),"#FAF8F2",ORANGE,radius=22)
        text(d,(x+30,y+30),sc,28,bold=True,fill=ORANGE)
        text(d,(x+30,y+82),place,24,bold=True)
        text(d,(x+30,y+130),c7,22,fill=GREEN,bold=True)
        text(d,(x+30,y+178),"AI OFF → host remains complete" if not zh else "AI OFF → 普通城市主机仍完整",20,fill=MUTED)
    rr(d,(85,900,1715,1015),"#E9F0EC",GREEN,radius=18)
    text(d,(120,928),"NEW AI LAND-USE CODES = 0" if not zh else "新增 AI 专用用地代码 = 0",34,bold=True,fill=GREEN)
    text(d,(710,936),"AI changes interfaces, not statutory land-use categories." if not zh else "AI 改变接口，不伪造新的法定用地分类。",23)
    return im


def draw_keyareas(lang):
    zh=lang=="zh"
    im,d=base_canvas("THREE HOSTS · THREE SIDECARS" if not zh else "三种城市主机 · 三种 AI SIDECAR", "AI OFF 与 AI ON 共享同一条普通路径；ON 只增加侧向接口。" if zh else "AI OFF and AI ON share the same ordinary route; ON adds only a lateral interface.")
    areas=[
        ("众智园" if zh else "ZHONGZHIYUAN","ROAD-009","TEST POCKET",["BLDG-012","BLDG-013","PUBLIC-006"],"研发校园" if zh else "R&D CAMPUS"),
        ("AI 原点" if zh else "AI ORIGIN","ROAD-010","CARE PORCH",["BLDG-007","BLDG-009","PUBLIC-004"],"长期社区" if zh else "LONG-TERM NEIGHBORHOOD"),
        ("大钟寺" if zh else "DAZHONGSI","ROAD-011","ARRIVAL SIDECAR",["BLDG-001","BLDG-002","PUBLIC-001"],"站城到达" if zh else "STATION-CITY ARRIVAL"),
    ]
    for i,(name,rid,sc,hosts,typ) in enumerate(areas):
        x=70+i*575
        rr(d,(x,235,x+535,1015),WHITE,LINE,radius=22)
        text(d,(x+28,270),name,30,bold=True)
        text(d,(x+28,312),typ,18,fill=MUTED)
        # OFF panel
        rr(d,(x+28,365,x+507,625),"#EEF3F0",GREEN2,radius=18)
        text(d,(x+48,388),"AI OFF",24,bold=True,fill=GREEN)
        d.line((x+72,520,x+435,520),fill=GREEN,width=10)
        for bx in [x+100,x+220,x+340]:
            rr(d,(bx,455,bx+75,505),SAND,LINE,radius=8)
        text(d,(x+48,555),rid+" · SAME ROUTE",18,bold=True)
        text(d,(x+48,585),"complete ordinary city" if not zh else "完整普通城市",18,fill=MUTED)
        # ON panel
        rr(d,(x+28,650,x+507,925),"#FFF4EC",ORANGE,radius=18)
        text(d,(x+48,674),"AI ON",24,bold=True,fill=ORANGE)
        d.line((x+72,805,x+435,805),fill=GREEN,width=10)
        for bx in [x+100,x+220,x+340]:
            rr(d,(bx,740,bx+75,790),SAND,LINE,radius=8)
        rr(d,(x+355,835,x+465,890),"#F4D4C1",ORANGE,radius=10)
        d.line((x+410,805,x+410,835),fill=ORANGE,width=5)
        text(d,(x+48,840),sc,18,bold=True,fill=ORANGE)
        text(d,(x+48,870),"route geometry unchanged" if not zh else "主路线几何不变",17,fill=MUTED)
        text(d,(x+28,948),"HOSTS: "+" / ".join(hosts),15,fill=MUTED)
    text(d,(72,1040),"Dazhongsi: REAL LEVEL DATA REQUIRED" if not zh else "大钟寺：REAL LEVEL DATA REQUIRED（真实站口/高差/桥隧/通廊参数均未声明）",18,bold=True,fill=BLUE)
    return im


def draw_mobility(lang):
    zh=lang=="zh"
    im,d=base_canvas("MOBILITY + BLUE/GREEN HOST" if not zh else "交通慢行 + 蓝绿主机", "普通路径、公共绿脊与六条缝合联系先成立；sidecar 不占用主骨架。" if zh else "Ordinary routes, the public green spine and six stitches work first; sidecars do not occupy the host network.")
    rr(d,(70,230,1220,1015),WHITE,LINE,radius=22)
    x=600
    d.line((x,300,x,930),fill=GREEN,width=30)
    text(d,(x+28,300),"PUBLIC GREEN SPINE" if not zh else "京张公共绿脊",23,bold=True,fill=GREEN)
    for i in range(6):
        y=365+i*92
        d.line((200,y,1000,y),fill=BLUE,width=5)
        text(d,(155,y),f"STITCH {i+1}",15,fill=MUTED,anchor="rm")
    routes=[(390,"ROAD-011","ARRIVAL"),(610,"ROAD-010","CARE"),(830,"ROAD-009","TEST")]
    for y,rid,lab in routes:
        d.line((320,y,900,y),fill=ORANGE,width=11)
        d.ellipse((x-16,y-16,x+16,y+16),fill=INK)
        rr(d,(930,y-34,1150,y+34),"#FFF4EC",ORANGE,radius=12)
        text(d,(950,y-13),rid+" · "+lab,16,bold=True,fill=ORANGE)
    rr(d,(1260,230,1730,1015),WHITE,LINE,radius=22)
    text(d,(1300,270),"NETWORK RULES" if not zh else "网络规则",30,bold=True)
    bullets=[
        "3 invariant routes" if not zh else "3 条不绕行主路",
        "6 east-west stitches" if not zh else "6 条东西缝合联系",
        "1 public green spine" if not zh else "1 条公共绿脊",
        "sidecar hosts are lateral" if not zh else "sidecar 宿主只在侧边",
        "no AI-only route" if not zh else "没有 AI 专用路径",
        "no fabricated station level" if not zh else "不虚构站城高差/竖向",
    ]
    y=350
    for b in bullets:
        d.ellipse((1305,y+7,1320,y+22),fill=GREEN)
        text(d,(1340,y),b,21)
        y+=72
    rr(d,(1295,820,1695,955),"#EEF2F5",BLUE,radius=16)
    text(d,(1320,845),"DAZHONGSI",20,bold=True,fill=BLUE)
    text(d,(1320,884),"REAL LEVEL DATA\nREQUIRED",28,bold=True,fill=INK)
    return im


def draw_metrics(lang):
    zh=lang=="zh"
    im,d=base_canvas("METRICS + EVIDENCE BOUNDARY" if not zh else "核心指标 + 证据边界", "锁定面积指标不动；v0.15.s 只增加可复核的 sidecar 设计事实。" if zh else "Locked area metrics remain unchanged; v0.15.s adds only reviewable sidecar design facts.")
    fixed=[("SITE", "11,412,825.386 m²"),("GREEN", "2,225,592.728 m²"),("GREEN RATIO","19.5008%"),("PUBLIC SPACE","386,029.358 m²"),("PUBLIC RATIO","3.3824%"),("BUILDING FOOTPRINT","1,024,945.371 m²")]
    text(d,(70,245),"LOCKED / 锁定" if zh else "LOCKED AREA METRICS",28,bold=True,fill=GREEN)
    for i,(k,v) in enumerate(fixed):
        col=i%2; row=i//2
        x=70+col*500; y=300+row*190
        rr(d,(x,y,x+460,y+155),WHITE,LINE,radius=18)
        text(d,(x+24,y+24),k,18,bold=True,fill=MUTED)
        text(d,(x+24,y+68),v,28,bold=True)
    text(d,(1080,245),"v0.15.s DESIGN FACTS" if not zh else "v0.15.s 设计事实",28,bold=True,fill=ORANGE)
    facts=[("SIDECAR TYPES","3"),("HOST FEATURES","9"),("PUBLIC HOSTS","3"),("ROUTE PRESERVATION","1.0"),("NEW AI LAND-USE","0")]
    y=300
    for k,v in facts:
        rr(d,(1080,y,1730,y+118),"#FFF8F2",ORANGE,radius=16)
        text(d,(1110,y+24),k,18,bold=True,fill=MUTED)
        text(d,(1665,y+24),v,36,bold=True,fill=ORANGE,anchor="ra")
        y+=135
    rr(d,(70,900,1730,1015),"#EEF2F5",BLUE,radius=18)
    text(d,(105,924),"EVIDENCE BOUNDARY" if not zh else "证据边界",23,bold=True,fill=BLUE)
    msg=("Concept geometry ≠ survey / statutory control / engineering alignment. Dazhongsi needs verified entrances and real level data." if not zh else "概念 geometry ≠ 测绘 / 法定控规 / 工程线位。大钟寺仍需核实真实站口与高程。")
    text(d,(360,928),msg,20)
    return im


def generate_figures() -> None:
    out=ROOT/"assets/figures"; out.mkdir(parents=True,exist_ok=True)
    funcs=[("site-overview",draw_site),("land-use-structure",draw_landuse),("key-areas",draw_keyareas),("mobility-bluegreen",draw_mobility),("metrics-evidence",draw_metrics)]
    for name,fn in funcs:
        fn("zh").save(out/f"{name}.png",quality=95)
        fn("en").save(out/f"{name}.en.png",quality=95)


def draw_pdf_image(c, img_path: Path, x, y, w, h):
    im=Image.open(img_path)
    iw,ih=im.size
    scale=min(w/iw,h/ih)
    dw,dh=iw*scale,ih*scale
    c.drawImage(ImageReader(im),x+(w-dw)/2,y+(h-dh)/2,dw,dh,preserveAspectRatio=True,mask='auto')


def generate_pdf(path: Path, lang: str, kind: str) -> None:
    zh=lang=="zh"
    page=landscape(A0 if kind=="a0" else A3)
    c=canvas.Canvas(str(path),pagesize=page)
    W,H=page
    if zh:
        pdfmetrics.registerFont(UnicodeCIDFont('STSong-Light'))
        face='STSong-Light'
    else:
        face='Helvetica'
    bold='Helvetica-Bold' if not zh else face
    margin=W*0.035
    c.setFillColorRGB(0.125,0.188,0.2)
    c.setFont(bold,32 if kind=="a0" else 22)
    c.drawString(margin,H-margin*0.9,"京张城市完整度 v0.15.s | AI SIDECAR CITY" if zh else "JING-ZHANG CITY COMPLETENESS v0.15.s | AI SIDECAR CITY")
    c.setFont(face,18 if kind=="a0" else 13)
    c.setFillColorRGB(0.39,0.45,0.46)
    c.drawString(margin,H-margin*1.55,"普通城市是主机，AI 只能侧挂。" if zh else "The ordinary city is the host. AI is only a reversible sidecar.")
    top=H-margin*2.15
    bottom=margin*1.1
    gap=margin*0.45
    left_w=(W-2*margin-gap)*0.53
    right_w=(W-2*margin-gap)-left_w
    draw_pdf_image(c,ROOT/("assets/figures/site-overview.png" if zh else "assets/figures/site-overview.en.png"),margin,bottom,left_w,top-bottom)
    draw_pdf_image(c,ROOT/("assets/figures/key-areas.png" if zh else "assets/figures/key-areas.en.png"),margin+left_w+gap,bottom,right_w,top-bottom)
    c.showPage()
    # second page/board: land use + mobility
    c.setFont(bold,28 if kind=="a0" else 20); c.setFillColorRGB(0.125,0.188,0.2)
    c.drawString(margin,H-margin,"C7 HOST + MOBILITY" if not zh else "C7 主机 + 交通慢行")
    draw_pdf_image(c,ROOT/("assets/figures/land-use-structure.png" if zh else "assets/figures/land-use-structure.en.png"),margin,margin,(W-3*margin)/2,H-2.2*margin)
    draw_pdf_image(c,ROOT/("assets/figures/mobility-bluegreen.png" if zh else "assets/figures/mobility-bluegreen.en.png"),W/2+margin/2,margin,(W-3*margin)/2,H-2.2*margin)
    c.showPage()
    # third page for A3 only; A0 also gets metrics as third board for completeness
    c.setFont(bold,28 if kind=="a0" else 20); c.setFillColorRGB(0.125,0.188,0.2)
    c.drawString(margin,H-margin,"METRICS + REALITY BOUNDARY" if not zh else "核心指标 + 现实边界")
    draw_pdf_image(c,ROOT/("assets/figures/metrics-evidence.png" if zh else "assets/figures/metrics-evidence.en.png"),margin,margin,W-2*margin,H-2.2*margin)
    c.save()


def generate_pdfs() -> None:
    out=ROOT/"drawings"; out.mkdir(exist_ok=True)
    generate_pdf(out/"a3-booklet.pdf","zh","a3")
    generate_pdf(out/"a3-booklet.en.pdf","en","a3")
    generate_pdf(out/"a0-boards.pdf","zh","a0")
    generate_pdf(out/"a0-boards.en.pdf","en","a0")


def visual_html(lang: str) -> str:
    zh=lang=="zh"
    title="京张城市完整度 v0.15.s｜AI 侧挂城市" if zh else "Jing-Zhang City Completeness v0.15.s | AI SIDECAR CITY"
    thesis="普通城市是主机，AI 只能侧挂。" if zh else "The ordinary city is the host. AI is only a reversible sidecar."
    intro="AI OFF 是完整城市；AI ON 只在同一座城市旁边增加可关闭的测试、照护与到达接口。" if zh else "AI OFF is a complete city; AI ON adds only stoppable test, care and arrival interfaces beside the same city."
    site="site-overview.png" if zh else "site-overview.en.png"
    key="key-areas.png" if zh else "key-areas.en.png"
    land="land-use-structure.png" if zh else "land-use-structure.en.png"
    mob="mobility-bluegreen.png" if zh else "mobility-bluegreen.en.png"
    met="metrics-evidence.png" if zh else "metrics-evidence.en.png"
    markers="总览地图 · 三层范围 · 重点区域 · 用地分区 · 交通慢行 · 蓝绿公共空间 · 建筑 · 更新项目 · AI 场景 · 核心指标 · 任务覆盖 · 自检状态 · 来源 · 假设"
    cards = [
        ("ROAD-009","TEST POCKET","众智园｜研发校园" if zh else "ZHONGZHIYUAN | R&D CAMPUS","BLDG-012 · BLDG-013 · PUBLIC-006"),
        ("ROAD-010","CARE PORCH","AI 原点｜长期社区" if zh else "AI ORIGIN | LONG-TERM NEIGHBORHOOD","BLDG-007 · BLDG-009 · PUBLIC-004"),
        ("ROAD-011","ARRIVAL SIDECAR","大钟寺｜站城到达" if zh else "DAZHONGSI | STATION-CITY ARRIVAL","BLDG-001 · BLDG-002 · PUBLIC-001"),
    ]
    card_html="\n".join(f'''<article class="sidecar-card" data-sidecar="{sc}">
          <div class="route">{rid}</div><h3>{sc}</h3><p>{place}</p><small>{hosts}</small>
          <div class="states"><span class="off">AI OFF · SAME ROUTE</span><span class="on">AI ON · + SIDECAR</span></div>
        </article>''' for rid,sc,place,hosts in cards)
    return f'''<!doctype html>
<html lang="{'zh-CN' if zh else 'en'}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>{title}</title>
  <style>
    *{{box-sizing:border-box}} body{{margin:0;background:#f5f1e7;color:#203033;font-family:Arial,"Noto Sans CJK SC",sans-serif;line-height:1.5}}
    main{{max-width:1500px;margin:auto;padding:34px 44px 86px}} header{{display:grid;grid-template-columns:1fr auto;gap:28px;align-items:end;border-bottom:3px solid #203033;padding-bottom:20px}}
    .eyebrow{{font-weight:800;color:#d26f3c;letter-spacing:.04em}} h1{{font-size:48px;line-height:1.08;margin:8px 0 10px}} header p{{font-size:24px;margin:0;max-width:900px}} .rule{{font-size:18px;color:#667477;text-align:right}}
    .hero{{display:grid;grid-template-columns:1.02fr .98fr;gap:20px;margin-top:24px}} .hero img,.figure-grid img,.wide{{width:100%;display:block;background:white;border:1px solid #c9c1b5}}
    .toggle{{display:flex;gap:10px;margin:22px 0 14px}} button{{border:1px solid #203033;background:#fff;padding:9px 16px;border-radius:999px;font-weight:800;cursor:pointer}} button.active{{background:#203033;color:#fff}}
    .cards{{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}} .sidecar-card{{background:#fff;border:1px solid #c9c1b5;border-top:7px solid #d26f3c;padding:18px 20px;border-radius:14px}}
    .route{{font-weight:800;color:#2d6b5e}} h3{{font-size:24px;margin:8px 0}} .sidecar-card p{{font-size:18px;margin:0 0 6px}} small{{color:#667477}} .states{{display:flex;gap:8px;margin-top:14px;flex-wrap:wrap}} .states span{{font-size:13px;font-weight:800;padding:5px 8px;border-radius:999px}} .off{{background:#e9f0ec;color:#2d6b5e}} .on{{background:#f9e4d6;color:#b65d2f}}
    body[data-focus="off"] .on{{opacity:.28}} body[data-focus="on"] .off{{opacity:.28}} section{{margin-top:34px}} h2{{font-size:31px;margin:0 0 15px}} .figure-grid{{display:grid;grid-template-columns:1fr 1fr;gap:20px}}
    .metrics{{display:grid;grid-template-columns:repeat(5,1fr);gap:10px;margin-top:14px}} .metric{{background:#fff;border:1px solid #c9c1b5;border-radius:12px;padding:14px}} .metric b{{display:block;font-size:21px}} .metric span{{font-size:13px;color:#667477}}
    .audit{{background:#eef2f5;border-left:6px solid #4c7795;padding:18px 22px}} footer{{margin-top:38px;border-top:1px solid #aaa;padding-top:18px;color:#667477}}
    @media(max-width:900px){{header,.hero,.cards,.figure-grid,.metrics{{grid-template-columns:1fr}} .rule{{text-align:left}}}}
  </style>
</head>
<body data-focus="split">
<main>
  <header>
    <div><div class="eyebrow">v0.15.s · AI SIDECAR CITY</div><h1>{title}</h1><p>{thesis}<br><strong>{intro}</strong></p></div>
    <div class="rule">3 invariant routes<br>3 sidecar types<br>9 host features<br>0 AI-only land-use codes</div>
  </header>
  <div class="hero">
    <img src="../assets/figures/{site}" alt="{'总体结构、三条不绕行路线与三个侧挂接口' if zh else 'Overall structure, three invariant routes and three lateral sidecar interfaces'}">
    <img src="../assets/figures/{key}" alt="{'众智园、AI原点和大钟寺的AI OFF与AI ON空间对照' if zh else 'AI OFF versus AI ON spatial comparison for Zhongzhiyuan, AI Origin and Dazhongsi'}">
  </div>
  <div class="toggle" aria-label="AI state emphasis"><button class="active" data-mode="split">OFF + ON</button><button data-mode="off">AI OFF</button><button data-mode="on">AI ON</button></div>
  <div class="cards">{card_html}</div>
  <section><h2>{'用地分区：AI 不是第八种用地' if zh else 'Land-use host: AI is not an eighth land-use category'}</h2><img class="wide" src="../assets/figures/{land}" alt="{'C7普通城市功能与三个sidecar的附着关系' if zh else 'C7 ordinary-city functions and three sidecar attachment relationships'}"></section>
  <section><h2>{'交通慢行、蓝绿公共空间与侧挂边界' if zh else 'Mobility, blue-green public space and sidecar boundaries'}</h2><div class="figure-grid"><img src="../assets/figures/{mob}" alt="{'绿脊、六条缝合联系和三条不绕行路线' if zh else 'Green spine, six stitches and three invariant routes'}"><img src="../assets/figures/{met}" alt="{'六项锁定指标、sidecar设计事实与证据边界' if zh else 'Six locked metrics, sidecar design facts and evidence boundary'}"></div></section>
  <section><h2>{'核心指标' if zh else 'Core metrics'}</h2><div class="metrics">
    <div class="metric"><b data-metric="site_area_sqm" data-value="11412825.386">11,412,825.386 m²</b><span>site_area_sqm</span></div>
    <div class="metric"><b data-metric="green_ratio" data-value="0.195008">19.5008%</b><span>green_ratio</span></div>
    <div class="metric"><b data-metric="public_space_ratio" data-value="0.033824">3.3824%</b><span>public_space_ratio</span></div>
    <div class="metric"><b data-metric="ai_sidecar_type_count" data-value="3">3</b><span>ai_sidecar_type_count</span></div>
    <div class="metric"><b data-metric="ai_sidecar_host_feature_count" data-value="9">9</b><span>ai_sidecar_host_feature_count</span></div>
  </div></section>
  <section class="audit"><h2>{'任务覆盖 / 自检状态 / 来源 / 假设' if zh else 'Task coverage / self-check / sources / assumptions'}</h2><p>{markers}</p><p>{'三层范围、建筑、更新项目与 AI 场景仍在 proposal / geometry / matrices 中逐项闭环；本页只把第一视觉收敛到“主机 + sidecar”的空间判断。' if zh else 'Three-level scope, buildings, renewal projects and AI scenarios remain closed through proposal, geometry and evidence matrices; this first screen focuses on the host + sidecar spatial judgment.'}</p></section>
  <footer>{'REALITY BOUNDARY：所有 sidecar 都是概念空间关系。真实尺寸、运营、站口、高差、工程线位和许可均需正式证据。' if zh else 'REALITY BOUNDARY: every sidecar is a conceptual spatial relationship. Real dimensions, operations, station entrances, levels, engineering alignments and permits require formal evidence.'}</footer>
</main>
<script>
  document.querySelectorAll('[data-mode]').forEach(function(btn){{btn.addEventListener('click',function(){{document.body.dataset.focus=btn.dataset.mode;document.querySelectorAll('[data-mode]').forEach(function(x){{x.classList.toggle('active',x===btn)}});}})}});
</script>
</body>
</html>
'''


def update_visuals() -> None:
    (ROOT/"visual/index.html").write_text(visual_html("zh"),encoding="utf-8")
    (ROOT/"visual/index.en.html").write_text(visual_html("en"),encoding="utf-8")


def update_changelog() -> None:
    p=ROOT/"changelog.md"
    old=p.read_text(encoding="utf-8")
    block='''\n## v0.15.s — AI SIDECAR CITY / AI 侧挂城市\n\n- 将 v0.14.s 的三条 invariant civic routes 升级为“普通城市主机 + 可逆 AI sidecar”：TEST POCKET、CARE PORCH、ARRIVAL SIDECAR。\n- 在 `buildings.geojson`、`public_space.geojson` 和 `roads.geojson` 中为 9 个宿主 feature 建立 sidecar / route / AI OFF-ON 机器可读关系；不修改 Polygon 或 LineString 几何。\n- 删除重点区域正文中遗留的 3.5m、2.0m、1.8m、400m、多层甲板、通廊净宽等无正式依据的伪工程精度；大钟寺继续 `REAL LEVEL DATA REQUIRED`。\n- 新增 `ai_sidecar_type_count=3`、`ai_sidecar_host_feature_count=9`、`ai_off_route_preservation_ratio=1.0`、`new_ai_land_use_code_count=0` 等设计事实指标。\n- 重建 5 组中英 canonical PNG、双语 A3/A0、visual 首页；AI OFF/ON 在同一图中对照，普通路线位置保持不变。\n- 清理 v0.14.s review 反馈：visual 图片补齐 alt；HTML 保持可读格式；report section markers 后处理为真实注释；旧 v0.13.g section refs 从 evidence matrices 移除。\n'''
    if "## v0.15.s — AI SIDECAR CITY" not in old:
        if old.startswith("#"):
            first_nl=old.find("\n")
            old=old[:first_nl+1]+block+old[first_nl+1:]
        else:
            old=block+old
    p.write_text(old,encoding="utf-8")


def main() -> None:
    if not ROOT.is_dir():
        raise SystemExit(f"submission missing: {ROOT}")
    update_proposals()
    update_geometry()
    update_metrics()
    update_contract()
    update_matrices()
    generate_figures()
    generate_pdfs()
    update_visuals()
    update_changelog()
    print("v0.15.s builder complete")

if __name__ == "__main__":
    main()
