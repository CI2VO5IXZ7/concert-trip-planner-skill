---
name: concert-trip-planner
description: "Use when the user wants to plan a tight round trip for a concert or live event — including transport search, local venue routing, and minute-by-minute itinerary. Covers trains, flights, local transit, ride shares, and overnight options. 特种兵式演唱会行程规划。"
version: 5.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [travel, concert, trip-planner, transport, itinerary]
    related_skills: [maps]
---

# 🎵 演唱会特种兵行程规划器

Plan tight concert round trips with live concert verification, lowest-risk-first transport choices, local venue routing, and a minute-by-minute itinerary.

## What This Skill Does

Guide through the full concert trip planning workflow:
1. Collect required user inputs.
2. Search and verify current concert information.
3. Plan outbound transport.
4. Plan the local route to the venue.
5. Plan the local route after the concert.
6. Plan the return transport.
7. Output the final itinerary.

All plans must be based on current search results and are not guaranteed.

## Required User Inputs

Before planning, ask for:
- Departure city
- Concert name + date
- Earliest departure time / latest arrival preference
- Return time
- Return destination

If the departure city or return destination is ambiguous, ask for clarification.
If the date is missing, ask for clarification.
If multiple concerts match, ask which one to use.

## Workflow

1. Collect and confirm all required inputs.
2. **Feasibility pre-check (快速粗判)** — before any deep search, estimate viability so you scale effort to the case:
   - Rough distance between departure city and concert city, and whether a direct high-speed rail or flight plausibly exists.
   - Compare concert end time + minimum return travel time against the user's deadline.
   - Output a quick verdict: **高 / 中 / 低 可行性**. If 低 (e.g. 900+ km, no direct line, next-morning hard deadline), tell the user upfront it is likely infeasible and confirm they still want the full search before spending it.
3. Search current concert information, verify venue/date/timing, and verify historical concert duration (reuse same-tour duration if already known).
4. **执行返程搜索矩阵（见下方）— 必须同时遍历所有维度，不可遗漏。**
5. Plan local route from arrival point to venue.
6. Plan local route from venue to the return departure point.
7. Plan outbound major transport (same matrix applies).
8. Produce a concise itinerary with risk assessment and buffer checks.

## ⚠️ 强制搜索矩阵（每次必须全部执行）

**核心原则：不预设结论，不跳过维度。先查再排除。**

### 返程搜索矩阵（演唱会结束后 → 目的地）

必须**同时**发起以下所有搜索，然后综合排序：

| 维度 | 搜索内容 | 工具 |
|---|---|---|
| ① 直达火车 | 演唱会结束后，出发城市→目的地的所有直达火车 | `flyai search-train` |
| ② 直达飞机 | 出发城市→目的地（含附近机场）的所有航班 | `flyai search-flight` |
| ③ 中转火车 | **全量遍历**（见下方详细逻辑） | train_list.js 索引 + flyai |
| ④ 飞机+地面交通 | 飞到目的地附近机场 + 高铁/驾车到目的地 | flyai + 高德 |

### 中转火车全量遍历逻辑

**不要只查"常见中转城市"，必须全量碰撞：**

**Step A — 出发端：** 用 train_list.js 索引查询出发城市所有车站的所有车次（不限目的地），提取每个车次的起点和终点。

**Step B — 到达端：** 用 train_list.js 索引查询目的地所有车站的所有车次（不限出发地），提取每个车次的起点和终点。

**Step C — 交叉匹配：** 将 Step A 的终点集合 与 Step B 的起点集合取交集，交集站点即为**候选中转城市**。

**Step D — 逐个验证：** 对每个候选中转城市，用 `flyai search-train` 验证：
- 出发端车次到达中转城市的时间
- 到达端车次从中转城市出发的时间
- 换乘时间是否满足最低缓冲（同站≥15分钟，跨站≥实测交通时间+15分钟）

