# AMap Local Route Planning Reference

## Purpose
Use AMap Skills only for local logistics routing around the concert trip: resolve addresses, choose a route mode, estimate travel time, and plan the last-mile trip to and from the venue.

## Scope
- Allowed: venue, airport, and train-station geocoding.
- Allowed: route planning for transit, driving, taxi, and short walking transfer legs if needed.
- Allowed: POI lookup only to disambiguate a venue, station, or airport name/address.
- Not allowed: restaurants, entertainment, sightseeing, shopping, or any other POI recommendations.

## Workflow
1. Geocode the arrival point first: airport or train station.
2. Geocode the venue address and, if needed, the return departure point.
3. Compare the arrival point to the venue and plan the local route to the venue.
4. After the concert, plan the route from the venue back to the departure airport or train station.
5. Add the local route buffer on top of the AMap duration before finalizing the itinerary.

## Geocoding guidance
- Use address-to-coordinate lookup for venue, airport, and train-station addresses.
- If the name is ambiguous, use POI lookup only to confirm which venue/station/airport is correct.
- Do not expand POI search beyond logistics disambiguation.

## Route planning guidance
- Prefer transit when service is available and the time window is comfortable.
- Prefer driving or taxi when the concert ends late, when public transit may be closed, or when the transit transfer risk is too high.
- Use walking only for short transfer legs between the geocoded point and the main route start/end.
- Evaluate both the outbound route and the return route separately.

## Mode selection
- Transit is best for daytime or early-evening legs with clear service availability.
- Driving/taxi is best for late-night returns, tight departure windows, or when missing the last transit connection would cause a miss.
- If the route is close but the buffer is tight, mark the plan as riskier instead of assuming it will work.

## Buffer rule
- Add a fixed 20-minute local route buffer on top of the AMap duration.
- Apply that buffer to both the trip to the venue and the trip back to the station/airport.
- If the buffered route does not fit the schedule, treat the plan as high risk or infeasible.

## Late-night fallback
- If public transit is unavailable after the concert, switch to taxi/driving first.
- If taxi/driving still leaves too little time before the next deadline, flag the route as tight risk.
- Do not promise real-time traffic or guaranteed ride availability.

## Output expectation
For each local leg, record:
- origin and destination
- chosen mode
- unbuffered AMap duration
- +20 minute local buffer
- risk note if the timing is tight
