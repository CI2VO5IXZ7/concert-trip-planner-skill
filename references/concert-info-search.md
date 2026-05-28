# Concert Info Search Reference

## Purpose
Use this guide to find and verify concert venue, address, date, start time, and estimated end time from current online sources.

## Search Strategy
1. Search with **artist/concert name + city + date** first.
2. If the result set is broad, add one more discriminator such as venue name, tour name, or nearby landmark.
3. Search in both English and Chinese when the concert may be listed in either language.
4. Cross-check the same concert across at least two independent sources before treating a time or address as confirmed.

Example query patterns:
- `artist name + city + date`
- `concert name + city + date`
- `artist name + venue + date`
- `artist name + city + ticketing platform`

## Reliable Source Hierarchy
Prefer sources in this order:
1. Official venue website / official venue event page
2. Official organizer / promoter / artist announcement
3. Major ticketing platform event page
4. Venue social media or artist social media that directly states the event details
5. Other reputable event listings only as backup

Never treat unofficial reposts, scalper listings, or discussion posts as authoritative.

## Citation Requirement
Every extracted concert detail must include a source citation with:
- source name
- source URL
- search timestamp

Suggested format:
- `Source: Official Venue Page — https://example.com/event (searched 2026-05-29 12:34 UTC)`

## Required Extraction Fields
Capture the following fields for each matched concert:
- Artist
- Venue name
- Venue address
- Date
- Start time
- Estimated end time
- Source URL
- Search timestamp
- Confidence

## Handling Ambiguous or Conflicting Results
### Multiple venues
If the concert appears at more than one venue, compare official sources first and keep the venue that matches the most authoritative source. If uncertainty remains, disclose it and ask the user.

### Conflicting times
If sources disagree on the start time, prefer the official venue or organizer page. If still conflicting, note the conflict explicitly and do not present the time as confirmed.

### Duplicate city names
If multiple cities share the same name, disambiguate with country, province/state, or venue context before concluding the match.

### Multiple matching concerts
If several concerts match the same artist/date/city query, separate them by venue and tour/event title, then ask the user which one to use when needed.

## End Time Policy
If the official end time is not published, prefer historical duration data first; if it cannot be obtained, estimate it and label it clearly as **estimated**.

- Default estimate: **prefer historical duration data; otherwise start time + 2.5 hours**
- Add buffer when using it for travel planning
- Never present an estimated end time as a confirmed fact

## No-Fabrication Rule
Never invent concert times, venue addresses, durations, or source details.
If the information cannot be verified with enough confidence, say so and ask the user for clarification or permission to proceed with a lower-confidence estimate.

## Confidence Guidance
- **High**: official venue/organizer page confirms venue, address, date, and start time
- **Medium**: only major ticketing or social confirmation is available, but details align across sources
- **Low**: conflicting or incomplete sources; disclose uncertainty and ask the user

## Minimal Workflow
1. Search by artist/concert name + city + date.
2. Identify the best matching event.
3. Verify venue name and address from the highest-ranked source available.
4. Capture start time from the same source or the next best authoritative source.
5. Estimate end time only if the official end time is missing, and label it as estimated.
6. Record the source URL, search timestamp, and confidence.

## Duration Verification

### Historical Duration Search Strategy
1. Search the specific topic's historical concert records first.
2. Use the search order: **topic-level historical shows → artist-level fallback**.
3. If this is a new topic with no reliable topic history, fall back to the artist's past concert durations and use the artist's historical average.
4. Only use a default estimate after historical data search fails.

### Search Query Templates
- `{艺人} {主题} 演唱会 时长`
- `{艺人} {主题} 演唱会 几点结束`
- `{艺人} 过往演唱会 平均时长`
- `{艺人} {主题} concert duration`
- `{艺人} {主题} concert end time`

### Source Requirements
- Every duration result must include a source citation in this format: `Source: {name} — {URL} (searched {timestamp})`
- Mark confidence as **High**, **Medium**, or **Low**.
- Distinguish source type explicitly: **official**, **fan repo**, or **media report**.
- Prefer official sources first, then media reports, then fan repos only when nothing better is available.

### Fallback to Default Estimate
If historical duration data cannot be found, use **start time + 2.5 hours** as the fallback estimate.
- Always label it as **estimate**.
- Do not present it as a confirmed duration.
- Use it only after topic-level and artist-level historical searches fail.
