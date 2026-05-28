# Trip Output Template

Use this exact markdown structure for the final concert itinerary.
This template is a reusable markdown placeholder format with one example block and one no-viable-plan variant.

## Scope note
- Default content only: concert info, transport, venue routing, buffers, feasibility, and risk.
- Do not add restaurants, sightseeing, entertainment, shopping, or hotel sections unless the user explicitly asks for them.

## Template

### 1. Header
**Concert:** {{concert_name}}  
**Artist:** {{artist_name}}  
**Date:** {{concert_date}}  
**Venue:** {{venue_name}}  
**Venue address:** {{venue_address}}  
**Departure city:** {{departure_city}}  
**Return destination:** {{return_destination}}  
**Planning goal:** {{planning_goal}}  
**Risk level:** {{risk_level}} (LOW / MEDIUM / HIGH)

### 2. Sources
**Search timestamp:** {{search_timestamp_iso}}  
**Concert sources:**
- {{concert_source_1_title}} — {{concert_source_1_url}}
- {{concert_source_2_title}} — {{concert_source_2_url}}
**Transport sources:**
- {{transport_source_1_title}} — {{transport_source_1_url}}
- {{transport_source_2_title}} — {{transport_source_2_url}}
**Local route sources:**
- {{local_route_source_1_title}} — {{local_route_source_1_url}}

### 3. Concert verification
- **Official start time:** {{official_start_time}}
- **Estimated end time:** {{estimated_end_time}}
- **Verification note:** {{verification_note}}

### 4. Minute-by-minute timeline

| Time | Action | Location / transport | Buffer used | Source |
|---|---|---|---|---|
| {{timeline_time_1}} | {{timeline_action_1}} | {{timeline_location_1}} | {{timeline_buffer_1}} | {{timeline_source_1}} |
| {{timeline_time_2}} | {{timeline_action_2}} | {{timeline_location_2}} | {{timeline_buffer_2}} | {{timeline_source_2}} |
| {{timeline_time_3}} | {{timeline_action_3}} | {{timeline_location_3}} | {{timeline_buffer_3}} | {{timeline_source_3}} |

### 5. Outbound transport
- **Chosen option:** {{outbound_option}}
- **Route:** {{outbound_route}}
- **Departure:** {{outbound_departure_time}}
- **Arrival:** {{outbound_arrival_time}}
- **Why this option:** {{outbound_reason}}
- **Constraints checked:** {{outbound_constraints_checked}}

### 6. Local route to venue
- **Arrival point:** {{arrival_point}}
- **Venue route:** {{route_to_venue}}
- **Travel mode:** {{route_to_venue_mode}}
- **Estimated duration:** {{route_to_venue_duration}}
- **Buffer check:** {{route_to_venue_buffer_check}}

### 7. Local route after concert
- **Exit time:** {{post_concert_exit_time}}
- **Return point route:** {{route_after_concert}}
- **Travel mode:** {{route_after_concert_mode}}
- **Estimated duration:** {{route_after_concert_duration}}
- **Buffer check:** {{route_after_concert_buffer_check}}

### 8. Return transport
- **Chosen option:** {{return_option}}
- **Route:** {{return_route}}
- **Departure:** {{return_departure_time}}
- **Arrival:** {{return_arrival_time}}
- **Why this option:** {{return_reason}}
- **Constraints checked:** {{return_constraints_checked}}

### 9. Buffer summary
- **Venue buffer:** {{venue_buffer_summary}}
- **Airport buffer:** {{airport_buffer_summary}}
- **Train station buffer:** {{train_station_buffer_summary}}
- **Local route buffer:** {{local_route_buffer_summary}}

### 10. Risk assessment
- **Risk level:** {{risk_level}} (LOW / MEDIUM / HIGH)
- **Main reasons:** {{risk_reasons}}
- **Failure points:** {{failure_points}}
- **Recommended action:** {{recommended_action}}

### 11. Final note
{{final_note}}

## Example output

### 1. Header
**Concert:** Sample City Night Live  
**Artist:** Sample Artist  
**Date:** 2026-06-15  
**Venue:** Sample Arena  
**Venue address:** Sample District, Sample City  
**Departure city:** Sample Departure City  
**Return destination:** Sample Departure City  
**Planning goal:** Lowest-risk same-day round trip  
**Risk level:** MEDIUM

