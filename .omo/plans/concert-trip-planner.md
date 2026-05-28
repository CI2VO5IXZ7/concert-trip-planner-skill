# 演唱会特种兵行程规划器 (OpenClaw Skill)

## TL;DR

> **Quick Summary**: Build an OpenClaw Skill that instructs AI agents to plan tight "special forces" concert trips by searching live concert info, orchestrating FlyAI for round-trip transport, and AMap for local venue routing, producing a minute-by-minute itinerary with risk assessment.
>
> **Deliverables**:
> - `SKILL.md` — main skill entry point and behavior guide
> - `references/concert-info-search.md` — how to search and verify concert details
> - `references/flyai-transport-search.md` — how to call FlyAI for flights/trains
> - `references/amap-local-route-planning.md` — how to call AMap for local routes
> - `references/trip-output-template.md` — output format and minute-by-minute template
> - `references/risk-and-buffer-rules.md` — buffer times, feasibility checks, risk scoring
>
> **Estimated Effort**: Short
> **Parallel Execution**: YES — 2 waves
> **Critical Path**: Task 1-6 (parallel) → Task 7 → F1-F4

---

## Context

### Original Request
用户需要一个看演唱会特种兵行程的规划工具，基于 FlyAI 技能和 AMap Skills。用户输入城市和日期，agent 询问期望到达时间，然后调用技能规划行程。

### Interview Summary
**Key Discussions**:
- **载体**: OpenClaw Skill（技能文件形式）
- **技能依赖**: FlyAI + AMap Skills
- **用户输入**: 出发城市、演唱会名称（agent 网上搜索地址和开场时间）、返程时间和地点
- **行程模式**: 无限制，用户完全自定义时间窗口
- **规划维度**: 往返大交通 + 当地交通（机场/车站 ↔ 场馆）
- **排除项**: 吃喝玩乐推荐、酒店搜索（除非过夜且用户明确要求）

**Research Findings**:
- FlyAI 提供 `search-flight`, `search-train`, `search-hotel`, `search-poi`, `keyword-search`, `ai-search`
- AMap JSAPI Skills 提供 geocoding, route planning (driving/walking/cycling/transit), POI search
- OpenClaw skills follow `SKILL.md + references/` structure
- Skill is behavior guidance, not an executable app

### Metis Review
**Identified Gaps** (addressed in plan):
- Added source citation requirement for concert info
- Added minimum buffer rules (venue 60min, airport 90min, train 45min, local 20min)
- Added feasibility assessment and risk scoring
- Added "no viable plan" handling
- Locked down scope creep areas (no food/fun, no hotels unless explicitly needed)

---

## Work Objectives

### Core Objective
Build an OpenClaw Skill that, given a user's departure city, target concert, and return constraints, searches live concert information online and produces a minute-by-minute "special forces" itinerary using FlyAI for round-trip transport and AMap for local venue routing, with explicit feasibility assessment and buffer rules.

### Concrete Deliverables
- `SKILL.md` — main skill entry point
- `references/concert-info-search.md`
- `references/flyai-transport-search.md`
- `references/amap-local-route-planning.md`
- `references/trip-output-template.md`
- `references/risk-and-buffer-rules.md`

### Definition of Done
- [ ] All 6 files exist in the skill directory
- [ ] SKILL.md references all reference files correctly
- [ ] Agent QA test passes with sample prompt (Jay Chou Beijing concert scenario)

### Must Have
- Concert info search with source citation
- Round-trip major transport search via FlyAI
- Local transport route planning via AMap
- Minute-by-minute itinerary output
- Buffer time rules and risk assessment
- "No viable plan" explicit handling
- Scope guardrails in SKILL.md

### Must NOT Have (Guardrails)
- Food/entertainment/POI recommendations around venue
- Hotel search unless user explicitly asks for overnight stay
- Ticket purchasing or booking actions
- Standalone web/mobile app
- Calendar integration
- Group coordination or budget tracking
- **禁止编造**: Agent MUST NOT fabricate concert times, transport schedules, venue addresses, or travel durations
- **禁止过度承诺**: All plans MUST be framed as "based on current search results" — never guaranteed
- **城市名歧义处理**: If multiple cities share the same name, agent MUST ask user to clarify before planning

### Defaults Applied (override if needed)
- **优化目标**: 默认优先"最低风险"而非"最低成本"或"最快到达"
- **演唱会结束时间**: 如官方未公布，按行业标准估算 2.5 小时并加缓冲
- **时间缓冲**: 场馆 60min / 机场 90min / 火车站 45min / 当地交通 20min
- **风险分级**: LOW（所有缓冲满足）、MEDIUM（一项紧张）、HIGH（多项紧张或不可能）

### Spec Framework Integration
- **Detected Framework**: None (this is a custom OpenClaw Skill, not using OpenSpec or Spec Kit)

---

## Verification Strategy

> **ZERO HUMAN INTERVENTION** — ALL verification is agent-executed.

### Test Decision
- **Infrastructure exists**: NO (Skill is markdown, no code test framework)
- **Automated tests**: None
- **Framework**: N/A
- **Agent QA**: YES — primary verification method

### QA Policy
Every task includes agent-executed QA scenarios. Evidence saved to `.omo/evidence/task-{N}-{scenario-slug}.{ext}`.
- **Skill behavior verification**: Use OpenClaw/Claude Code chat with sample prompts, verify output format and content

---

## Execution Strategy

### Parallel Execution Waves

