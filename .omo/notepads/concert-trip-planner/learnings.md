
## 2026-05-29
- The main skill file should stay as a behavior guide only: triggers, workflow, guardrails, fallback handling, and relative links to references.
- Keep the planning bias on lowest risk first, and explicitly require clarification for missing date, missing return destination, ambiguous cities, and multiple matching concerts.
- The trip output template needs both a reusable placeholder version and a clearly labeled sample output, while still excluding food/fun/hotel content by default.
- The template should carry source citation fields, a search timestamp, buffer summaries for venue/airport/train station/local route, and a no-viable-plan variant.
- Task 3 reference should map user constraints directly to FlyAI flags, then rank results by lowest risk, arrival fit, and price.
- Treat outbound and return as separate searches so each leg can be checked against the venue and station/airport buffer rules.
- AMap local routing should stay logistics-only: geocode venue/station/airport addresses, plan transit or driving/taxi with short walking transfers only, add a fixed 20-minute local buffer, and fall back to taxi/driving when transit is closed late at night.
- POI usage for AMap should be limited to venue/station/airport disambiguation only; no food, entertainment, sightseeing, or shopping lookup belongs in the routing reference.
- The concert search reference should force artist/concert name + city + date queries, prefer official venue/organizer/ticketing sources, and always record source URL plus search timestamp.
- If end time is not published, the reference should require a clearly labeled estimate using start time + 2.5 hours, never a silent assumption.
- Task 6 should keep buffer rules exact and explicit: venue 60min, airport 90min, train station 45min, and local transit/route 20min.
- Uncertain concert end times should be handled as a 2.5h estimate plus the venue buffer, and no-viable-plan cases need a clear reject template.
- Task 7 cross-reference audit passed without source edits: all SKILL links resolve, buffer values stay aligned, FlyAI stays numeric-only for documented flags, AMap stays logistics-only, and disambiguation/no-fabrication guardrails remain in place.