### 2. Sources
**Search timestamp:** 2026-05-29T09:30:00+08:00  
**Concert sources:**
- Official venue page — https://example.com/venue
- Artist social post — https://example.com/artist-post
**Transport sources:**
- Sample rail search — https://example.com/rail
- Sample flight search — https://example.com/flight
**Local route sources:**
- Sample map route — https://example.com/map-route

### 3. Concert verification
- **Official start time:** 19:30
- **Estimated end time:** 22:00
- **Verification note:** Start time confirmed by venue page; end time estimated from the published runtime window.

### 4. Minute-by-minute timeline

| Time | Action | Location / transport | Buffer used | Source |
|---|---|---|---|---|
| 14:00 | Depart origin station | Outbound train | — | Sample rail search |
| 16:40 | Arrive at destination station | Station arrival | 45 min station buffer reserved | Sample rail search |
| 17:10 | Arrive near venue | Local transit from station | 20 min local buffer reserved | Sample map route |
| 18:30 | Enter venue area | Venue entry / security | 60 min venue buffer reserved | Official venue page |
| 19:30 | Concert starts | Venue | — | Official venue page |
| 22:00 | Concert ends (estimated) | Venue exit | — | Official venue page |
| 22:20 | Reach return station | Local transit after concert | 20 min local buffer reserved | Sample map route |
| 23:00 | Return departure | Outbound station | 45 min station buffer reserved | Sample rail search |
| 01:40 | Arrive home city | Return transport complete | — | Sample rail search |

### 5. Outbound transport
- **Chosen option:** Same-day train
- **Route:** Sample Departure City Station → Sample City Station
- **Departure:** 14:00
- **Arrival:** 16:40
- **Why this option:** Lowest-risk option with enough station and venue buffer.
- **Constraints checked:** Arrival before 18:00; station buffer preserved.

### 6. Local route to venue
- **Arrival point:** Sample City Station
- **Venue route:** Station exit → metro line X → venue gate
- **Travel mode:** Transit
- **Estimated duration:** 30 minutes
- **Buffer check:** Leaves 70 minutes before concert start.

### 7. Local route after concert
- **Exit time:** 22:20
- **Return point route:** Venue gate → transit stop → Sample City Station
- **Travel mode:** Transit
- **Estimated duration:** 40 minutes
- **Buffer check:** Arrives with 40 minutes before return departure.

### 8. Return transport
- **Chosen option:** Late-night train
- **Route:** Sample City Station → Sample Departure City Station
- **Departure:** 23:00
- **Arrival:** 01:40
- **Why this option:** Keeps same-day return and avoids overnight hotel need.
- **Constraints checked:** Meets return-time preference and preserves local transfer buffer.

### 9. Buffer summary
- **Venue buffer:** 60 minutes reserved before entry
- **Airport buffer:** N/A because this sample uses rail only
- **Train station buffer:** 45 minutes reserved before departures
- **Local route buffer:** 20 minutes reserved for each local transfer

### 10. Risk assessment
- **Risk level:** MEDIUM
- **Main reasons:** Tight but feasible station-to-venue transfer; evening return depends on on-time local transit.
- **Failure points:** If the inbound train is delayed by more than 20 minutes, the venue buffer shrinks too much.
- **Recommended action:** Keep the same plan only if live transport results remain on schedule.

### 11. Final note
This itinerary is based on current search results and is not guaranteed.

## No viable plan variant

### 1. Header
**Concert:** {{concert_name}}  
**Artist:** {{artist_name}}  
**Date:** {{concert_date}}  
**Venue:** {{venue_name}}  
**Departure city:** {{departure_city}}  
**Return destination:** {{return_destination}}  
**Risk level:** HIGH

### 2. Sources
**Search timestamp:** {{search_timestamp_iso}}  
**Concert sources:** {{concert_source_list}}  
**Transport sources:** {{transport_source_list}}  
**Local route sources:** {{local_route_source_list}}

### 3. No viable plan
- **Status:** No viable plan found
- **Why:** {{why_no_plan}}
- **Constraint that fails:** {{failed_constraint}}
- **Closest feasible option:** {{closest_feasible_option}}
- **Recommended next step:** {{recommended_next_step}}

### 4. Risk assessment
- **Risk level:** HIGH
- **Main reasons:** {{risk_reasons}}
- **Failure points:** {{failure_points}}
- **Recommended action:** Ask the user to relax one or more constraints.
