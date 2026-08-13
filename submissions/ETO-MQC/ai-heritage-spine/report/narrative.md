# 提交附录：权利台账与双语实质等值核验 / Submission Appendix: Rights Ledger and Bilingual Equivalence

> 本附录覆盖 `submissions/ETO-MQC/ai-heritage-spine/` 的静态交付物。它记录 **AI 生成后的版本核验**，不冒充人工签署。正式公开、评奖或实施前，必须由获得授权的中英文专业人员、权利审核人和提交责任人完成实质等值、来源和许可复核。

## 1. 资产权利与使用边界 / Asset Rights and Use Boundaries

| 资产类别 | 包内路径或来源 | 权利状态与核验 | 使用边界 |
| --- | --- | --- | --- |
| 方案正文、译文和静态 HTML | `proposal.md`、`proposal.en.md`、`report/proposal*.html`、`visual/*.html` | 由申报智能体生成；哈希与 `agent.json`、`manifest.json` 关联。 | `COMMUNITY-DISPLAY-ONLY` 仅用于提交展示；不等于商业再许可。 |
| 概念几何与指标 | `geometry/*.geojson`、`metrics.json` | 每层声明 `source_type`、置信度和临时边界提示；指标按 EPSG:4548 复算。 | 非官方红线、地籍、控规或审批依据；正式数据发布后整包重算。 |
| 图件、图册与展板 | `assets/figures/*.png`、`drawings/*.pdf` | 基于包内 GeoJSON 和 metrics 的本地渲染结果；不加载在线底图或地图瓦片。 | 可用于方案评审；不主张真实测绘精度或已批准建设方案。 |
| Logo 与 VI | `assets/identity/logo-lockup.*`、`assets/identity/brand-system.*` | 原创概念性矢量构图及可见 PNG 预览；未使用政府徽标、注册商标或既有企业标志。 | 仅供本提案；公共实施前需完成商标检索、导视审批与书面授权。 |
| 字体 | SVG 内声明 Noto Sans CJK / DejaVu Sans；PNG 为本地渲染像素 | 不随包分发字体文件。 | 正式出版时由出版方确认嵌入或替换字体许可。 |
| 代码与依赖 | 静态 HTML 无远程脚本、远程字体、iframe 或 API；生成依赖不打包。 | 离线 HTML 与 visual review 核验。 | 不把生成环境、密钥或第三方源代码作为提交资产。 |
| 外部案例资料 | `sources.json` CASE-* | 仅链接、仅事实概括、仅比较机制；未嵌入第三方图片、图纸、Logo、仪表盘或全文。 | 未明确开放许可时，不自动推导素材权利已清理。 |

## 2. 六个全球案例的来源、时间与许可处理 / Six Case Sources, Dates, and Licence Treatment

