# Task 11 Evidence: Reverse Planning Strategy

## Created File

- `/home/momentg/Project/tezhongbing/references/reverse-planning-strategy.md`

## Content Coverage

- PASS: includes `## Purpose` for 特种兵 reverse planning when direct routes are unavailable or fragile.
- PASS: includes `## Reverse Planning Workflow` with 5 reverse-search steps.
- PASS: includes `## Transfer Hub Selection Rules` covering distance priority, 30-60 minute tactical transfer buffer, >6h overnight option, and high-speed hub preference.
- PASS: includes `## Return-First Principle` with workflow adjustment: Step 1 确认返程 → Step 2 规划去程 → Step 3 规划现场.
- PASS: includes `## Example Case Study` for 太原 → 泰州 before next-day 8:00, using generic corridors only and no fabricated train / flight numbers.
- PASS: includes `## Multi-Leg Risk Escalation` aligned with LOW / MEDIUM / HIGH risk rules.
- PASS: includes `## Jigsaw Planning Mindset` for creative special-forces route stitching.

## Verification

Command run from `/home/momentg/Project/tezhongbing`:

```bash
python3 - <<'PY'
from pathlib import Path
path = Path('/home/momentg/Project/tezhongbing/references/reverse-planning-strategy.md')
text = path.read_text(encoding='utf-8')
checks = [
    ('file exists', path.exists()),
    ('Purpose heading', '## Purpose' in text),
    ('Reverse Planning Workflow heading', '## Reverse Planning Workflow' in text),
    ('Transfer Hub Selection Rules heading', '## Transfer Hub Selection Rules' in text),
    ('Return-First Principle heading', '## Return-First Principle' in text),
    ('Example Case Study heading', '## Example Case Study' in text),
    ('Multi-Leg Risk Escalation heading', '## Multi-Leg Risk Escalation' in text),
    ('Jigsaw Planning Mindset heading', '## Jigsaw Planning Mindset' in text),
    ('5-step workflow has step 1', '1. 搜索 "{截止时间} 前到 {目的地} 的所有车次/航班"' in text),
    ('5-step workflow has step 5', '5. 拼接完整行程，检查中转缓冲' in text),
    ('distance priority rule', '距离优先' in text),
    ('time buffer rule', '30-60 minutes' in text),
    ('overnight option rule', '过夜选项' in text and '>6 hours' in text),
    ('transport hub priority rule', '交通枢纽优先' in text),
    ('return-first workflow adjustment', 'Step 1 确认返程' in text and 'Step 2 规划去程' in text and 'Step 3 规划现场' in text),
    ('Taiyuan-Taizhou example', '太原 → 泰州' in text and '8:00' in text),
    ('no invented concrete trips warning', 'do not invent specific train numbers, flight numbers, prices, or real-time availability' in text),
    ('risk escalation 2 legs medium', '2段联运 = at least **MEDIUM**' in text),
    ('risk escalation 3 legs high', '3段以上 = **HIGH**' in text),
    ('overnight risk +1', '含过夜中转 = extra **+1 risk level**' in text),
]
failed = [name for name, ok in checks if not ok]
for name, ok in checks:
    print(f'{"PASS" if ok else "FAIL"}: {name}')
if failed:
    raise SystemExit('Failed checks: ' + ', '.join(failed))
print('All reverse planning strategy checks passed.')
PY
```

Result:

```text
PASS: file exists
PASS: Purpose heading
PASS: Reverse Planning Workflow heading
PASS: Transfer Hub Selection Rules heading
PASS: Return-First Principle heading
PASS: Example Case Study heading
PASS: Multi-Leg Risk Escalation heading
PASS: Jigsaw Planning Mindset heading
PASS: 5-step workflow has step 1
PASS: 5-step workflow has step 5
PASS: distance priority rule
PASS: time buffer rule
PASS: overnight option rule
PASS: transport hub priority rule
PASS: return-first workflow adjustment
PASS: Taiyuan-Taizhou example
PASS: no invented concrete trips warning
PASS: risk escalation 2 legs medium
PASS: risk escalation 3 legs high
PASS: overnight risk +1
All reverse planning strategy checks passed.
```

## Diagnostics

- Markdown LSP diagnostics could not run because no `.md` LSP server is configured in this workspace.
- Available configured servers reported: typescript, deno, vue, eslint, oxlint, biome, gopls, ruby-lsp, basedpyright, pyright.
