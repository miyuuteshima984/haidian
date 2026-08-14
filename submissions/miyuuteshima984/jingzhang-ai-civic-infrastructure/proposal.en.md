---
title: "Jing-Zhang City Completeness v0.12.s: Civic Failsafe Sections"
author_github: "miyuuteshima984"
language: "en"
proposal_format_version: "2"
bilingual_contract_version: "1"
translation_of: "proposal.md"
license: "COMMUNITY-DISPLAY-ONLY"
summary: "C7 city completeness remains the ordinary-city baseline. ARRIVE WITHOUT APP, CARE WITHOUT ACCOUNT and TEST WITHOUT BLOCKING become three failsafe spatial contracts tested through ordinary, enhanced, degraded and recovery states."
tracks: ["ai-origin-community", "ai-public-services", "ai-traffic-walkability"]
scenarios: ["ai-traffic-walkability", "robot-delivery-low-speed", "enterprise-service-copilot", "ai-cultural-guide", "ai-health-service-navigation"]
iteration: "v0.12-s"
---

# JING-ZHANG CITY COMPLETENESS v0.12.s / CIVIC FAILSAFE SECTIONS

> **Complete the city first, then let AI enter everyday life; the city must also remain usable when AI fails.**
>
> v0.12.s turns the three public promises into state-based urban sections. Every key area must work in **S0 Ordinary, S1 Enhanced, S2 Degraded and S3 Recovery**. Basic movement, care, work, waiting, rest and common life belong to the city itself. AI, robots, dynamic information and testing are optional overlays.

![v0.12.s master failsafe framework](assets/figures/site-overview.en.png)

## Design Basis and Source List

The proposal continues to use the public announcement, `brief/site-package/`, the agent taskbook, the repository source registry and registered public planning references. The announced approximately 43.6 km² coordinated research area, approximately 11.4 km² overall design area and approximately 368.4 ha of three key areas are task scales. The submitted `SITE_BOUNDARY` and three `KEY_AREA` geometries remain provisional rough geometry for relative relationships, topology, concept quantities and drawings; they are not statutory redlines, property boundaries, road redlines, station exits, regulatory plans or engineering alignments. [source:OFFICIAL-ANNOUNCEMENT] [source:BOUNDARY-SOURCE]

Only registered land-use, building and source enums are used. Approved FAR, height, density, setbacks, road redlines, building-by-building existing conditions, ownership, utilities, fire and heritage controls are incomplete. Public planning references are used only when they change a design judgment, while keeping their evidence status. [source:PLANNING-LIMITS] [standard:MOHURD-URBAN-DESIGN-MEASURES]

The v0.12.s increment is intentionally placed in the main review channels: proposal, bilingual report, canonical figures, A3/A0 first pages, compliance matrix and design-depth matrix. Human and machine reviewers should see the same ordinary-task → spatial-contract → state-transition → human-takeover → rollback logic. [source:FORMAL-GUIDE]

## Three-Level Scope Framework

The coordinated research scale asks how an AI innovation ecosystem can depend on long-term urban life; the overall design scale asks how one civic spine, six bands, six stitches and three cores carry the seven C7 abilities; the key-area scale asks whether concrete spatial tasks remain usable when AI, accounts or tests are unavailable. [source:DESIGN-BRIEF] [depth:three_level_scope_framework]

