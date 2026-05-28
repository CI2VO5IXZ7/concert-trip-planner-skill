# OpenClaw Concert Special-Forces Trip Planner

## Skill Name
Concert Special-Forces Trip Planner

## Description
Plan tight concert round trips with live concert verification, lowest-risk-first transport choices, local venue routing, and a minute-by-minute itinerary.

## Activation Triggers
Activate when the user mentions any of: `concert`, `演唱会`, `特种兵`.

## What This Skill Does
This is the main OpenClaw skill entry point for concert trip planning. It guides the agent to:
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
2. Search current concert information, verify venue/date/timing, and verify historical concert duration.
3. Plan outbound major transport with the lowest-risk option first. If no direct route is feasible, or the return-side deadline is too tight/fragile, trigger reverse planning.
4. Plan local route from arrival point to venue.
5. Plan local route from venue to the return departure point.
6. Plan return major transport, including extended transport modes when needed.
7. Produce a concise itinerary with risk assessment and buffer checks.

## Default Optimization Goal
Default to **lowest risk first**, not cheapest or fastest. (特种兵精神: 不怕苦不怕累，直达不是唯一选择，时间优先于舒适)

## Fixed Buffers
- Venue: 60 minutes
- Airport: 90 minutes
- Train station: 45 minutes
- Local route: 20 minutes
- Transfer: 30-60 minutes (特种兵标准，低于常规)

## Must Have
- Live concert info search with source verification
- Round-trip transport planning
- Local venue routing
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
- [concert-info-search.md](references/concert-info-search.md)
- [flyai-transport-search.md](references/flyai-transport-search.md)
- [amap-local-route-planning.md](references/amap-local-route-planning.md)
- [trip-output-template.md](references/trip-output-template.md)
- [risk-and-buffer-rules.md](references/risk-and-buffer-rules.md)
- [extended-transport-options.md](references/extended-transport-options.md)
- [reverse-planning-strategy.md](references/reverse-planning-strategy.md)
