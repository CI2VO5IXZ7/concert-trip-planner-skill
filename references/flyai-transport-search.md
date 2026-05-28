# FlyAI Transport Search Reference

Use FlyAI for major transport only. Search outbound and return as separate passes, and always choose the lowest-risk option first.

## Core rule
- Default ranking: lowest-risk first, then best duration/arrival fit, then price.
- Do not book; only search and compare results.
- If no option satisfies the constraints, report that the plan is infeasible and name the failed constraint.

## Map user constraints to FlyAI parameters
- Origin city / station / airport -> `--origin`
- Destination city / station / airport -> `--destination`
- Travel date -> `--dep-date`
- Return date -> `--back-date`
- One-way search -> omit `--back-date`; use documented numeric `--journey-type` values only when the FlyAI README requires direct/connecting or transit filtering
- Sort preference -> documented numeric `--sort-type` values (for example, `3` for price low → high and `6` for depart early → late)
- Departure window -> `--dep-hour-start` / `--dep-hour-end`
- Arrival window -> `--arr-hour-start` / `--arr-hour-end`
- Maximum total trip time -> `--total-duration-hour`
- Maximum acceptable fare -> `--max-price`

For trains, also apply the plan’s train-specific filter when needed:
- Seat class preference -> `seat-class-name`

## Outbound search
Search the outbound leg first so the arrival window can be checked against the concert buffer.

### Flight example
```bash
flyai search-flight --origin 上海 --destination 北京 --dep-date 2026-06-20 --sort-type 3 --dep-hour-start 07 --dep-hour-end 14 --arr-hour-start 09 --arr-hour-end 18 --total-duration-hour 4 --max-price 2000
```

### Train example
```bash
flyai search-train --origin 上海 --destination 北京 --dep-date 2026-06-20 --journey-type 1 --sort-type 6 --dep-hour-start 06 --dep-hour-end 13 --arr-hour-start 08 --arr-hour-end 18 --total-duration-hour 8 --max-price 800 --seat-class-name second class
```

## Return search
Search the return leg as a separate pass after confirming the concert end time estimate and the post-show buffer.

### Flight example
```bash
flyai search-flight --origin 北京 --destination 上海 --dep-date 2026-06-21 --journey-type 1 --sort-type 6 --dep-hour-start 22 --dep-hour-end 24 --arr-hour-start 23 --arr-hour-end 24 --total-duration-hour 4 --max-price 2000
```

### Train example
```bash
flyai search-train --origin 北京 --destination 上海 --dep-date 2026-06-21 --journey-type 1 --sort-type 3 --dep-hour-start 21 --dep-hour-end 24 --arr-hour-start 23 --arr-hour-end 24 --total-duration-hour 8 --max-price 800 --seat-class-name second class
```

## Ranking logic
1. Lowest-risk option first: the itinerary that best satisfies all buffers and windows.
2. Then duration and arrival fit: prefer the option that lands closest to the needed arrival window without violating it.
3. Then price: only use price to break ties after risk and timing.

## Buffer coordination
- Venue buffer: arrive at the venue at least 60 minutes before show start.
- Airport buffer: arrive at the airport at least 90 minutes before departure.
- Train buffer: arrive at the station at least 45 minutes before departure.
- Local route buffer: keep 20 minutes for the last-mile transfer.

Coordinate the transport search with the venue plan:
- Outbound arrival must leave time for local transit plus the venue buffer.
- Return departure must leave time for local egress plus the station/airport buffer.
- If the concert end time is uncertain, use the estimate plus the venue buffer before choosing a return option.

## No-viable-plan behavior
If nothing matches the constraints:
- Say the trip is infeasible for the requested windows.
- Identify the failing constraint, such as no arrival before the venue buffer, no return after the concert buffer, or no result within the price/duration cap.
- Try reverse planning and extended transport modes.
- Ask for a wider time window or a relaxed constraint before searching again.

## Conditional hotel note
- `search-hotel` is only relevant if the user explicitly asks for overnight stay.

## Extended Transport Modes
- FlyAI native base tools: `search-flight` and `search-train`.
- FlyAI native overnight support: `search-hotel` only for airport/station nearby overnight stays.
- Other transport modes are not supported by FlyAI and require agent web search.
- 顺风车: web search `{起点} 到 {终点} 顺风车`
- 大巴 / 夜巴: web search `{起点} 汽车站 {终点} 班次`
- 自驾: use AMap driving route planning
- 机场过夜 / 车站过夜: use FlyAI `search-hotel` only for overnight scenarios near airports/stations
- 多段联运: search each leg separately, then stitch by buffer

## Fallback Strategy: When FlyAI Finds No Direct Route
1. Loosen search constraints first: widen the time window, raise the price ceiling, and try nearby stations/airports.
2. If there is still no result, start reverse planning; see `references/reverse-planning-strategy.md`.
3. Then consider extended transport modes; see `references/extended-transport-options.md`.
4. If all options remain infeasible, clearly explain which constraint failed and why.

## Reverse Planning Trigger
- When the user's return-time window is extremely tight, prioritize the return search first.
- Return-first principle: confirm whether arrival before the deadline is possible before planning the outbound leg.