| ID | 发布主体、来源与时间 | 核验机制 | 许可与适用性处理 |
| --- | --- | --- | --- |
| CASE-QUAYSIDE | [Waterfront Toronto: Quayside](https://www.waterfrontoronto.ca/our-projects/quayside)，访问核验 2026-08-12。 | 公共领域统筹、竞争性开发伙伴、步行滨水空间。 | 不复制网页渲染图、Logo 或数据。 |
| CASE-DMC | [Seoul Metropolitan Government: Smart City & Digitization](https://english.seoul.go.kr/policy/smart-city/vision-governance/)，访问核验 2026-08-12。 | 公共利益、包容、网络安全与公众参与。 | 首尔市版权保留；不复制其视觉素材，也不复刻 DMC。 |
| CASE-PDD | [JTC: Punggol Digital District](https://www.jtc.gov.sg/punggoldigitaldistrict)，页面更新 2026-01-14。 | 产学社区融合、园区运行数据平台、低碳出行。 | 只作机制比较，不再分发 JTC 图纸或图片。 |
| CASE-KQ | [University College London: Knowledge Quarter dashboard](https://www.ucl.ac.uk/enterprise/about/london-knowledge-quarter-research-and-innovation-dashboard)，2024–2025 资料。 | 多机构协作网络、研究/产业绩效看板。 | UCL/Elsevier 对 findings 要求署名；本包不再分发数据或截图。 |
| CASE-QIANHAI | [Shenzhen Municipal Commerce Bureau: Qianhai](https://www.sz.gov.cn/en_szgov/business/SpecialFunctionalAreas/content/post_11487172.html)，更新 2024-08-08。 | 跨区域制度、交通、生态接口协同。 | 来源明确未经授权不得转载；只作原创事实概括，不表示合作。 |
| CASE-SHIBUYA | [Tokyo Convention & Visitors Bureau: Shibuya Stream](https://www.gotokyo.org/en/spot/1747/index.html)，更新 2025-12-11。 | 轨道遗址、滨水步行空间、广场、多用途设施缝合。 | 图片带版权标记；不复制图像、标志或设计图。 |

案例的适用性是本方案的原创判断，必须结合海淀正式边界、法律、产权、公众参与和专业意见再验证。

## 3. 双语逐项对照 / Item-by-Item Bilingual Equivalence

| 对照项 | 中文落点 | 英文落点 | AI 核验结果 |
| --- | --- | --- | --- |
| 项目名称、作者和许可 | `proposal.md` front matter、标题 | `proposal.en.md` front matter、title | `ETO-MQC`、双语契约和 `COMMUNITY-DISPLAY-ONLY` 一致。 |
| 范围、边界与未知值 | 设计依据、三层框架、指标、风险 | Design Basis, Three-Level Scope, Metrics, Risk | 均声明临时 geometry、正式 polygon 后整包重算；FAR/高度/密度不编造。 |
| 17 项指标 | 指标体系、`metrics.json` | Metrics、`metrics.json` | 面积、比例、数量、EPSG:4548 口径一致。 |
| 五组图件 | `assets/figures/*.png` | `assets/figures/*.en.png` | 同一 GeoJSON/metrics 生成；地图、图例、数据限制翻译对应。 |
| 品牌与 VI | 品牌识别段、identity assets | Concept identity section、same identity assets | 颜色、标志语义、非官方/非注册边界一致。 |
| 六案例证据 | 全球案例表、CASE-* | Six-case evidence table、CASE-* | 主体、时间、机制、许可处理和不背书声明一致。 |
| 三验证场景 | 概念性试点卡表 | Conceptual pilot cards table | 数据、TRL、指标、空间、运营方、退出与人工兜底一致。 |
| 组件、地标、历史与运营 | 公共空间、实施与分期章节 | Public Space, Renewal, and operating model sections | 组件库、三地标、历史解释、活动/开发者/场景开放/品牌治理内容对应。 |
| 状态表述 | `manifest.json`、`self_check.json`、`visual/index.html` | same JSON、`visual/index.en.html` | 统一为 `ready_for_review` / “正式评审就绪 / Formal review ready”，不等于获奖、实施批准或政府背书。 |

## 4. 人工实质等值与权利签署 / Human Sign-off Required Before Publication

| 角色 | 姓名 / 机构 | 日期 | 应核对事项 | 签名 |
| --- | --- | --- | --- | --- |
| 中文专业审核人 | 待指定 | 待填写 | 规划术语、地名、数据口径、法律状态。 | 待签 |
| 英文专业审核人 | 待指定 | 待填写 | 译名、模态词、非承诺性表述、专业语境。 | 待签 |
| 权利与来源审核人 | 待指定 | 待填写 | 第三方来源、商标、字体、公开传播与再使用许可。 | 待签 |
| 提交责任人 | ETO-MQC 或授权代表 | 待填写 | 最终文件、SHA-256、提交分支和变更范围。 | 待签 |

## 5. 未清权或待决事项 / Unresolved Items

官方边界、控规、产权、道路红线、市政、消防、文保和公共服务资料尚未作为可用于法定结论的数据提供。任何活动名称、合作方 Logo、奖项展示、商标、真实运营数据或个人数据，在使用前均需逐项书面授权、目的限定、数据最小化、网络安全与人工复核。未取得书面许可的外部案例图像、图纸、标志和数据库截图不得加入提交资产。
