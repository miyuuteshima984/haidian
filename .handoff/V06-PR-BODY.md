## 投稿信息

- GitHub 用户名：`miyuuteshima984`
- 方案路径：`submissions/miyuuteshima984/jingzhang-ai-civic-infrastructure/`
- 方案标题：**京张城市完整度 / JING-ZHANG CITY COMPLETENESS**
- 迭代版本：`v0.6`
- 提交级别：`formal`
- 前序合并：#1954（71/100）→ #2062 v0.5（83/100，APPROVED）
- 当前 exact head：`252978860c1c88b54d482d9c2d88abfd07e2e2cb`

## v0.6 目标

v0.6 不改变“**先把城市做完整，再让 AI 进入日常**”的核心方法，也不通过增加更多技术名词来冲分。本轮把 v0.5 已有的专业内容进一步变成**可直接定位、可启动/停止、可由评审快速核验**的证据链，重点加强实施可行性、公共利益与多模态表达。

## v0.6 主要增强

- **三个旗舰试点协议**：众智园低速机器人受控测试、AI 原点无障碍/照护导航、大钟寺换乘/多语导览；每项均包含 non-AI baseline、概念数量基础、前置证据门、时间窗、KPI 方向、停止阈值、退出收据与责任结构。
- **9 类显性设计测试人群**：长期居民/家庭、老年居民、残障/行动或感知受限使用者、儿童/照护者、学生/科研、创业/企业、服务劳动者/通勤者、访客/国际使用者、无手机/无账号/主动退出使用者；逐类检查受益、负担、排斥风险、non-AI 等价路径与人工帮助/申诉。
- **实施资源 + RACI 证据门**：将概念数量基础、A/R/C/I、维护频率、许可/安全/保险/人工兜底/数据治理等启动前核验项，组织为 `PRECONDITION → TEST → RECEIPT → GO/REVISE/STOP`。真实货币预算、最终 FTE、采购、合同、保险和具名机构责任在未核实前保持 UNKNOWN。
- **Reviewer Evidence Index**：把公开七项 rubric 与 `agent.1`–`agent.6` 一跳映射到 proposal、图件、JSON、GeoJSON、来源与权利证据，并逐项写明 claim boundary；该索引不是参与者自评分。
- **Review Evidence Dashboard**：把核心指标、C7、三个旗舰试点、9 类人群、实施证据门和主张边界推到中英文 `visual/index*.html` 首屏，同时作为 A3/A0 第一页核心证据，避免关键深化内容只隐藏在 supplemental assets 后部。
- **双语 proposal / metrics / matrices 同步**：iteration 更新为 `v0.6`；`persona_count=9`，新增 `flagship_pilot_count=3`；compliance / taskbook evidence 同步接入上述成果。
- **权利与生成台账继续细化**：v0.6 五组新增双语 SVG 均为本方案原创/AI 辅助表达，不嵌入第三方 Logo、图片、地图、字体文件或专有图表。

## Formal scoring readiness

- [x] `manifest.validation_claim.known_blockers = []`
- [x] persisted self-check：`ok=true`
- [x] `can_enter_formal_review=true`
- [x] `review_status=formal-review-ready`
- [x] deterministic validation：PASS
- [x] spatial review：PASS（仅 3 条允许的 provisional key-area minor 提示）
- [x] visual packaging：PASS（issues=0）
- [x] professional evidence：PASS（issues=0）
- [x] participant preflight / push dry-run：PASS
- [x] PNG / SVG / PDF binary integrity：PASS
- [x] 中英文 A3/A0 已重建，评审证据总表置于第一页

## 数据与实施边界

- [ ] `geometry/site_boundary.geojson` 使用可信 official boundary 且 `official_boundary=true`
- [ ] `geometry/key_areas.geojson` 使用可信 official key-area polygons 且 `official_boundary=true`
- [x] 上述两项继续保持未勾选：当前仍是仓库允许的 provisional geometry，本 PR 不伪装官方数据。
- [x] 不声称官方红线、控规、工程定位、合作承诺、投资额、财政承诺、已批活动、真实预算或现场绩效。
- [x] 机器 PASS 只证明提交包结构、哈希、图件与证据一致性，不把 provisional / unknown 内容升级为现实事实。

## 变更范围

- [x] 当前与 upstream `main` 的比较显示 v0.6 为 8 个真实 commits。
- [x] 所有 PR 文件均限制在 `submissions/miyuuteshima984/jingzhang-ai-civic-infrastructure/`。
- [x] 不修改 `.github/`、`brief/`、`data/`、`docs/`、`schema/`、`scripts/`、`tracks/`、`scenarios/`、gallery 索引或他人投稿。
- [x] automation / handoff 分支内容不进入正式 PR。

## v0.6 commits

1. `e78a2790` — flagship pilot protocols
2. `ee8ba922` — inclusion and burden matrix
3. `10f4b736` — implementation resource and RACI gates
4. `0d3855fe` — reviewer evidence index
5. `6bacd0b7` — surface review evidence above fold
6. `765811fa` — register evidence assets and iteration notes
7. `a11a1a4b` — integrate pilots, inclusion and review traceability
8. `25297886` — finalize bilingual review package and validation

## 提交后跟进

- [x] 只跟进当前 exact head 的 official `submission-validation`、Review Agent 与 maintainer review。
- [x] 只修真实、current-head、participant-controlled 的 blocker / required repair。
- [x] 不用空评论催促、不通过无意义提交刷新队列。
- [x] 若组织方补充 official boundaries / key-area polygons，将按来源与许可要求整体复算 geometry、metrics、figures、HTML 与 PDF。
