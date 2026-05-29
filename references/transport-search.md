# Transport Search Reference

Use FlyAI skill (primary) and 12306 skill (fallback) for all major transport searches. Search outbound and return as separate passes. Always choose the lowest-risk option first.

## Environment Check

Before any search, verify FlyAI is available:
```bash
flyai --help
```
If not found, install it first:
```bash
npm i -g @fly-ai/flyai-cli
```
If FlyAI returns a `体验模式` warning in results, note that output may be incomplete — inform the user and suggest obtaining a full API key at https://flyai.open.fliggy.com/

## Tool Priority

1. **FlyAI CLI** (`flyai search-train` / `flyai search-flight`) — primary, real-time data, verified station names
2. **12306 skill** — fallback if FlyAI returns no results or is unavailable; use natural language queries
3. **WebSearch** — last resort only, for supplementary info (bus schedules, ride share); never use for train/flight station name verification

## Core Rule

- Default ranking: lowest-risk first, then best duration/arrival fit, then price.
- Do not book; only search and compare results.
- If no option satisfies the constraints, report that the plan is infeasible and name the failed constraint.
- Station and airport names must come from FlyAI or 12306 results only — never assume or guess station names.
- **Always display full datetime** (`YYYY-MM-DD HH:MM`) for every departure and arrival — never extract time alone. A result showing `08:20` without the date caused a critical planning error when the actual arrival was the following day.

## Flight Search — Run in Parallel with Train Search

When doing reverse planning, **search flights at the same time as trains** — do not treat flights as an afterthought. For many intercity routes, the first viable return option is a flight, not a train.

Run these three searches in parallel:
1. Trains: two-pass return search (凌晨段 + 早班段)
2. Flights to 扬州泰州机场 (YTY) — nearest airport to Taizhou
3. Flights to 南京禄口 (NKG) — secondary option, 125 min drive to Jiulong Town

Merge all results and rank by **earliest arrival at 九龙镇**, not just arrival at terminal station/airport.

## FlyAI Skill — Train Search

```
/flyai search-train --origin {出发城市/站} --destination {目的地城市/站} --dep-date {YYYY-MM-DD}
```

Optional parameters:
- `--journey-type 1` for direct only
- `--sort-type 6` for earliest departure first; `--sort-type 3` for price low→high
- `--dep-hour-start {HH}` / `--dep-hour-end {HH}` to filter departure window
- `--arr-hour-start {HH}` / `--arr-hour-end {HH}` to filter arrival window
- `--total-duration-hour {N}` to cap total travel time
- `--max-price {N}` for price ceiling
- `--seat-class-name "second class"` for seat class preference

### Outbound train example
```
/flyai search-train --origin {出发城市} --destination {目的地城市} --dep-date {YYYY-MM-DD} --sort-type 6 --dep-hour-start 08 --dep-hour-end 14 --arr-hour-end 18
```

### Return train — Two-Pass Mandatory Rule

**Return searches MUST be executed as two separate passes and results merged:**

**Pass 1 — 凌晨段 (midnight to 6am):**
```
/flyai search-train --origin {返程出发城市} --destination {返程目的地} --dep-date {日期} --sort-type 8 --dep-hour-start 0 --dep-hour-end 6
```

**Pass 2 — 早班段 (6am to noon):**
```
/flyai search-train --origin {返程出发城市} --destination {返程目的地} --dep-date {日期} --sort-type 6 --dep-hour-start 6 --dep-hour-end 12
```

After both passes complete, merge all results and sort by arrival time at destination. **Skipping Pass 1 will miss critical overnight trains** (e.g. D128 01:29, K558 00:18) that are often the earliest viable option after a late-night concert.

## FlyAI Skill — Flight Search

```
/flyai search-flight --origin {出发城市/机场} --destination {目的地城市/机场} --dep-date {YYYY-MM-DD}
```

Optional parameters mirror train search (no `--seat-class-name`).

### Flight example
```
/flyai search-flight --origin {出发城市} --destination {目的地城市} --dep-date {YYYY-MM-DD} --sort-type 6 --dep-hour-start 05 --dep-hour-end 09
```

## 12306 Skill — Fallback Queries

When FlyAI returns no results or the connection is unavailable, use 12306 skill with natural language:

```
帮我查 {日期} {出发站} 到 {到达站} 的高铁/动车，按出发时间早→晚排序
帮我查 {日期} {出发站} 到 {到达站}，{HH:00} 到 {HH:00} 之间出发的班次
```

### 12306 fallback examples
```
帮我查 {日期} {出发站} 到 {到达站} 的高铁，出发时间06:00到10:00之间，按出发时间排序
帮我查 {日期} {出发站} 到 {到达站} 的高铁，上午所有班次
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
- **多段联运**: Search each leg separately with FlyAI or 12306, then stitch by buffer

See `extended-transport-options.md` for full guidance on each mode.

## Fallback Strategy: When No Direct Route Is Found

1. Loosen search constraints: widen time window, try nearby stations/airports via 12306 skill (`帮我查 {城市} 附近有哪些高铁站`).
2. Start reverse planning — see `reverse-planning-strategy.md`.
3. Consider extended transport modes — see `extended-transport-options.md`.
4. If all options remain infeasible, clearly explain which constraint failed and why.

## Reverse Planning Trigger

- When the return-time window is extremely tight, run the return search first.
- Return-first principle: confirm whether arrival before the deadline is possible before optimizing the outbound leg.