The overall design area keeps the Jing-Zhang public green spine as the shared framework. Six working bands and six east-west stitches repair ordinary-city capabilities. Provisional geometry supports package consistency only, and official geometry would trigger recalculation of absolute areas and control-dependent relationships. [metric:site_area_sqm] [data:geometry/site_boundary.geojson#SITE-001]

![Three-level scope and continuous urban structure](assets/figures/land-use-structure.en.png)

The three key areas do not depend on invented engineering detail. Zhongzhiyuan studies testing versus ordinary public movement; AI Origin studies care, public ground floors and account barriers; Dazhongsi studies arrival, fixed wayfinding, staffed help and real vertical continuity. [source:KEY-AREA-SOURCE]

## Coordinated Research Area: Industry and Future City Research

The innovation ecosystem remains a research → translation → testing → adoption → long-term-life chain. Universities and research institutions supply knowledge and talent; Zhongzhiyuan hosts R&D and bounded tests; AI Origin tests whether technology can enter ordinary community life; Dazhongsi is an adoption and arrival interface; the Jing-Zhang heritage park provides a continuous public feedback ground. [source:AGENT-TASKBOOK] [standard:PROJECT-AGENT-OPEN-CALL-TASKBOOK]

International cases are used as mechanisms, not copied scale or statutory evidence: Vector Institute for research-industry connection, Mila for open and responsible AI, the Alan Turing Institute for cross-disciplinary public engagement, AI Singapore 100 Experiments for problem-to-PoC-to-scale discipline, Seoul AI Hub for talent/startup/shared-space proximity, and Punggol Digital District for industry-university-community adjacency. [source:CASE-VECTOR] [source:CASE-AISG-100E]

The proposal identity remains **C7 COMPLETE LOOP**: an open ring for continuous completion, twin rail lines for Jing-Zhang memory, and seven nodes for HOME / LEARN / CARE / MOVE / GREEN / WORK / COMMON LIFE. v0.12.s adds the communication rule “STATE, NOT DEVICE”: explain civic capability across operating states before showcasing devices. [source:AGENT-TASKBOOK]

## Overall Design Area: Urban Renewal and Regulatory-Plan-Level Urban Design

The spatial structure remains one spine, six bands, six stitches and three cores. The public spine first provides walking, cycling, accessibility, shade, rainwater, heritage memory and free staying space. Digital guidance and sensing come later. East-west stitches express desired connections, not confirmed roads, bridges, tunnels or station exits. [depth:overall_spatial_structure] [data:geometry/roads.geojson#ROAD-001]

The planning innovation is a stateful public-infrastructure model. **S0 ORDINARY** requires the physical city to work without AI. **S1 ENHANCED** permits optional AI, dynamic information, robots or tests. **S2 DEGRADED** returns critical tasks to fixed infrastructure and human stewardship when devices, models, accounts, networks or tests fail. **S3 RECOVERY** does not automatically re-enable the overlay; ordinary routes, human takeover and exit conditions are reviewed before restart. [source:AGENT-TASKBOOK] [depth:overall_spatial_structure]

No new “AI land-use” category is created. Existing residential, community-service, research, education, cultural, commercial and green-space categories carry the design. Formal FAR, height and building-by-building retain/renovate/demolish decisions remain unresolved until controlling data is available. [source:LAND-USE-CODES] [metric:land_use_feature_count]

## Detailed Design of Key Areas

![Three key-area failsafe spatial contracts](assets/figures/key-areas.en.png)

### Zhongzhiyuan - TEST WITHOUT BLOCKING

The ordinary task is arrival → R&D/service work → food/rest → shared space → departure. A bounded test pocket or branch must be distinguishable, closable and removable without relocating the ordinary public route or green spine. A human stewardship role must be able to stop the test and restore the ordinary state. No unsupported lane width, bollard specification or device spacing is invented. [data:geometry/key_areas.geojson#PROV-KEY-001] [depth:three_key_area_detailed_design]

G0 audits the ordinary route; G1 establishes proposed public-realm and test-operator roles, manual stop and maintenance boundaries; G2 permits a reversible pilot; G3 scales only if closing the test leaves the ordinary task unchanged, otherwise rollback. Legal entities remain to be confirmed. [source:AGENT-TASKBOOK]

### AI Origin - CARE WITHOUT ACCOUNT

The ordinary task is home → shade/rest → care/help → civic commons → green spine. Basic service doors cannot require registration, login, personal-data authorization or smartphone ownership. Physical routes, fixed information and staffed/telephone/paper alternatives form the shared S0/S2 baseline. AI navigation, multilingual help and service matching are optional. [data:geometry/key_areas.geojson#PROV-KEY-002] [depth:three_key_area_detailed_design]

G0 asks whether an accountless resident can complete basic care and help tasks; G1 establishes proposed community-service stewardship and manual takeover; G2 tests optional AI; G3 scales only when refusal of data, account loss or model exit does not change basic access. [source:AGENT-TASKBOOK]

### Dazhongsi - ARRIVE WITHOUT APP

The ordinary task is arrival → orientation → transfer/help → ordinary waiting/retail → Jing-Zhang heritage public interface. Fixed bilingual wayfinding, legible physical entrances, staffed help and an accessible continuity intention form the baseline; dynamic multilingual information and crowd guidance only enhance it. The provisional polygon is not used to infer actual station exits, bridges, tunnels or road engineering. [data:geometry/key_areas.geojson#PROV-KEY-003] [source:KEY-AREA-SOURCE]

G0 asks whether arrival and help remain possible without a phone; G1 establishes a proposed station-city public-interface/human-service role; G2 permits dynamic information; G3 scales only if the ordinary arrival chain remains legible after the dynamic layer is switched off. [depth:traffic_rail_slow_parking]

## AI Innovation Ecosystem, Personas, and AI+ Scenarios

Personas continue to include researchers, service workers, long-term residents, older people, children/caregivers, people without smartphones, commuters, international visitors and small merchants. The common test is: **when data, accounts, models or devices are unavailable, can the person still complete the original urban task?** [metric:persona_count] [source:AGENT-TASKBOOK]

Ten scenarios cover industry testing, enterprise services, health-service navigation, education/culture, multilingual arrival, low-speed delivery, public-space sensing, developer events, community-service matching and urban-operations assistance. Every scenario states location, user, non-AI baseline, human takeover, exit and risk. Industry test scenarios remain bounded and reversible. [metric:ai_scenario_count] [metric:industry_test_scenario_count]

Three flagship pilots keep the prerequisite → limited test → readable receipt → GO / REVISE / STOP protocol. v0.12.s makes STOP a spatial state: after STOP, the package must return to the ordinary physical route and human-service baseline rather than leaving a new barrier behind. [source:AGENT-TASKBOOK]

## Land Use, Building Scale, and Retain-Renovate-Demolish Strategy

The proposal uses allowed residential, community-service, research, cultural, educational, commercial-service and park-green categories. Thirteen conceptual land-use features and thirteen conceptual building prototypes test adjacency among housing, public service, R&D, commerce, green space and public ground floors. They are design models, not surveyed buildings or approved development capacity. [data:geometry/land_use.geojson#LU-001] [data:geometry/buildings.geojson#BLDG-001]

Approved FAR, height, density, setbacks, road redlines and building-by-building retain/renovate/demolish decisions remain pending official planning, ownership, structural, fire and heritage data. v0.12.s avoids unsupported engineering dimensions and instead defines public performance that later design must preserve. [source:PLANNING-LIMITS] [depth:development_intensity_controls]

The sequence is survey and control verification first, then retain/renovate/demolish/new-build decisions. At the current data depth only reversible infill/reuse research actions are proposed. [depth:retain_renovate_demolish]

## Transport, Rail, Municipal Infrastructure, and Public Services

![Mobility and blue-green public-space system](assets/figures/mobility-bluegreen.en.png)

A north-south public green spine and six east-west stitches form the conceptual walking, cycling and accessible network. Road centerlines are connection intentions, not road redlines. Dazhongsi's ARRIVE WITHOUT APP relies on fixed wayfinding, staffed help and ordinary waiting/retail while real vertical engineering awaits verified road, rail and station data. [depth:traffic_rail_slow_parking] [source:ALLOWED-DESIGN-SPACE]

Municipal and digital infrastructure follow the same failsafe discipline: basic lighting, help access, accessibility, drainage and ordinary public service should not depend on one AI platform remaining online. Edge compute, sensing and digital services remain replaceable overlays; utility capacity and device specifications require later surveys. [depth:municipal_new_infrastructure]

## Blue-Green Network, Public Space, and Urban Character

The Jing-Zhang heritage park and civic green spine are the primary non-digital public infrastructure: continuous walking, shade, staying, rainwater, heritage memory and free use come first. Sensing, digital guidance and event information are optional overlays. [depth:blue_green_public_space] [metric:green_ratio]

The three pilgrimage/recognition nodes remain functional: Open Test Yard demonstrates that testing can stop; City Commons Hall demonstrates that public service does not require an account; Jing-Zhang Civic Station demonstrates arrival without an app. They are civic spaces and knowledge/recognition interfaces first, technology experiences second. [source:AGENT-TASKBOOK]

Urban character differs by type: visible R&D boundaries at Zhongzhiyuan, everyday streets/shade/public ground floors at AI Origin, and legible station-city/heritage continuity at Dazhongsi. A common state-signage hierarchy does not claim to be a government standard. [source:AGENT-TASKBOOK]

## Renewal Projects, Implementation Policy, and Phasing

Implementation is organized by release gates rather than invented construction dates. **G0 BASELINE** audits the ordinary task and missing data. **G1 STEWARDSHIP** assigns proposed roles, manual takeover, maintenance and exit. **G2 REVERSIBLE PILOT** permits only overlays that do not displace S0. **G3 SCALE / ROLLBACK** advances after acceptance or returns to the baseline when any ordinary route/service is blocked. [data:geometry/phasing.geojson#PHASE-001] [depth:phasing_implementation]

Five role types must eventually be owned by real legal entities: public-realm management, basic public service/manual takeover, test operation, station-city public interface and cross-project review. The concept names roles rather than pretending that a specific agency or company has already accepted them. [source:AGENT-TASKBOOK]

Long-term operations include developer/public events, scenario access, international communication, civic experience routes and conversion of successful pilots into durable services. All activities, financing and policy arrangements remain proposals. Every enhancement has an exit design so operator or model replacement does not leave unmaintainable dedicated barriers. [source:AGENT-TASKBOOK]

## Metrics, Area Recalculation, and Compliance Matrix

![Fixed metrics, release gates and evidence closure](assets/figures/metrics-evidence.en.png)

Fixed package metrics remain consistency evidence: `site_area_sqm=11412825.386`, `green_ratio=0.195008`, `public_space_ratio=0.033824`, and `green_space_area_sqm=2225592.728`. They are proposal-derived quantities from provisional geometry, not statutory controls; official geometry requires recalculation. [metric:site_area_sqm] [metric:green_ratio]

The new acceptance logic uses concept-coverage targets rather than fabricated field performance: 3/3 key areas bind to one spatial contract; 3/3 critical tasks state a no-AI/account/test completion path; 3/3 state manual takeover; 3/3 state GO / REVISE / STOP and rollback conditions. These are proposal completeness criteria, not field-performance claims. `metrics.json` now exposes the contract count, AI-OFF critical-task coverage and G0–G3 release-gate count to the structured review path. [metric:spatial_contract_count] [metric:ai_off_critical_task_coverage_ratio] [metric:civic_release_gate_count]

`compliance_matrix.json` maps the contracts to announcement 1.3/1.4/1.5 and agent.1-agent.6; `design_depth_matrix.json` maps them into structure, key-area design, transport, municipal systems, public space, phasing and risk. The purpose is semantic alignment across prose, matrices, five canonical figures, report and PDFs. [source:FORMAL-GUIDE]

## Risk, Copyright, and Compliance

The largest spatial risk remains provisional `SITE_BOUNDARY` and `KEY_AREA` geometry, especially the known absolute-location risk of the Dazhongsi rough polygon. The proposal therefore does not output real station exits, property boundaries, road redlines, bridge/tunnel engineering, approved FAR/height or approved demolition decisions. [source:KEY-AREA-SOURCE] [depth:risk_missing_data]

Data and algorithm risk follows minimum necessity: basic movement, care, public space and staffed service remain available when personal data is refused; high-risk judgments transfer to humans; refusing a test cannot remove civic rights. Operational risk is handled through G0-G3 and S0-S3: enhancement may stop, the city must not stop with it. [source:AGENT-TASKBOOK]

All new figures are generated from package geometry, metrics and original diagrams. No remote map screenshot, unlicensed portrait, government emblem or third-party corporate logo is used. C7 COMPLETE LOOP and the three spatial contracts are proposal identities, not official branding, government policy, implementation commitments or claims of completed field tests. [source:SOURCE-REGISTRY]

## References

1. Centennial Jing-Zhang AI Innovation Belt public announcement and task requirements. [source:OFFICIAL-ANNOUNCEMENT]
2. `brief/site-package/` and the source registry for evidence status. [source:SITE-PACKAGE]
3. Agent taskbook for positioning, functions and the six agent tasks. [source:AGENT-TASKBOOK]
4. Public urban-design and regulatory-planning standards for professional-depth boundaries. [standard:MOHURD-CONTROL-DETAILED-PLANNING]
5. Registered Haidian urban-renewal, AI-industry and public planning references, used only within their evidence status. [source:HD-URBAN-RENEWAL-GUIDE-2025]