```
Wave 1 (Start Immediately — all files can be drafted in parallel):
├── Task 1: SKILL.md main entry point [quick]
├── Task 2: Concert info search reference [quick]
├── Task 3: FlyAI transport search reference [quick]
├── Task 4: AMap local route planning reference [quick]
├── Task 5: Trip output template reference [quick]
└── Task 6: Risk and buffer rules reference [quick]

Wave 2 (After Wave 1 — integration and cross-reference):
└── Task 7: Cross-reference audit and consistency check [quick]

Wave 3 (Optimization Wave — v2 features, all parallel):
├── Task 8: Update concert-info-search.md with historical duration search [quick]
├── Task 9: Create extended-transport-options.md [quick]
├── Task 10: Update flyai-transport-search.md with fallback strategy [quick]
├── Task 11: Create reverse-planning-strategy.md [unspecified-high]
└── Task 12: Update risk-and-buffer-rules.md with multi-leg rules [quick]

Wave 4 (V2 integration):
├── Task 13: Update SKILL.md with v2 features [quick]
└── Task 14: Cross-reference audit v2 [quick]

Wave 5 (Re-test):
└── Task 15: V2 test with Wang Sulong case [unspecified-high]

Wave FINAL (After ALL tasks — 8 parallel reviews, then user okay):
├── F1. Plan compliance audit v1 (oracle) — COMPLETED
├── F2. Skill structure review v1 (unspecified-high) — COMPLETED
├── F3. Real agent QA test v1 (unspecified-high) — COMPLETED
├── F4. Scope fidelity check v1 (deep) — COMPLETED
├── F5. V2 feature compliance audit (oracle)
├── F6. V2 skill structure review (unspecified-high)
├── F7. V2 agent QA test — Wang Sulong case (unspecified-high)
└── F8. V2 scope fidelity check (deep)
-> Present results -> Get explicit user okay

Critical Path: 
  V1: Task 1-6 (parallel) → Task 7 → F1-F4 — COMPLETED
  V2: Task 8-12 (parallel) → Task 13-14 → Task 15 → F5-F8 → user okay
Parallel Speedup: ~80% faster than sequential
Max Concurrent: 6 (Wave 1), 5 (Wave 3)
```

### Dependency Matrix
- **1**: None → Blocks 7
- **2**: None → Blocks 7
- **3**: None → Blocks 7
- **4**: None → Blocks 7
- **5**: None → Blocks 7
- **6**: None → Blocks 7
- **7**: 1,2,3,4,5,6 → Blocks F1-F4
- **8**: None → Blocks 13, 14, F5-F8
- **9**: None → Blocks 13, 14, F5-F8
- **10**: None → Blocks 13, 14, F5-F8
- **11**: None → Blocks 13, 14, F5-F8
- **12**: None → Blocks 13, 14, F5-F8
- **13**: 8,9,10,11,12 → Blocks 14, F5-F8
- **14**: 8,9,10,11,12,13 → Blocks F5-F8
- **15**: 8-14 → Blocks F5-F8

### Agent Dispatch Summary
- **1**: **6** — T1-T6 → `quick`
- **2**: **1** — T7 → `quick`
- **3**: **5** — T8-T12 → `quick` (T8, T9, T10, T12), `unspecified-high` (T11)
- **4**: **2** — T13-T14 → `quick` (T13, T14)
- **5**: **1** — T15 → `unspecified-high`
- **FINAL**: **8** — F1-F4 (v1, completed) + F5 → `oracle`, F6 → `unspecified-high`, F7 → `unspecified-high`, F8 → `deep`

---

## TODOs

- [x] 1. SKILL.md — main skill entry point

  **What to do**:
  - Create the main `SKILL.md` file for the OpenClaw Skill
  - Define skill name, description, activation triggers (concert, 演唱会, 特种兵)
  - Describe the overall workflow: collect required user inputs → search concert info → plan outbound transport → plan local route to venue → plan return local route → plan return transport → output itinerary
  - Define required user inputs agent must collect: departure city, concert name + date, earliest departure time/latest arrival preference, return time, return destination (if different from departure city)
  - Reference all `references/` files with relative paths
  - Include scope guardrails (Must Have / Must NOT Have summaries)
  - Include fallback behavior when info is missing or plan is infeasible

  **Must NOT do**:
  - Do NOT include implementation code or API calls
  - Do NOT duplicate full content from reference files — only summarize and link
  - Do NOT add food/entertainment recommendations

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: This is a markdown file write with clear structure requirements
  - **Skills**: [`writing`]
    - `writing`: Technical documentation writing for AI skill behavior guides

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 1 (with Tasks 2-6)
  - **Blocks**: Task 7 (cross-reference audit)
  - **Blocked By**: None

  **References**:
  - FlyAI skill README: https://github.com/alibaba-flyai/flyai-skill.git — canonical OpenClaw Skill structure
  - AMap Skills README: https://github.com/AMap-Web/amap-skills.git — Skill reference pattern

  **Acceptance Criteria**:
  - [ ] `SKILL.md` exists in skill root directory
  - [ ] Contains skill name, description, and activation triggers
  - [ ] Describes the 6-step workflow
  - [ ] Explicitly lists required user inputs: departure city, concert name + date, earliest departure time / latest arrival preference, return time, return destination
  - [ ] References all 5 reference files via relative paths
  - [ ] Includes Must Have / Must NOT Have summaries
  - [ ] Includes "missing info" and "infeasible plan" fallback behavior

  **QA Scenarios**:

  ```
  Scenario: SKILL.md structure is complete
    Tool: Bash
    Preconditions: File written to skill-directory/SKILL.md
    Steps:
      1. grep -c "references/" skill-directory/SKILL.md
      2. grep -c "Must Have\|Must NOT Have" skill-directory/SKILL.md
      3. grep -c "concert\|演唱会\|特种兵" skill-directory/SKILL.md
    Expected Result: All grep counts >= 1, file has at least 5 reference links, workflow described
    Failure Indicators: Missing reference links, no workflow, no guardrails
    Evidence: .omo/evidence/task-1-skill-md-structure.md
  ```

  **Evidence to Capture**:
  - [ ] `task-1-skill-md-structure.md`

  **Commit**: NO (all files committed together after Task 7)