**示例命令：**
```bash
# Step A: 查询北京南站所有车次
python3 scripts/train_index_builder.py --query "北京南"
# Step B: 查询无锡所有车次
python3 scripts/train_index_builder.py --query "无锡"
# Step D: 验证中转方案
flyai search-train --origin "北京" --destination "南京" --dep-date 2026-08-23 --dep-hour-start 22
flyai search-train --origin "南京" --destination "无锡" --dep-date 2026-08-24 --arr-hour-end 9
```

### 去程搜索矩阵（出发地 → 演唱会城市）

同样必须同时搜索：直达火车、直达飞机、中转火车、飞机+地面交通。确保在演唱会开始前有充足缓冲（含本地交通时间）。

## Default Optimization Goal

Default to **lowest risk first**, not cheapest or fastest. (特种兵精神: 不怕苦不怕累，直达不是唯一选择，时间优先于舒适)

## Fixed Buffers

- Venue: 60 minutes
- Airport: 90 minutes
- Train station: 45 minutes
- Local route: 20 minutes
- Transfer: 30-60 minutes (特种兵标准，低于常规)

## Environment Check (Run Before Starting)

Before collecting user inputs, verify all required tools are available:

```bash
# 1. flyai — 火车/航班查询（每日100次限额）
flyai --help 2>&1 | head -3 || echo "需安装: npm i -g @fly-ai/flyai-cli"
echo "FLYAI_API_KEY set: ${FLYAI_API_KEY:+yes}"

# 2. train_list.js 索引 — 某站所有车次（无限，静态数据）
python3 ~/.hermes/skills/productivity/concert-trip-planner/scripts/train_index_builder.py 2>&1 || echo "需运行索引构建"

# 3. 高德地图 API Key
echo "GAODE_API_KEY set: ${GAODE_API_KEY:+yes}"
```

## Required Tools

| Task | Primary Tool | 限额 |
|------|-------------|------|
| 火车班次查询（直达+中转） | `flyai search-train` | 100次/天 |
| 航班查询（直达+中转） | `flyai search-flight` | 100次/天 |
| 某站所有车次（全量碰撞） | `train_index_builder.py --query` | **无限**（静态） |
| 车站编码查询 | `train_index_builder.py --query` 或 flyai 返回自带 | **无限** |
| 本地路线 / 距离查询 | 高德地图 REST API (curl) | **无限** |
| 演唱会信息 / 大巴 / 顺风车 | WebSearch | **无限** |
| 酒店 / 景点搜索 | `flyai search-hotel` / `flyai search-poi` | 100次/天 |
| 经停站查询（低频） | 携程问道 API (`node wendao_query.js`) | 30次/天 |

Station and airport names must be verified by flyai results. Never assume or guess station names.

**限额使用策略：** flyai 100次/天用于火车/航班查询（含中转推荐）。携程问道 30次/天仅用于经停站查询等飞猪无法覆盖的场景。train_list.js 索引和高德地图无限使用。

## Must Have

- Live concert info search with source verification
- Round-trip transport planning using flyai (飞猪) + train_list.js index
- Local venue routing using 高德地图 REST API
- Minute-by-minute itinerary output
- Buffer checks and feasibility assessment
- Explicit infeasible-plan handling
- Extended transport mode search (ride share, bus/night bus, self-drive, overnight transit)
- Reverse jigsaw planning when direct routes are infeasible

## Must NOT Have

- Food recommendations
- Fun / entertainment recommendations
- Sightseeing recommendations
- Hotel search unless the user explicitly asks for overnight stay
- Ticket purchasing or booking actions
- Calendar integration
- Group coordination or budget tracking
- Fabrication of concert times, venue addresses, schedules, or travel durations

## Fallback Behavior

If key information is missing, stop and ask only for the missing item(s).
If the plan is infeasible, say so clearly and explain which constraint fails.
If current search results conflict, prefer verified sources and disclose uncertainty.

## Reference Files

Follow the detailed guidance in these references for each step:

