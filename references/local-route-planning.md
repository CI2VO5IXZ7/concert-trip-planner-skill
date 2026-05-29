# Local Route Planning Reference

## Purpose

Use the **AMap Web Service REST API** (via curl) for all local logistics routing: address geocoding, driving/transit route planning, and last-mile distance estimation. Do not substitute WebSearch for any routing or distance data.

## API Key Requirement

Requires an **AMap Web Service Key** (Web服务类型).
- Apply at: https://console.amap.com/dev/key/app → 添加Key → 服务平台选「Web服务」
- If the user has not provided a key, ask for it before proceeding.
- The JSAPI Key (Web端JS API类型) will return error `10009 USERKEY_PLAT_NOMATCH` — do not use it.

## Scope

- Allowed: venue, airport, and train-station geocoding.
- Allowed: route planning for transit, driving/taxi, and short walking legs.
- Allowed: POI lookup only to confirm venue, station, or airport identity.
- Not allowed: restaurants, entertainment, sightseeing, shopping, or any other POI.

## Workflow

1. Geocode the arrival point (airport or train station).
2. Geocode the venue address.
3. Plan the inbound local route: arrival point → venue (transit or driving).
4. Plan the outbound local route: venue → return departure point (driving/taxi after late-night concerts).
5. Add the 20-minute local buffer to each leg before finalizing.

---

## API Reference

### 1. Geocoding — Address to Coordinates

**Endpoint:** `GET https://restapi.amap.com/v3/geocode/geo`

**Parameters:**
- `address` — full Chinese address or POI name
- `city` — city name to narrow results
- `key` — AMap Web Service Key

**Curl template:**
```bash
curl -s "https://restapi.amap.com/v3/geocode/geo?address={地址}&city={城市}&key={AMAP_KEY}"
```

**Extract location:**
```bash
curl -s "https://restapi.amap.com/v3/geocode/geo?address=郑州奥林匹克体育中心&city=郑州&key={AMAP_KEY}" \
  | python3 -c "import json,sys; g=json.load(sys.stdin)['geocodes'][0]; print(g['formatted_address'], g['location'])"
```

**Response fields to capture:** `formatted_address`, `location` (lng,lat), `adcode`

---

### 2. Driving/Taxi Route

**Endpoint:** `GET https://restapi.amap.com/v3/direction/driving`

**Parameters:**
- `origin` — departure coordinates `lng,lat`
- `destination` — destination coordinates `lng,lat`
- `key`

**Curl template:**
```bash
curl -s "https://restapi.amap.com/v3/direction/driving?origin={lng,lat}&destination={lng,lat}&key={AMAP_KEY}"
```

**Extract duration and distance:**
```bash
curl -s "https://restapi.amap.com/v3/direction/driving?origin=113.537479,34.743276&destination=113.766353,34.748107&key={AMAP_KEY}" \
  | python3 -c "
import json,sys
r=json.load(sys.stdin)['route']['paths'][0]
print(f\"{int(r['duration'])//60}分钟，{int(r['distance'])/1000:.1f}km\")
"
```

---

### 3. Transit Route (Public Transport)

**Endpoint:** `GET https://restapi.amap.com/v3/direction/transit/integrated`

**Parameters:**
- `origin` — departure coordinates
- `destination` — destination coordinates
- `city` — city name (required for transit)
- `nightflag` — `0` for daytime, `1` for night service check
- `key`

**Curl template:**
```bash
curl -s "https://restapi.amap.com/v3/direction/transit/integrated?origin={lng,lat}&destination={lng,lat}&city={城市}&nightflag=0&key={AMAP_KEY}"
```

**Extract top-3 transit options:**
```bash
curl -s "https://restapi.amap.com/v3/direction/transit/integrated?origin=113.766353,34.748107&destination=113.537479,34.743276&city=郑州&nightflag=0&key={AMAP_KEY}" \
  | python3 -c "
import json,sys
transits=json.load(sys.stdin)['route']['transits']
for i,t in enumerate(transits[:3]):
    dur=int(t['duration'])
    segs=[]
    for s in t['segments']:
        if 'bus' in s:
            for line in s['bus']['buslines']:
                segs.append(line['name'].split('(')[0])
        elif 'walking' in s and int(s['walking'].get('distance',0))>100:
            segs.append(f'步行{int(s[\"walking\"][\"distance\"])}m')
    print(f'方案{i+1}: {dur//60}分钟 | {\" → \".join(segs)}')
"
```

---

## Route Mode Selection

- **Transit**: preferred for daytime / early-evening legs when metro/bus is running.
- **Driving/taxi**: required for late-night returns (after transit last service ~23:00), tight departure windows, or when missing last transit would break the chain.
- **Walking**: only for legs ≤15 minutes as a feeder between geocoded point and transit stop.
- Check transit availability for post-concert legs — metro often ends at 23:00–23:30.

## Buffer Rule

- Add a fixed **20-minute local route buffer** on top of every AMap duration result.
- Apply to both the inbound leg (to venue) and outbound leg (to station/airport).
- If the buffered total causes the schedule to fail, treat the plan as HIGH risk or infeasible.

## Late-Night Fallback

- Run a transit query with `nightflag=1` to check whether service is still running after concert end time.
- If transit is unavailable, switch to driving route.
- Do not promise real-time traffic or guaranteed ride availability.

## Output Expectation

For each local leg, record:
- Origin and destination (AMap-verified `formatted_address`)
- Chosen mode
- AMap raw duration (seconds → minutes)
- Distance (meters → km)
- +20 min buffer applied
- Buffered total
- Risk note if timing is tight
