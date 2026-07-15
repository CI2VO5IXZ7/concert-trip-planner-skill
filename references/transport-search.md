# Transport Search Reference

Use 携程问道 (TripAI) API for all major transport searches (train + flight). Search outbound and return as separate passes. Always choose the lowest-risk option first.

## Environment Check

Before any search, verify 携程问道 is available:
```bash
node ~/.hermes/skills/productivity/ctrip-wendao/scripts/wendao_query.js --help 2>&1 || echo "需确认脚本存在"
```

如有需要，可申请 API Key 配置到 `.env` 中（`TRIPAI_API_KEY`）。不配也能用，但可能被限流。

## Tool Priority

1. **携程问道 API** — primary, covers 火车/高铁/航班/景点门票/一日游等全部旅行场景
2. **WebSearch** — last resort only, for supplementary info (bus schedules, ride share); never use for train/flight station name verification

## ⚠️ Data Reliability — Read First

携程问道的数据来自携程官方，一般较完整。但仍需注意：

**Rule:** 当携程问道返回空或结果异常少时，你 MUST NOT 直接判 NO VIABLE PLAN。标注输出：`⚠️ 携程问道返回数据可能不完整，以下结论需人工复核 12306/航司官方余票`。

## Core Rule

- Default ranking: lowest-risk first, then best duration/arrival fit, then price.
- Do not book; only search and compare results.
- If no option satisfies the constraints, report that the plan is infeasible and name the failed constraint — **but only after confirming the data source was complete**.
- Station and airport names must come from 携程问道 results only — never assume or guess station names.
- **Always display full datetime** (`YYYY-MM-DD HH:MM`) for every departure and arrival — never extract time alone.

## Flight Search — Run in Parallel with Train Search

When doing reverse planning, **search flights at the same time as trains** — do not treat flights as an afterthought. For many intercity routes, the first viable return option is a flight, not a train.

Run these searches in parallel:
1. Trains: two-pass return search (凌晨段 + 早班段)
2. Flights to the nearest airport to the return destination
3. Flights to secondary airports (if any, check drive time to final destination)

Merge all results and rank by **earliest arrival at final destination**, not just arrival at terminal station/airport.

## 携程问道 — Train Search

```bash
node ~/.hermes/skills/productivity/ctrip-wendao/scripts/wendao_query.js "{日期} {出发城市/站} 到 {目的地城市/站} 的高铁/动车，{出发时间} 出发，按出发时间排序"
```

### Outbound train example
```bash
node ~/.hermes/skills/productivity/ctrip-wendao/scripts/wendao_query.js "2026-07-15 南京 到 泰州 的高铁，08:00到14:00之间出发，按出发时间排序"
```

### Return train — Two-Pass Mandatory Rule

**Return searches MUST be executed as two separate passes and results merged:**

**Pass 1 — 凌晨段 (midnight to 6am):**
```bash
node ~/.hermes/skills/productivity/ctrip-wendao/scripts/wendao_query.js "{日期} {返程出发城市} 到 {返程目的地} 的火车，凌晨0点到6点之间出发"
```

**Pass 2 — 早班段 (6am to noon):**
```bash
node ~/.hermes/skills/productivity/ctrip-wendao/scripts/wendao_query.js "{日期} {返程出发城市} 到 {返程目的地} 的高铁，06:00到12:00之间出发，按出发时间排序"
```

After both passes complete, merge all results and sort by arrival time at destination. **Skipping Pass 1 will miss critical overnight trains** (e.g. D128 01:29, K558 00:18) that are often the earliest viable option after a late-night concert.

## 携程问道 — Flight Search

```bash
node ~/.hermes/skills/productivity/ctrip-wendao/scripts/wendao_query.js "{日期} {出发城市} 到 {目的地城市} 的航班，{出发时间} 出发"
```

### Flight example
```bash
node ~/.hermes/skills/productivity/ctrip-wendao/scripts/wendao_query.js "2026-07-15 上海 到 南京 的航班，05:00到09:00之间出发"
```

## Ranking Logic

1. Lowest-risk option first: the itinerary that best satisfies all buffers and time windows.
2. Then duration and arrival fit: prefer the option that lands closest to the needed arrival window without violating it.
3. Then price: only use price to break ties after risk and timing.

## Buffer Coordination

- Venue buffer: arrive at venue at least **60 minutes** before show start.
- Airport buffer: arrive at airport at least **90 minutes** before departure.
- Train station buffer: arrive at station at least **45 minutes** before departure.
- Local route buffer: keep **20 minutes** for last-mile transfer.

Coordinate the transport search with the venue plan:
- Outbound arrival must leave time for local transit plus the venue buffer.
- Return departure must leave time for local egress plus the station/airport buffer.
- If the concert end time is uncertain, use the estimate plus the venue buffer before choosing a return option.

## No-Viable-Plan Behavior

If nothing matches the constraints:
- Say the trip is infeasible for the requested windows.
- Identify the failing constraint.
- Trigger reverse planning (see `reverse-planning-strategy.md`).
- Try extended transport modes (see `extended-transport-options.md`).
- Ask for a wider time window or a relaxed constraint before searching again.

## Extended Transport Modes

When direct trains and flights are unavailable or infeasible:

- **顺风车**: WebSearch `{起点} 到 {终点} 顺风车 {日期}`
- **长途大巴 / 夜巴**: WebSearch `{起点} 长途汽车站 {终点} 班次时刻` or `{起点} 到 {终点} 夜间大巴`
- **自驾/租车**: Use AMap REST API driving route (`/v3/direction/driving`) to get distance and estimated drive time
- **机场/车站过夜**: WebSearch `{机场或车站名} 24小时候车区 过夜` for rules and areas
- **多段联运**: Search each leg separately with 携程问道, then stitch by buffer

See `extended-transport-options.md` for full guidance on each mode.

## Fallback Strategy: When No Direct Route Is Found

1. Loosen search constraints: widen time window, try nearby stations/airports via 携程问道 (`"{城市} 附近有哪些高铁站"`).
2. Start reverse planning — see `reverse-planning-strategy.md`.
3. Consider extended transport modes — see `extended-transport-options.md`.
4. If all options remain infeasible, clearly explain which constraint failed and why.

## Reverse Planning Trigger

- When the return-time window is extremely tight, run the return search first.
- Return-first principle: confirm whether arrival before the deadline is possible before optimizing the outbound leg.