- [references/concert-info-search.md](references/concert-info-search.md) — how to search and verify concert info
- [references/transport-search.md](references/transport-search.md) — how to search trains, flights, and transport options
- [references/local-route-planning.md](references/local-route-planning.md) — how to plan local routes to/from venue
- [references/trip-output-template.md](references/trip-output-template.md) — final output format
- [references/risk-and-buffer-rules.md](references/risk-and-buffer-rules.md) — risk levels and buffer rules
- [references/extended-transport-options.md](references/extended-transport-options.md) — extended modes: ride share, bus, self-drive, overnight
- [references/reverse-planning-strategy.md](references/reverse-planning-strategy.md) — reverse jigsaw planning when direct routes fail
- [references/flyai-cli.md](references/flyai-cli.md) — flyai (飞猪) CLI 命令参考、参数、返回格式、已知限制

## Common Pitfalls

1. **演唱会时长必须向用户确认** — 默认 2.5 小时只是兜底。如果用户提供了实际时长（如"汪苏泷都是3.5小时"），必须采用，并在可行性判断中使用。时长直接影响返程可行性。
2. **flyai 返回空结果** — 不要直接判无方案，标注数据可能不完整并提示人工复核。应改用 web_search 补充查询。
3. **高德 Key 类型错误** — JSAPI Key 会返回 10009 错误，必须用 Web服务 Key。
4. **返程双段搜索遗漏** — 凌晨段(0-6点) + 早班段(6-12点)必须分开搜索再合并，否则会漏掉夜车。
5. **中转时间硬拦截** — 同站换乘 < 15 分钟、跨站换乘时间不足的方案直接剔除，不进候选。
6. **train_list.js 索引过期** — 每次查询前必须运行 `train_index_builder.py` 检查更新（自动检查缓存是否有效，7天内不重新下载）。
7. **可行性预判要用实际距离** — 用高德 API 驾车路线查询实际距离和耗时，不要凭感觉估算。>800km + 次日早班硬约束 = 几乎必然不可行。
8. **"无可行方案"也要给出选项** — 即使判断 NO VIABLE，仍需列出所有方案按最早到达排序，让用户自己决定是否放宽约束。不要只说"不可行"就结束。
9. **自驾方案必须附带疲劳警告** — 自驾作为扩展方案时，必须明确标注：单人夜间疲劳驾驶风险极高，建议两人轮换或不采用。
10. **用户不接受提前离场时** — 应搜索演唱会结束时间之后的所有可能交通方式（夜车、深夜航班、自驾），按最早到达排序，而不是只推荐提前离场一个方案。
11. **【致命错误】跳过搜索维度** — 必须同时搜索：直达火车、直达飞机、中转火车、飞机+地面交通。不允许"只查火车不查飞机"或"只查直达不查中转"。每次犯这个错都会被用户纠正。搜索矩阵是强制的，不是建议。
12. **【致命错误】不做中转碰撞** — 中转不能只查"常见城市"（如南京、徐州），必须用 train_list.js 索引全量遍历出发端和到达端的所有车次站点，取交集。参见搜索矩阵的Step A-D。
13. **演唱会时长是关键输入** — 不要默认2.5小时。必须向用户确认，或搜索该歌手的历史演唱会时长。时长直接影响返程可行性判断。

## Verification Checklist

- [ ] flyai CLI 可执行：`flyai --help`
- [ ] FLYAI_API_KEY 已设置
- [ ] train_list.js 索引已建：`python3 scripts/train_index_builder.py`
- [ ] 高德 API Key 有效：`curl -s "https://restapi.amap.com/v3/geocode/geo?address=北京天安门&city=北京&key=$GAODE_API_KEY"`
- [ ] 去程火车/航班搜索返回结果
- [ ] 返程双段搜索（凌晨+早班）均已执行
- [ ] 本地路线（车站/机场→场馆）已规划并加 20 分钟缓冲
- [ ] 分钟级行程单已输出
- [ ] 风险等级已标注（LOW/MEDIUM/HIGH/NO VIABLE）
