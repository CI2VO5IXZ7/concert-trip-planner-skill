# Reverse Planning Strategy

## Purpose

This reference is for 特种兵行程的反向拼图规划. Use it when direct transport is unavailable, too late, or too fragile, especially when the user has a hard arrival deadline after a concert.

Core idea: do not start from the concert city only. Start from the required destination and deadline, work backward to find feasible inbound directions, then stitch the route like a puzzle.

## Reverse Planning Workflow

1. 搜索 "{截止时间} 前到 {目的地} 的所有车次/航班". Lock the hard arrival deadline first.
2. 分析这些车次/航班的来源方向. Group by source corridor, not by single ticket only.
3. 判断哪些来源方向靠近演唱会城市. Prefer corridors that reduce the first escape leg after the show.
4. 对靠近的来源方向，搜索 "演唱会城市 → 中转城市" 的交通. Include train, flight, overnight bus, ride share, and other allowed modes from `extended-transport-options.md`.
5. 拼接完整行程，检查中转缓冲. Use 特种兵 standard 30-60 minutes for tactical transfers, while keeping fixed safety minimums visible: venue 60min, airport 90min, train 45min, local 20min.

Only output a plan when every leg has a realistic connection. If reverse planning also fails, then use **REJECT / NO VIABLE PLAN** instead of forcing a route.

## Transfer Hub Selection Rules

- 距离优先: 中转城市距离演唱会城市越近越好, because it reduces the first post-concert leg and lowers missed-connection risk.
- 时间缓冲: 特种兵标准最少 **30-60 minutes**. This is lower than the conventional 2-hour comfort buffer, so mark the risk clearly when the connection is tight.
- 过夜选项: If transfer time is **>6 hours**, consider airport / train station overnight waiting in public allowed areas only. Do not turn this into hotel or leisure planning.
- 交通枢纽优先: Prefer high-capacity hub cities such as 南京、徐州、郑州、武汉、上海、杭州 when they fit the direction and deadline.

## Return-First Principle

特种兵行程通常返程更难: concert end time is uncertain, late-night local transit may be weak, and hard next-day deadlines leave less room for recovery. Therefore, confirm the return side before spending time optimizing the outbound side.

Workflow adjustment:

1. Step 1 确认返程: Can the user leave the concert city and reach the required destination before the deadline?
2. Step 2 规划去程: Only after return is viable, search arrival-to-concert-city options.
3. Step 3 规划现场: Add venue arrival, post-show escape, and local transfer buffers.

If return is not viable, tell the user early. This avoids wasting planning time on a good outbound route that cannot be completed safely.

## Example Case Study

Scenario: 太原 → 泰州, must arrive before next-day 8:00 after a concert. This is a reverse-planning example only; do not invent specific train numbers, flight numbers, prices, or real-time availability.

1. 步骤1: 搜索 8:00 前到泰州的车次 / 航班 / feasible transport arrivals. Focus on all routes that can reach 泰州 before the deadline.
2. 步骤2: 发现这些 arrivals may mainly come from 南京 / 徐州 / 上海方向. Treat these as source corridors, not guaranteed tickets.
3. 步骤3: 搜索 太原 → 南京 / 徐州 的高铁、飞机、夜间交通或组合交通. Also check whether 上海方向 is still realistic after post-concert departure time.
4. 步骤4: 评估中转可行性. For 南京 / 徐州, check whether station or airport overnight waiting is allowed, whether the first morning connection reaches 泰州 before 8:00, and whether the train / airport / local buffers are met.
5. 步骤5: 给出多段联运方案或明确不可行. If the puzzle requires impossible timing, zero slack, or unavailable overnight waiting, output **REJECT / NO VIABLE PLAN** with the failed constraint.

## Multi-Leg Risk Escalation

- 1段直达 = **LOW** baseline, assuming all required buffers are satisfied.
- 2段联运 = at least **MEDIUM**, because one missed connection can break the route.
- 3段以上 = **HIGH**, even if each single leg looks possible.
- 含过夜中转 = extra **+1 risk level** because fatigue, station / airport access rules, and late-night uncertainty increase failure probability.
- If any fixed minimum buffer is violated, follow `risk-and-buffer-rules.md`: mark the plan **HIGH** or reject it when the route cannot work safely.

## Jigsaw Planning Mindset

- 特种兵精神: 不怕苦不怕累，直达不是唯一选择. The target is to complete the mission, not to make the route comfortable.
- 鼓励创造性组合: train + flight, flight + bus, high-speed rail + ride share, overnight bus + local transit, or other allowed modes from `extended-transport-options.md`.
- 时间换空间: 宁可多花时间在路上，也要达成目标, as long as safety, legality, and minimum buffers are not broken.
- Keep uncertainty visible. Creative does not mean fabricated; every leg still needs source-checking before final recommendation.
