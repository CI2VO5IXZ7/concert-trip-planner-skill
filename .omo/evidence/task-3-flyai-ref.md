# Task 3 Evidence

- Created `/home/momentg/Project/tezhongbing/references/flyai-transport-search.md`
- Includes `search-flight` and `search-train`
- Includes mapping for origin, destination, dep date, return date, time windows, and price/duration caps
- Includes lowest-risk-first ranking and buffer coordination
- Includes no-viable-plan behavior

Verification to run:
- grep checks from plan Task 3

Verification results:
- `grep -c 'search-flight\|search-train'` => 4
- `grep -c 'origin\|destination\|dep-date'` => 7
- `grep -c 'buffer\|round-trip\|往返'` => 11
- Correction applied: removed undocumented `one-way` / string sort examples; examples now use numeric `--sort-type` values and `second class` wording.
- Ban check passed: no `one-way`, `lowest-price`, `depart-earliest`, or `second-class` remains in the reference.
- Official doc alignment: examples now use numeric journey/sort values and omit string one-way/sort labels.
