# Final QA Evidence — Real Agent QA Test

Date: 2026-05-29
Task: F3. Real Agent QA Test — unspecified-high
Evidence mode: agent dry-run

## Environment check

Command used:

```bash
command -v openclaw || command -v claude || command -v claude-code
```

Result: no output. OpenClaw/Claude Code was not available in this environment, so this QA used the required documented agent dry-run path.

## Required inputs read

- `/home/momentg/Project/tezhongbing/SKILL.md`
- `/home/momentg/Project/tezhongbing/references/concert-info-search.md`
- `/home/momentg/Project/tezhongbing/references/flyai-transport-search.md`
- `/home/momentg/Project/tezhongbing/references/amap-local-route-planning.md`
- `/home/momentg/Project/tezhongbing/references/trip-output-template.md`
- `/home/momentg/Project/tezhongbing/references/risk-and-buffer-rules.md`
- `/home/momentg/Project/tezhongbing/.omo/notepads/concert-trip-planner/learnings.md`
- `/home/momentg/Project/tezhongbing/.omo/notepads/concert-trip-planner/issues.md`
- `/home/momentg/Project/tezhongbing/.omo/notepads/concert-trip-planner/problems.md`
- `/home/momentg/Project/tezhongbing/.omo/notepads/concert-trip-planner/decisions.md`

## Sample prompt under test

> I am in Shanghai and want to attend Jay Chou's concert in Beijing on 2026-07-18. I can leave after 08:00 and must return to Shanghai before noon the next day.

## Agent dry-run

### Parsed user constraints

- Departure city: Shanghai
- Concert target: Jay Chou concert in Beijing
- Concert date: 2026-07-18
- Earliest outbound departure: after 08:00 on 2026-07-18
- Return destination: Shanghai
- Return deadline: before noon on 2026-07-19
- Optimization goal: default lowest-risk first

### Required behavior with no real source data available in this QA run

The skill package requires current concert verification before itinerary planning:

- `SKILL.md` requires live concert info search and source verification before transport/local routing.
- `concert-info-search.md` requires source URL, timestamp, confidence, and at least authoritative verification of venue/address/date/start time.
- `concert-info-search.md` says not to invent concert times, venue addresses, durations, or source details, and to ask the user for clarification or permission to proceed with a lower-confidence estimate if information cannot be verified.
- `risk-and-buffer-rules.md` repeats that missing/uncertain information must remain visible and must not be fabricated.

Expected agent response for this dry-run state:

> I cannot produce a confirmed itinerary yet because I do not have verified current source data for Jay Chou's Beijing concert on 2026-07-18, including official venue, venue address, and start time. Please provide an official venue/organizer/ticketing source, or confirm that you want me to continue with a clearly labeled low-confidence estimate. I will not invent the venue, start time, transport schedule, or local route.

This satisfies the must-not-fabricate requirement and prevents silently proceeding with missing concert source data.

## Scenario checks

| ID | Check | Result | Evidence |
|---|---|---|---|
| S1 | Sample prompt can be processed without asking for already supplied user fields | PASS | Departure city, date, outbound window, return destination, and return deadline are present. |
| S2 | Missing live concert source data causes stop/clarifying ask instead of fabricated venue/start time | PASS | No-fabrication and low-confidence ask are explicitly required by `concert-info-search.md` and `risk-and-buffer-rules.md`. |
| S3 | If verified concert data exists, intended final output contains all required sections | PASS | `trip-output-template.md` includes Header, Sources, Concert verification, Minute-by-minute timeline, Outbound transport, Local route to venue, Local route after concert, Return transport, Buffer summary, Risk assessment, and Final note. |

Scenario result: 3/3 pass.

## Integration checks

| ID | Integration | Result | Evidence |
|---|---|---|---|
| I1 | Concert venue/start time must be sourced | PASS | `concert-info-search.md` requires current search, source URL, timestamp, and confidence. |
| I2 | Outbound options use FlyAI at guidance level | PASS | `flyai-transport-search.md` requires outbound major transport search first, with lowest-risk ranking and FlyAI examples. |
| I3 | Return options use FlyAI at guidance level | PASS | `flyai-transport-search.md` requires return search as a separate pass after end-time and post-show buffer checks. |
| I4 | Local routes use AMap at guidance level | PASS | `amap-local-route-planning.md` requires geocoding arrival point, venue, return point, and separate route planning to/from the venue. |
| I5 | Risk/buffer and infeasible handling are integrated | PASS | `risk-and-buffer-rules.md` defines fixed buffers, high-risk/no-viable-plan conditions, and no-fabrication guardrails. |

Integration result: 5/5 pass.

## Edge cases tested

| Edge case | Expected behavior | Result |
|---|---|---|
| Real concert source unavailable | Stop and ask for official source or permission for clearly labeled low-confidence estimate; do not fabricate venue/start time. | PASS |
| Multiple/conflicting concert matches | Prefer verified official sources; if uncertainty remains, disclose and ask which event/source to use. | PASS |
| Transport/local route infeasible after verified data | Use no-viable-plan handling; identify failed constraint and safe next step rather than forcing an itinerary. | PASS |

Edge cases tested: 3.

## Verdict

VERDICT: APPROVE

Rationale: The skill docs are sufficient for an agent to either produce the required itinerary sections after verified current source data is available, or to stop and ask the correct clarifying/source question when venue/start-time data cannot be verified. The package explicitly directs FlyAI for outbound/return transport, AMap for local routing, minute-by-minute timeline output, buffer/risk assessment, and no-fabrication handling for infeasible or uncertain cases.