- [x] 2. Concert info search reference

  **What to do**:
  - Create `references/concert-info-search.md`
  - Document how the agent should search for concert information online
  - Include: search strategies (artist name + city + date), reliable sources (official venue sites, ticketing platforms, artist social media), source citation format
  - Include: how to handle ambiguous results (multiple venues, conflicting times), how to verify venue address
  - Include: extraction template (artist, venue name, venue address, date, start time, estimated end time, source URL)

  **Must NOT do**:
  - Do NOT include ticket purchasing instructions
  - Do NOT recommend unofficial/scalper sources
  - Do NOT assume concert end time without noting it's an estimate

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: [`writing`]

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 1 (with Tasks 1, 3-6)
  - **Blocks**: Task 7
  - **Blocked By**: None

  **References**:
  - Web search best practices for event information

  **Acceptance Criteria**:
  - [ ] `references/concert-info-search.md` exists
  - [ ] Contains search strategies for finding concert details
  - [ ] Contains source reliability guidelines
  - [ ] Contains ambiguous result handling procedures
  - [ ] Contains data extraction template

  **QA Scenarios**:
  ```
  Scenario: Reference file covers concert search comprehensively
    Tool: Bash
    Preconditions: File exists
    Steps:
      1. grep -c "search\|搜索" references/concert-info-search.md
      2. grep -c "source\|来源\|citation" references/concert-info-search.md
      3. grep -c "ambiguous\|冲突\|multiple" references/concert-info-search.md
    Expected Result: All counts >= 1
    Evidence: .omo/evidence/task-2-concert-search-ref.md
  ```

  **Evidence to Capture**:
  - [ ] `task-2-concert-search-ref.md`

  **Commit**: NO (groups with Task 1)

- [x] 3. FlyAI transport search reference

  **What to do**:
  - Create `references/flyai-transport-search.md`
  - Document exact FlyAI commands to use for outbound and return transport
  - Include: `search-flight` and `search-train` command syntax with all relevant flags
  - Include: parameter mapping from user constraints (departure city, destination, date, time preferences) to FlyAI flags
  - Include: how to interpret and rank results (by departure time, arrival time, price, duration)
  - Include: round-trip coordination (ensure outbound arrival leaves enough buffer before concert, ensure return departure leaves enough buffer after concert)

  **Must NOT do**:
  - Do NOT include `search-hotel` unless explicitly noted as conditional
  - Do NOT include `search-poi` for entertainment/food
  - Do NOT invent FlyAI command flags not documented in official skill

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: [`writing`]

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 1 (with Tasks 1-2, 4-6)
  - **Blocks**: Task 7
  - **Blocked By**: None

  **References**:
  - FlyAI official README: https://github.com/alibaba-flyai/flyai-skill.git — command reference
  - `search-flight` flags: origin, destination, dep-date, back-date, journey-type, sort-type
  - `search-train` flags: origin, destination, dep-date, seat-class-name, journey-type, sort-type

  **Acceptance Criteria**:
  - [ ] `references/flyai-transport-search.md` exists
  - [ ] Documents `search-flight` command with all relevant flags
  - [ ] Documents `search-train` command with all relevant flags
  - [ ] Contains parameter mapping guide
  - [ ] Contains result ranking guidance
  - [ ] Contains round-trip buffer coordination logic

  **QA Scenarios**:
  ```
  Scenario: FlyAI reference is accurate and complete
    Tool: Bash
    Preconditions: File exists
    Steps:
      1. grep -c "search-flight\|search-train" references/flyai-transport-search.md
      2. grep -c "origin\|destination\|dep-date" references/flyai-transport-search.md
      3. grep -c "buffer\|round-trip\|往返" references/flyai-transport-search.md
    Expected Result: All counts >= 2
    Evidence: .omo/evidence/task-3-flyai-ref.md
  ```

  **Evidence to Capture**:
  - [ ] `task-3-flyai-ref.md`

  **Commit**: NO (groups with Task 1)

- [x] 4. AMap local route planning reference

  **What to do**:
  - Create `references/amap-local-route-planning.md`
  - Document how to use AMap Skills for local transportation
  - Include: geocoding venue address and station/airport addresses
  - Include: route planning commands (driving, transit, walking) from station/airport to venue and back
  - Include: how to estimate travel time and select best mode based on time of day
  - Include: late-night fallback (what if public transit is closed after concert)
  - Include: POI search limited to venue/station/airport lookup only

  **Must NOT do**:
  - Do NOT include food/entertainment POI search
  - Do NOT include sightseeing recommendations
  - Do NOT use AMap for anything beyond logistics routing

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: [`writing`]

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 1 (with Tasks 1-3, 5-6)
  - **Blocks**: Task 7
  - **Blocked By**: None

  **References**:
  - AMap Skills README: https://github.com/AMap-Web/amap-skills.git — routing and geocoding capabilities
  - AMap routing.md: route planning (driving, walking, cycling, transit)
  - AMap geocoder.md: address to coordinates

  **Acceptance Criteria**:
  - [ ] `references/amap-local-route-planning.md` exists
  - [ ] Documents geocoding workflow
  - [ ] Documents route planning for at least 2 modes (transit + driving/taxi)
  - [ ] Contains late-night fallback guidance
  - [ ] Explicitly limits POI search to logistics only

  **QA Scenarios**:
  ```
  Scenario: AMap reference covers local transport
    Tool: Bash
    Preconditions: File exists
    Steps:
      1. grep -c "route\|路线\|routing" references/amap-local-route-planning.md
      2. grep -c "geocod\|编码" references/amap-local-route-planning.md
      3. grep -c "late-night\|夜间\|fallback" references/amap-local-route-planning.md
    Expected Result: All counts >= 1
    Evidence: .omo/evidence/task-4-amap-ref.md
  ```

  **Evidence to Capture**:
  - [ ] `task-4-amap-ref.md`

  **Commit**: NO (groups with Task 1)

- [x] 5. Trip output template reference

  **What to do**:
  - Create `references/trip-output-template.md`
  - Define the exact output format the agent should produce
  - Include: header (concert info with sources), timeline (minute-by-minute schedule), transport details (outbound + return), local routes (to venue + from venue), risk assessment, buffer summary
  - Include: markdown template with placeholders
  - Include: example output for a sample trip

  **Must NOT do**:
  - Do NOT include food/entertainment sections in template
  - Do NOT include hotel sections unless conditional
  - Do NOT make template so rigid that agent cannot adapt to edge cases

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: [`writing`]

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 1 (with Tasks 1-4, 6)
  - **Blocks**: Task 7
  - **Blocked By**: None

  **References**:
  - FlyAI output format (JSON results rendered as markdown)
  - AMap route output format

  **Acceptance Criteria**:
  - [ ] `references/trip-output-template.md` exists
  - [ ] Contains markdown template with placeholders
  - [ ] Contains minute-by-minute timeline structure
  - [ ] Contains risk assessment section
  - [ ] Contains at least one complete example

  **QA Scenarios**:
  ```
  Scenario: Output template is complete and usable
    Tool: Bash
    Preconditions: File exists
    Steps:
      1. grep -c "template\|模板\|placeholder" references/trip-output-template.md
      2. grep -c "timeline\|时间表\|schedule" references/trip-output-template.md
      3. grep -c "risk\|风险\|assessment" references/trip-output-template.md
      4. grep -c "example\|示例\|sample" references/trip-output-template.md
    Expected Result: All counts >= 1
    Evidence: .omo/evidence/task-5-output-template.md
  ```

  **Evidence to Capture**:
  - [ ] `task-5-output-template.md`

  **Commit**: NO (groups with Task 1)

