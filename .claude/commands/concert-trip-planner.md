# 演唱会特种兵行程规划器

Plan tight concert round trips with live concert verification, lowest-risk-first transport choices, local venue routing, and a minute-by-minute itinerary.

## What This Command Does

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
4. Plan outbound major transport with the lowest-risk option first. If no direct route is feasible, or the return-side deadline is too tight/fragile, trigger reverse planning.
5. Plan local route from arrival point to venue.
6. Plan local route from venue to the return departure point.
7. Plan return major transport, including extended transport modes when needed.
8. Produce a concise itinerary with risk assessment and buffer checks.

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
# 1. FlyAI
flyai --help || npm i -g @fly-ai/flyai-cli

# 2. AMap Key
# Ask the user: "请提供高德地图 Web服务 Key（非JSAPI Key）"
# Verify type: the key must work with https://restapi.amap.com/v3/geocode/geo
# If user provides a JSAPI key, error 10009 will appear — ask them to create a Web服务 Key instead
```

If FlyAI search results include a `体验模式` warning, inform the user that results may be incomplete.

## Required Skills

This command depends on the following skills — invoke them in the order listed:

| Task | Primary Skill | Fallback |
|------|--------------|---------|
| 火车班次查询 | FlyAI skill (`/flyai search-train`) | 12306 skill — **仅交互式会话可用（需扫码登录）** |
| 航班查询 | FlyAI skill (`/flyai search-flight`) | 12306 skill — 同上 |
| 本地路线 / 地址解析 / 距离查询 | 高德地图 REST API (curl) | — (no WebSearch substitution) |
| 演唱会信息 / 大巴班次 / 顺风车 | WebSearch | WebFetch |

Station and airport names must be verified by FlyAI or 12306 results. Never assume or guess station names.

**重要可靠性提醒：** FlyAI 体验模式数据可能不完整，12306 fallback 在无人值守环境不可用。当 FlyAI 返回空或结果稀少时，**不得据此直接判定无方案**，必须标注数据可能不全并提示人工复核。详见 `references/transport-search.md` 的「Data Reliability」章节。

## Must Have

- Live concert info search with source verification
- Round-trip transport planning using FlyAI + 12306
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
