## 投稿信息

- GitHub 用户名：`miyuuteshima984`
- 方案路径：`submissions/miyuuteshima984/jingzhang-ai-civic-infrastructure/`
- 方案标题：**京张城市完整度 / JING-ZHANG CITY COMPLETENESS**
- 迭代版本：`v0.7`
- 提交级别：`formal`
- 前序合并：#1954（71/100）→ #2062 v0.5（83/100）→ #2143 v0.6（76/100，APPROVED）
- 当前 exact head：`b35790ae96144224ea26dd8530b2a41641cffa3f`

## v0.7 目标

v0.7 不继续增加 reviewer-facing rubric dashboard，而是保留 v0.6 已有的治理深度，同时把有限的核心视觉预算重新交给**空间设计、人的一天和 AI 对城市形态的真实影响**。

核心方法仍然是：**先把城市做完整，再让 AI 进入日常。** AI 不是第八类用地，而是让测试、服务、到达、基础设施和规划过程需要新的“可开 / 可停 / 可替换”物理接口。

## v0.7 主要增强

- **三条日常城市链**：
  - 众智园：研究者 + 服务劳动者，从到达/研发、吃饭休息、普通步行走到与公共通行物理分离的受控测试院。
  - AI 原点：老人 + 照护者 + 无手机使用者，从家门、遮阴/坐凳/实体导视、照护/人工服务走到公共客厅；拒绝账号不降低基本服务。
  - 大钟寺：通勤者 + 国际访客 + 服务劳动者，从固定双语导视、人工换乘、普通商业/休息走到京张遗产公共界面；动态信息失败时回到实体路径和人工服务。
- **六类可逆 AI 城市形态接口**：测试口袋、无障碍求助节点、连续站城到达界面、可替换小型服务节点、人优先公共首层、可回退空间版本链。
- **重建固定 `key-areas.png/.en.png` 核心图**：直接用三套不同空间剖面表达“创新校园 / 长期社区 / 站城生活区”，让固定 Review Agent 视觉输入看到空间差异，而不是 reviewer-oriented task cards。
- **Reviewer dashboard / evidence index 降级为后部追溯附件**：保留审计价值，但不再占据 visual 首屏、A3/A0 第一页和设计主叙事。
- **真实公开实施锚点**：新增海淀区 2025 城市更新导则、2025 城市更新实施指引和 2025Q4 AI 创新街区公开进展，用于校准真实政策语境与实施边界。
- **两条实施路径**：低扰动可逆动作 vs. 需要真实项目生成、实施方案审查和行政许可的重改造；本包不预授权。
- **最新 design-depth 边界字段**：使用 `completeness_limited_by` 明示 official polygons、真实入口/交通、权属/现状建筑、公共服务容量、项目主体和许可等待核验项，不用伪数据填满。
- **新增可复算设计指标**：`everyday_journey_count=3`、`reversible_urban_form_prototype_count=6`、`implementation_path_count=2`。

## Design-first multimodal package

- `visual/index*.html` 首屏：三条日常城市链。
- A3 第一页：三条日常城市链。
- A0 第一页：三处重点区空间剖面 + AI 城市形态原型 + 公共空间组件/导视 + 总体方法 + brand/VI + landmarks/events。
- reviewer evidence index 只在后部追溯页。
- 四组中英文 PDF 已重建并完成第一屏渲染/非空白 QA。

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
- [x] PNG / SVG / PDF integrity：PASS
- [x] A3/A0 已恢复 design-first 第一页，不把 rubric dashboard 作为主视觉

## 数据、政策与实施边界

- [ ] `geometry/site_boundary.geojson` 使用可信 official boundary 且 `official_boundary=true`
- [ ] `geometry/key_areas.geojson` 使用可信 official key-area polygons 且 `official_boundary=true`
- [x] 上述两项继续保持未勾选：当前仍是仓库允许的 provisional geometry，本 PR 不伪装官方数据。
- [x] 不声称官方红线、控规、工程定位、合作承诺、投资额、财政承诺、已批活动、真实预算、许可或现场绩效。
- [x] 海淀城市更新导则/实施指引只用于现实方向和实施流程边界，不等于本方案入库、立项、审批或具名主体确认。
- [x] 官方公开的 AI 创新街区/AI 原点社区进展只证明现实政策语境，不把现有示范项目写成本方案成果。

## 变更范围

- [x] v0.7 为 4 个真实 commits。
- [x] 与当前 upstream `main` 比较：ahead 4 / behind 139；behind 主要来自并发的其他 submissions。
- [x] 当前 27 个 changed files 全部限制在 `submissions/miyuuteshima984/jingzhang-ai-civic-infrastructure/`。
- [x] 不修改 `.github/`、`brief/`、`data/`、`docs/`、`schema/`、`scripts/`、`tracks/`、`scenarios/`、gallery 索引或他人投稿。
- [x] automation / handoff 分支内容不进入正式 PR。
- [x] 已回读当前 upstream：核心 Review Agent / rubric / validator 文件无规则漂移需要主动 sync；如 current-main CI 报真实问题再处理。

## v0.7 commits

1. `478eeaeb` — `v0.7: restore design-first spatial narratives`
2. `4ff59f58` — `v0.7: spatialize the three key areas`
3. `d7737c02` — `v0.7: anchor implementation to current public guidance`
4. `b35790ae` — `v0.7: finalize design-first bilingual review package`

## 提交后跟进

- [x] 只跟进当前 exact head `b35790ae96144224ea26dd8530b2a41641cffa3f` 的 official `submission-validation`、Review Agent 与 maintainer review。
- [x] 只修真实、current-head、participant-controlled 的 blocker / required repair。
- [x] 不用空评论催促、不通过无意义提交刷新队列。
- [x] 目标仍是 85+，但只有 current exact-head 新评分才算；不预先宣称达到。
- [x] 若组织方补充 official boundaries / key-area polygons，将按来源与许可要求整体复算 geometry、metrics、figures、HTML 与 PDF。