- [x] 6. Risk and buffer rules reference

  **What to do**:
  - Create `references/risk-and-buffer-rules.md`
  - Define minimum buffer times: venue arrival 60min before start, airport arrival 90min before flight, train station 45min before departure, local transit 20min buffer
  - Define risk scoring: LOW (all buffers met), MEDIUM (one buffer tight), HIGH (multiple buffers tight or impossible)
  - Define "no viable plan" conditions and response template
  - Define how to handle uncertain concert end time (use estimate + buffer)
  - Define how to handle last-mile unavailability (late night, no transit)

  **Must NOT do**:
  - Do NOT reduce buffers below safety minimums
  - Do NOT present high-risk plans without explicit risk warnings
  - Do NOT skip feasibility check before presenting plan

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: [`writing`]

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 1 (with Tasks 1-5)
  - **Blocks**: Task 7
  - **Blocked By**: None

  **References**:
  - Travel industry standard buffer recommendations
  - Metis review findings on buffer rules

  **Acceptance Criteria**:
  - [ ] `references/risk-and-buffer-rules.md` exists
  - [ ] Documents all 4 buffer rules with exact times
  - [ ] Contains risk scoring rubric (LOW/MEDIUM/HIGH)
  - [ ] Contains "no viable plan" response template
  - [ ] Contains uncertain end time handling
  - [ ] Contains last-mile fallback guidance

  **QA Scenarios**:
  ```
  Scenario: Risk rules are comprehensive
    Tool: Bash
    Preconditions: File exists
    Steps:
      1. grep -c "buffer\|缓冲\|minimum" references/risk-and-buffer-rules.md
      2. grep -c "LOW\|MEDIUM\|HIGH\|风险" references/risk-and-buffer-rules.md
      3. grep -c "no viable\|不可行\|infeasible" references/risk-and-buffer-rules.md
      4. grep -c "last-mile\|最后一公里\|late night" references/risk-and-buffer-rules.md
    Expected Result: All counts >= 1
    Evidence: .omo/evidence/task-6-risk-rules.md
  ```

  **Evidence to Capture**:
  - [ ] `task-6-risk-rules.md`

  **Commit**: NO (groups with Task 1)

- [x] 7. Cross-reference audit and consistency check

  **What to do**:
  - Read all 6 skill files (SKILL.md + 5 references)
  - Verify all cross-references are correct (SKILL.md links to existing reference files, reference files don't contradict each other)
  - Verify consistent terminology (e.g., "concert" vs "演唱会" used consistently)
  - Verify buffer rules referenced in SKILL.md match risk-and-buffer-rules.md exactly
  - Verify FlyAI command examples in flyai-transport-search.md match official documentation
  - Verify AMap route modes in amap-local-route-planning.md match AMap Skills capabilities
  - Fix any inconsistencies found

  **Must NOT do**:
  - Do NOT rewrite content unnecessarily — only fix inconsistencies
  - Do NOT add new scope beyond what's in the reference files

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: NO
  - **Parallel Group**: Sequential (after Wave 1)
  - **Blocks**: F1-F4
  - **Blocked By**: Tasks 1-6

  **References**:
  - All files created in Tasks 1-6

  **Acceptance Criteria**:
  - [ ] All SKILL.md reference links resolve to existing files
  - [ ] No contradictions between reference files
  - [ ] Buffer rules consistent across all files
  - [ ] FlyAI commands match official docs
  - [ ] AMap modes match official capabilities
  - [ ] No-fabrication guardrail documented in SKILL.md and risk-and-buffer-rules.md
  - [ ] City-name-disambiguation handling documented in SKILL.md or concert-info-search.md

  **QA Scenarios**:
  ```
  Scenario: All cross-references are valid
    Tool: Bash
    Preconditions: All Wave 1 files exist
    Steps:
      1. Extract all markdown links from SKILL.md
      2. Verify each linked file exists in references/
      3. grep for buffer times across all files and compare
    Expected Result: 0 broken links, buffer times identical across files
    Evidence: .omo/evidence/task-7-cross-ref-audit.md
  ```

  **Evidence to Capture**:
  - [ ] `task-7-cross-ref-audit.md`

  **Commit**: YES (single commit for all skill files)
  - Message: `feat(skill): add concert trip planner skill`
  - Files: `SKILL.md`, `references/*.md`

- [x] 8. 更新 concert-info-search.md — 添加历史演唱会时长搜索策略

  **What to do**:
  - 在 `references/concert-info-search.md` 中新增"时长验证"章节
  - 定义策略：搜索到具体主题（如"汪苏泷 明日世界"）后，必须搜索该主题的历史场次时长
  - 如果该主题是新主题/第一场，则搜索该艺人过往演唱会主题的平均时长
  - 添加搜索关键词模板："{艺人} {主题} 演唱会 时长"、"{艺人} 演唱会 几点结束"
  - 添加数据来源要求：必须引用来源，标注信心度
  - 修改默认估算规则：不再固定使用 start + 2.5h，而是使用搜索到的历史数据
  - 如果无法找到历史数据，才使用 2.5h 作为保守估计，并标注为 estimate

  **Must NOT do**:
  - 不要删除现有 concert-info-search.md 的其他内容
  - 不要改变文件的整体结构

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: [`writing`]

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 3 (with Tasks 9-12)
  - **Blocks**: Task 14, F5-F8
  - **Blocked By**: None (incremental update)

  **Acceptance Criteria**:
  - [ ] `references/concert-info-search.md` 包含"时长验证"章节
  - [ ] 章节包含历史时长搜索策略（主题级 → 艺人级）
  - [ ] 章节包含搜索关键词模板
  - [ ] 章节包含数据来源和信心度标注要求
  - [ ] 默认估算规则已更新为优先使用历史数据

  **QA Scenarios**:
  ```
  Scenario: Duration search strategy documented
    Tool: Bash
    Preconditions: File exists
    Steps:
      1. grep "时长" references/concert-info-search.md
      2. Verify "历史" or "过往" mentioned
      3. Verify "主题" or "艺人" mentioned in duration context
    Expected Result: Duration validation section exists with clear strategy
    Evidence: .omo/evidence/task-8-duration-search.md
  ```

  **Evidence to Capture**:
  - [ ] `task-8-duration-search.md`

  **Commit**: YES (grouped with Wave 3)

- [x] 9. 新建 extended-transport-options.md — 特种兵扩展交通方式指南

  **What to do**:
  - 新建 `references/extended-transport-options.md`
  - 定义特种兵允许的所有交通方式（不怕苦不怕累）
  - 允许的方式：火车/高铁/动车、飞机、顺风车（滴滴/哈啰等）、自驾（含租车）、机场过夜、车站过夜、凌晨大巴、夜间大巴、附近城市中转（多段联运）
  - 明确排除：包车/专车（费用过高）
  - 为每种方式添加：使用场景、搜索方法、优缺点、注意事项
  - 过夜场景：机场过夜指南（哪些机场允许、休息区位置）、车站过夜指南
  - 顺风车：搜索平台、安全提示、时间不确定性处理
  - 自驾：租车平台、驾驶疲劳提醒、轮换驾驶建议
  - 多段联运：如何组合不同交通方式、中转缓冲时间建议

  **Must NOT do**:
  - 不要包含包车/专车信息
  - 不要变成通用旅游指南，保持特种兵视角（紧凑、省钱、能吃苦）

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: [`writing`]

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 3 (with Tasks 8, 10-12)
  - **Blocks**: Task 13, 14, F5-F8
  - **Blocked By**: None

  **Acceptance Criteria**:
  - [ ] `references/extended-transport-options.md` 存在
  - [ ] 包含所有允许的交通方式清单
  - [ ] 明确排除包车/专车
  - [ ] 包含过夜场景指南（机场+车站）
  - [ ] 包含顺风车搜索和安全提示
  - [ ] 包含自驾/租车信息
  - [ ] 包含多段联运组合策略

  **QA Scenarios**:
  ```
  Scenario: Extended transport options documented
    Tool: Bash
    Preconditions: New file exists
    Steps:
      1. grep -i "顺风车\|自驾\|过夜\|大巴\|中转" references/extended-transport-options.md
      2. Verify "包车" marked as excluded
      3. Verify at least 8 transport modes covered
    Expected Result: Comprehensive guide with all modes and clear exclusions
    Evidence: .omo/evidence/task-9-extended-transport.md
  ```

  **Evidence to Capture**:
  - [ ] `task-9-extended-transport.md`

  **Commit**: YES (grouped with Wave 3)

- [x] 10. 更新 flyai-transport-search.md — 整合扩展交通方式

  **What to do**:
  - 在 `references/flyai-transport-search.md` 中新增"扩展交通方式"章节
  - 说明 FlyAI 的 `search-train` 和 `search-flight` 是基础工具
  - 补充其他交通方式的搜索方法（非 FlyAI 工具，需要 agent 主动搜索）
  - 顺风车：使用 web search 搜索"{起点} 到 {终点} 顺风车"
  - 大巴：使用 web search 搜索"{起点} 汽车站 {终点} 班次"
  - 自驾：使用 AMap route planning (driving mode) 获取路线和时间
  - 过夜：使用 FlyAI `search-hotel` 搜索机场/车站附近酒店（仅用于过夜场景）
  - 添加"当 FlyAI 找不到直达方案时"的 fallback 策略

  **Must NOT do**:
  - 不要删除现有的 FlyAI 命令文档
  - 不要声称 FlyAI 支持顺风车/大巴（它不支持，需要 web search）

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: [`writing`]

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 3 (with Tasks 8-9, 11-12)
  - **Blocks**: Task 13, 14, F5-F8
  - **Blocked By**: None

  **Acceptance Criteria**:
  - [ ] `references/flyai-transport-search.md` 包含扩展交通方式章节
  - [ ] 明确区分 FlyAI 原生支持的 vs 需要 web search 的
  - [ ] 包含 fallback 策略：当 FlyAI 无直达方案时怎么办

  **QA Scenarios**:
  ```
  Scenario: FlyAI fallback strategy documented
    Tool: Bash
    Preconditions: File updated
    Steps:
      1. grep "fallback\|无直达\|找不到" references/flyai-transport-search.md
      2. Verify "web search" mentioned for non-FlyAI modes
    Expected Result: Clear fallback strategy for missing direct routes
    Evidence: .omo/evidence/task-10-flyai-fallback.md
  ```

  **Evidence to Capture**:
  - [ ] `task-10-flyai-fallback.md`

  **Commit**: YES (grouped with Wave 3)

- [x] 11. 新建 reverse-planning-strategy.md — 反向拼图规划策略

  **What to do**:
  - 新建 `references/reverse-planning-strategy.md`
  - 定义"反向凑行程"策略：先看"几点前有哪些车次到目的地"，再反向找来源
  - 步骤：
    1. 搜索"{截止时间} 前到 {目的地} 的所有车次/航班"
    2. 分析这些车次/航班的来源方向
    3. 判断哪些来源方向靠近演唱会城市
    4. 对靠近的来源方向，搜索"演唱会城市 → 中转城市"的交通
    5. 拼接完整行程
  - 定义中转城市选择规则：
    - 优先选择距离演唱会城市较近的城市（减少第一段路程）
    - 中转时间建议最少 30-60 分钟（特种兵标准，可接受较短）
    - 考虑过夜中转（车站/机场过夜）
  - 添加拼图规划示例：太原→泰州（次日8:00前）的案例分析
    - 步骤1：搜索8:00前到泰州的车次
    - 步骤2：发现这些车次主要来自南京/徐州/上海方向
    - 步骤3：搜索太原→南京/徐州的交通
    - 步骤4：拼接多段联运方案
  - 定义"先查返程，再查去程"的规则：特种兵行程返程更难，返程优先

  **Must NOT do**:
  - 不要变成通用中转攻略，保持特种兵视角
  - 不要虚构车次/航班作为示例（使用通用示例格式）

  **Recommended Agent Profile**:
  - **Category**: `unspecified-high`
  - **Skills**: [`writing`]
    - Reason: 需要逻辑性强的策略文档，不是简单的列表

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 3 (with Tasks 8-10, 12)
  - **Blocks**: Task 13, 14, F5-F8
  - **Blocked By**: None

  **Acceptance Criteria**:
  - [ ] `references/reverse-planning-strategy.md` 存在
  - [ ] 包含反向搜索的5个步骤
  - [ ] 包含中转城市选择规则（距离优先、时间缓冲、过夜选项）
  - [ ] 包含拼图规划示例（太原→泰州案例）
  - [ ] 包含"返程优先"规则

  **QA Scenarios**:
  ```
  Scenario: Reverse planning strategy documented
    Tool: Bash
    Preconditions: New file exists
    Steps:
      1. grep "反向\|拼图\|中转\|返程优先" references/reverse-planning-strategy.md
      2. Verify step-by-step strategy present
      3. Verify example case study present
    Expected Result: Comprehensive reverse planning guide with clear rules and example
    Evidence: .omo/evidence/task-11-reverse-planning.md
  ```

  **Evidence to Capture**:
  - [ ] `task-11-reverse-planning.md`

  **Commit**: YES (grouped with Wave 3)

- [x] 12. 更新 risk-and-buffer-rules.md — 新增反向规划和中转规则

  **What to do**:
  - 在 `references/risk-and-buffer-rules.md` 中新增章节：
    - "中转缓冲时间"：建议最少 30-60 分钟（特种兵标准，低于常规）
    - "过夜中转"：机场/车站过夜的风险和注意事项
    - "多段联运风险"：每增加一段联运，风险等级提升一级（LOW→MEDIUM→HIGH）
    - "反向规划优先级"：当直达不可行时，自动启动反向规划
  - 更新风险分级规则：
    - LOW：所有缓冲满足，直达或最多1段中转
    - MEDIUM：一项紧张，或多段联运（2段）
    - HIGH：多项紧张，或3段以上联运，或需要过夜中转
    - NO VIABLE：所有组合均不可行
  - 更新"约束预检"规则（如果之前已添加）：
    - 当直达不可行时，不直接输出 NO VIABLE，而是启动反向规划
    - 只有当反向规划也找不到可行方案时，才输出 NO VIABLE

  **Must NOT do**:
  - 不要删除现有的缓冲规则和风险分级
  - 不要降低安全标准（过夜需注意安全提示）

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: [`writing`]

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 3 (with Tasks 8-11)
  - **Blocks**: Task 13, 14, F5-F8
  - **Blocked By**: None

  **Acceptance Criteria**:
  - [ ] `references/risk-and-buffer-rules.md` 包含中转缓冲规则
  - [ ] 包含过夜中转风险提示
  - [ ] 风险分级已更新为多段联运影响
  - [ ] 包含反向规划触发条件

  **QA Scenarios**:
  ```
  Scenario: Risk rules updated for multi-leg trips
    Tool: Bash
    Preconditions: File updated
    Steps:
      1. grep "中转\|联运\|过夜\|反向" references/risk-and-buffer-rules.md
      2. Verify "30.*60" mentioned for transfer buffer
      3. Verify risk escalation per leg mentioned
    Expected Result: Clear multi-leg and overnight risk rules
    Evidence: .omo/evidence/task-12-risk-rules-update.md
  ```

  **Evidence to Capture**:
  - [ ] `task-12-risk-rules-update.md`

  **Commit**: YES (grouped with Wave 3)

- [x] 13. 更新 SKILL.md — 整合所有 v2 改进

  **What to do**:
  - 更新 `SKILL.md`：
    - Workflow 步骤2：增加"搜索并验证演唱会时长（历史数据）"
    - Workflow 步骤3：增加"如直达不可行，启动反向规划策略"
    - Workflow 步骤6：增加"搜索扩展交通方式（顺风车、大巴、自驾、过夜等）"
    - 新增 Reference File：`extended-transport-options.md`
    - 新增 Reference File：`reverse-planning-strategy.md`
    - 更新"Default Optimization Goal"：保持最低风险优先，但增加"不怕苦不怕累"的特种兵精神
    - 更新"Must Have"：增加"扩展交通方式搜索"和"反向拼图规划"
    - 更新"Fixed Buffers"：增加"中转缓冲 30-60 分钟"
  - 确保所有新 reference 文件在 SKILL.md 中被引用

  **Must NOT do**:
  - 不要删除现有的 SKILL.md 内容
  - 不要改变现有的 Must NOT Have（吃喝玩乐仍然排除）

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: [`writing`]

  **Parallelization**:
  - **Can Run In Parallel**: NO
  - **Parallel Group**: Wave 4 (after Wave 3)
  - **Blocks**: Task 14, F5-F8
  - **Blocked By**: Tasks 8-12

  **Acceptance Criteria**:
  - [ ] `SKILL.md` workflow 包含时长验证步骤
  - [ ] `SKILL.md` workflow 包含反向规划触发
  - [ ] `SKILL.md` workflow 包含扩展交通方式
  - [ ] `SKILL.md` 引用所有7个 reference 文件（5个旧+2个新）
  - [ ] `SKILL.md` Must Have 包含新增项

  **QA Scenarios**:
  ```
  Scenario: SKILL.md updated with v2 features
    Tool: Bash
    Preconditions: File updated
    Steps:
      1. grep "时长\|反向\|扩展" SKILL.md
      2. Count reference links in SKILL.md (should be 7)
      3. Verify "extended-transport-options.md" and "reverse-planning-strategy.md" linked
    Expected Result: All v2 features integrated and all refs linked
    Evidence: .omo/evidence/task-13-skillmd-v2.md
  ```

  **Evidence to Capture**:
  - [ ] `task-13-skillmd-v2.md`

  **Commit**: YES (grouped with Wave 4)

- [x] 14. 交叉引用审计 v2 — 一致性检查

  **What to do**:
  - 读取所有8个文件（SKILL.md + 7 references）
  - 验证 SKILL.md 引用所有7个 reference 文件
  - 验证新增 reference 文件之间无矛盾
  - 验证风险规则在所有文件中一致
  - 验证交通方式列表在 flyai-transport-search.md 和 extended-transport-options.md 中一致
  - 验证反向规划策略在 reverse-planning-strategy.md 和 SKILL.md 中描述一致

  **Must NOT do**:
  - 不要重写内容，只修复不一致

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: NO
  - **Parallel Group**: Wave 4 (with Task 13)
  - **Blocks**: Task 15, F5-F8
  - **Blocked By**: Tasks 8-13

  **Acceptance Criteria**:
  - [ ] 所有 reference 链接有效（0 broken links）
  - [ ] 新增文件间无矛盾
  - [ ] 风险规则一致
  - [ ] 交通方式列表一致

  **QA Scenarios**:
  ```
  Scenario: All v2 cross-references valid
    Tool: Bash
    Preconditions: All files exist
    Steps:
      1. Extract all markdown links from SKILL.md
      2. Verify each linked file exists in references/
      3. grep for "中转" and "过夜" across all files and compare definitions
    Expected Result: 0 broken links, consistent definitions
    Evidence: .omo/evidence/task-14-cross-ref-v2.md
  ```

  **Evidence to Capture**:
  - [ ] `task-14-cross-ref-v2.md`

  **Commit**: YES (single commit for all v2 changes)

- [x] 15. 重新测试 — 汪苏泷太原案例验证 v2

  **What to do**:
  - 使用更新后的技能，重新运行测试案例：汪苏泷6/13太原→泰州，次日8:00前到
  - 验证 agent 是否：
    1. 搜索了汪苏泷"明日世界"主题的历史时长
    2. 尝试了反向规划策略（先看8:00前到泰州的车次）
    3. 考虑了扩展交通方式（顺风车、大巴、自驾、过夜中转等）
    4. 尝试了多段联运（太原→中转城市→泰州）
    5. 即使最终仍不可行，展示了所有尝试过的方案
  - 记录 v2 相比 v1 的改进效果

  **Must NOT do**:
  - 不要假设 v2 一定能找到可行方案（交通现实限制仍然存在）
  - 但要评估 v2 是否比 v1 更深入、更全面

  **Recommended Agent Profile**:
  - **Category**: `unspecified-high`
  - **Skills**: [`playwright`]

  **Parallelization**:
  - **Can Run In Parallel**: NO
  - **Parallel Group**: Wave 5 (after Wave 4)
  - **Blocks**: F5-F8
  - **Blocked By**: Tasks 8-14

  **Acceptance Criteria**:
  - [ ] Agent 主动搜索了历史演唱会时长
  - [ ] Agent 尝试了反向规划策略（查看到达车次再反推来源）
  - [ ] Agent 考虑了至少3种扩展交通方式
  - [ ] Agent 尝试了多段联运方案
  - [ ] 即使不可行，展示了所有尝试并给出详细替代建议

  **QA Scenarios**:
  ```
  Scenario: V2 test with Wang Sulong case
    Tool: OpenClaw chat (or web search simulation)
    Preconditions: Skill files updated
    Steps:
      1. Load updated skill
      2. Prompt: "我在泰州，想去看汪苏泷6月13日太原演唱会，次日8点前回到泰州"
      3. Verify agent searches for "汪苏泷 明日世界 演唱会 时长"
      4. Verify agent checks return options creatively (not just direct)
      5. Verify agent provides detailed reasoning if no viable plan
    Expected Result: More thorough search and creative solutions compared to v1
    Evidence: .omo/evidence/task-15-v2-test.md
  ```

  **Evidence to Capture**:
  - [ ] `task-15-v2-test.md`

  **Commit**: NO (test only, no code changes)

---

## Final Verification Wave

> 4 review agents run in PARALLEL. ALL must APPROVE. Present consolidated results to user and get explicit "okay" before completing.

- [x] F1. **Plan Compliance Audit** — `oracle`
  Read the plan end-to-end. For each "Must Have": verify file exists and content addresses requirement. For each "Must NOT Have": search skill files for forbidden patterns. Check evidence files exist in `.omo/evidence/`. Compare deliverables against plan.
  **Acceptance Criteria**:
  - [ ] All 6 skill files exist in expected paths
  - [ ] SKILL.md references all 5 reference files with valid relative paths
  - [ ] No forbidden content (food/fun recommendations, hotel search, ticket purchasing) found in any file
  - [ ] No-fabrication guardrail explicitly stated in at least one file
  - [ ] City-name-disambiguation handling documented in at least one file
  - [ ] Buffer rules documented with exact times in risk-and-buffer-rules.md
  - [ ] Evidence directory contains at least 7 task evidence files
  Output: `Must Have [N/N] | Must NOT Have [N/N] | Tasks [N/N] | VERDICT: APPROVE/REJECT`

- [x] F2. **Skill Structure and Format Review** — `unspecified-high`
  Verify OpenClaw Skill directory structure matches canonical pattern (`SKILL.md` + `references/`). Check all SKILL.md cross-references resolve to existing files. Verify markdown formatting, heading levels, and code block syntax. Check for typos and broken links.
  **Acceptance Criteria**:
  - [ ] Directory structure is `SKILL.md` + `references/*.md`
  - [ ] All cross-references in SKILL.md resolve to existing files (0 broken links)
  - [ ] All reference files have consistent markdown formatting (proper heading levels, code blocks)
  - [ ] No typos in skill name, file names, or reference paths
  Output: `Structure [PASS/FAIL] | References [N/N valid] | Format [PASS/FAIL] | VERDICT`

- [x] F3. **Real Agent QA Test** — `unspecified-high`
  Start OpenClaw/Claude Code with the skill loaded. Execute sample prompt: "I am in Shanghai and want to attend Jay Chou's concert in Beijing on 2026-07-18. I can leave after 08:00 and must return to Shanghai before noon the next day." Verify agent output contains: concert venue + start time (with source), outbound transport options, local route to venue, return local route, return transport options, minute-by-minute schedule, risk assessment. Save evidence to `.omo/evidence/final-qa/`.
  **Acceptance Criteria**:
  - [ ] Agent outputs concert venue and start time with cited source
  - [ ] Agent outputs at least 2 outbound transport options (flight or train)
  - [ ] Agent outputs local route from station/airport to venue
  - [ ] Agent outputs local route from venue to station/airport
  - [ ] Agent outputs at least 2 return transport options
  - [ ] Agent outputs minute-by-minute schedule
  - [ ] Agent outputs explicit risk assessment (LOW/MEDIUM/HIGH)
  - [ ] If plan is infeasible, agent explicitly says so instead of fabricating
  Output: `Scenarios [N/N pass] | Integration [N/N] | Edge Cases [N tested] | VERDICT`

- [x] F4. **Scope Fidelity Check** — `deep`
  For each task: read "What to do", read actual file content. Verify 1:1 — everything in spec was built, nothing beyond spec. Check "Must NOT do" compliance. Detect cross-task contamination. Flag unaccounted changes.
  **Acceptance Criteria**:
  - [ ] Tasks 1-6 have corresponding deliverable files in the skill directory
  - [ ] Task 7 has audit evidence in `.omo/evidence/`
  - [ ] No file contains content beyond its task scope
  - [ ] No forbidden patterns (food/fun/hotel/ticket/fake-data) found in any file
  - [ ] Buffer rules consistent across all files where referenced
  - [ ] No cross-task contamination (e.g., concert search reference doesn't contain FlyAI commands)
  - [ ] No-fabrication guardrail present in at least one file
  - [ ] City-name-disambiguation handling present in at least one file
  Output: `Tasks [N/N compliant] | Contamination [CLEAN/N issues] | Unaccounted [CLEAN/N files] | VERDICT`

- [x] F5. **V2 Feature Compliance Audit** — `oracle`
  Read all skill files end-to-end. Verify v2 features are present:
  - [ ] `references/concert-info-search.md` contains "时长验证" section with historical duration search strategy
  - [ ] `references/extended-transport-options.md` exists and covers at least 8 transport modes with clear exclusions (no包车)
  - [ ] `references/reverse-planning-strategy.md` exists with step-by-step reverse planning guide and example
  - [ ] `references/flyai-transport-search.md` contains fallback strategy for missing direct routes
  - [ ] `references/risk-and-buffer-rules.md` contains multi-leg trip risk escalation rules
  - [ ] `SKILL.md` workflow includes: duration verification, reverse planning trigger, extended transport modes
  - [ ] `SKILL.md` references all 7 reference files (5 old + 2 new)
  Output: `V2 Features [N/N] | Files [N/N] | VERDICT: APPROVE/REJECT`

- [x] F6. **V2 Skill Structure Review** — `unspecified-high`
  Verify v2 directory structure: `SKILL.md` + `references/*.md` (7 files total). Check new reference files have consistent formatting. Verify no typos in new file names or paths.
  **Acceptance Criteria**:
  - [ ] Directory contains 7 reference files
  - [ ] All new cross-references resolve correctly
  - [ ] New files have proper markdown formatting
  Output: `Structure [PASS/FAIL] | New Refs [N/N valid] | Format [PASS/FAIL] | VERDICT`

- [x] F7. **V2 Agent QA Test — Wang Sulong Case** — `unspecified-high`
  Load updated skill. Execute prompt: "我在泰州，想去看汪苏泷6月13日太原演唱会，次日8点前回到泰州". Verify:
  - [ ] Agent searches for historical concert duration
  - [ ] Agent attempts reverse planning (checks arrivals at destination first)
  - [ ] Agent considers at least 3 extended transport modes (顺风车, 大巴, 自驾, 过夜, etc.)
  - [ ] Agent attempts multi-leg routing (太原→中转→泰州)
  - [ ] Agent provides detailed reasoning for each attempted solution
  - [ ] Even if no viable plan, agent shows all attempts and creative alternatives
  Save evidence to `.omo/evidence/final-qa-v2/`.
  Output: `Duration Search [PASS/FAIL] | Reverse Planning [PASS/FAIL] | Extended Modes [PASS/FAIL] | Multi-leg [PASS/FAIL] | VERDICT`

- [x] F8. **V2 Scope Fidelity Check** — `deep`
  For Tasks 8-15: verify deliverables match task specs. Check Tasks 8-12 produce the expected reference file modifications. Check Task 13 updates SKILL.md correctly. Check Task 15 produces test evidence. Verify no scope creep: new files don't contain food/fun recommendations, don't add包车, don't add unrelated features.
  Output: `Tasks 8-15 [N/N compliant] | Contamination [CLEAN/N issues] | Unaccounted [CLEAN/N files] | VERDICT`

---

## Commit Strategy

- **V1 commit**: `feat(skill): add concert trip planner skill` — all skill files (SKILL.md + references/*.md) — COMPLETED
- **V2 commit**: `feat(skill): add reverse planning, extended transport, and historical duration search` — updated SKILL.md + modified references + new references/*.md
- **No per-task commits** — all v2 files committed together after Task 14 completes

---

## Success Criteria

### Verification Commands
```bash
# Verify skill directory structure (run in the skill root directory)
ls -la SKILL.md references/

# Verify all reference files exist (7 total for v2)
ls references/*.md | wc -l

# Verify v2 features present
grep -l "时长\|反向\|扩展" references/*.md SKILL.md
```

### Final Checklist
- [ ] All "Must Have" present in skill files
- [ ] All "Must NOT Have" absent from skill files
- [ ] Agent QA test passes with sample prompt (v1 case: Jay Chou Beijing)
- [ ] Agent QA test passes with v2 case (Wang Sulong Taiyuan)
- [ ] SKILL.md correctly references all 7 reference files
- [ ] Buffer rules and risk assessment documented (including multi-leg rules)
- [ ] "No viable plan" behavior documented (with reverse planning fallback)
- [ ] Historical duration search strategy documented
- [ ] Extended transport options documented (8+ modes, no包车)
- [ ] Reverse planning strategy documented with example
