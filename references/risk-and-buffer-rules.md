# Risk and Buffer Rules

## Fixed Buffer Minimums

- Venue: **60 minutes**
- Airport: **90 minutes**
- Train station: **45 minutes**
- Local transit / route: **20 minutes**

These are safety minimums. Do not reduce them.

## Risk Rubric

### LOW
Use LOW only when all required buffers are satisfied comfortably and no major dependency is tight.

### MEDIUM
Use MEDIUM when one buffer is tight, or when one key detail is uncertain but a fallback still exists.

### HIGH
Use HIGH when multiple buffers are tight, the plan depends on perfect timing, any minimum buffer is violated, or the itinerary requires 3+ legs / overnight transit.

High-risk plans must be explicitly warned and never presented as guaranteed.

## Uncertain Concert End Time

If the official end time is not published, estimate the concert length as **2.5 hours** and then add the required venue buffer before planning the return side.

Do not state the estimate as a fact. Label it as an estimate.

## Last-Mile and Late-Night Fallbacks

- Check last-mile coverage after the concert and before committing to the return plan.
- If local transit is weak, late, or unavailable, treat the plan as higher risk.
- If the late-night fallback depends on perfect timing, mark the plan HIGH.
- If no safe or workable fallback exists, treat the plan as no viable plan.

## No-Viable-Plan Conditions

Treat the plan as **REJECT / NO VIABLE PLAN** after trying direct search, reverse planning, and extended transport modes when any of the following applies:

- Arrival is after the concert start time.
- Return transport is impossible within the required timing.
- No local route exists for the required transfer.
- The plan requires unsafe or illegal assumptions.

## Response Template for No-Viable-Plan

Use this structure:

> **REJECT / NO VIABLE PLAN**
> - Reason: <short factual reason>
> - Failed constraint: <which buffer / timing / route constraint fails>
> - **All options ranked by earliest arrival:**
>
> | 方案 | 出发 | 到达 | 最早到达时间 | 风险 |
> |---|---|---|---|---|
> | <option 1> | ... | ... | ... | ... |
> | <option 2> | ... | ... | ... | ... |
>
> - **Earliest viable arrival: XX:XX** via <方案简述> — 供参考，如可放宽截止时间可采用此方案
> - Safe next step: <what user must change to make a plan possible; try widening the return window or considering nearby-city transfers>

**Earliest viable arrival is mandatory.** After declaring no-viable-plan, always calculate and state the earliest time the user *could* arrive at the destination under any safe transport combination, even if it exceeds their deadline. This lets the user decide whether to relax the constraint rather than having to ask.

**All options must be listed.** Even when declaring NO VIABLE, present every possible方案 in a table ranked by earliest arrival time. Include self-drive with AMap-estimated duration. This gives the user full information to decide (e.g., accept fatigue risk, accept late arrival, or change constraints).

**User rejects a方案时** — 如果用户拒绝了某个方案（如提前离场），不要重复推荐。转而列出演唱会结束后出发的所有方案，按最早到达排序。

## No-Fabrication Guardrail

- Do not fabricate concert times, venue details, travel durations, or route availability.
- Do not guarantee real-world availability.
- If information is missing or uncertain, say so clearly and keep the uncertainty visible.

## Transfer Buffer Minimums

特种兵标准 **30-60 分钟**（低于常规2小时，但需考虑前车延误）。分级：

| 中转时间 | 处理 |
|---------|------|
| **< 15 分钟** | **硬拦截 — 直接剔除，不进候选列表**。低于车站/机场物理换乘所需最低时间，必然脱线。 |
| 15–30 分钟 | HIGH risk，仅在无其他方案时保留，且必须显式警告"几乎无容错" |
| 30–60 分钟 | MEDIUM risk |
| > 60 分钟 | 可接受，但仍需评估 |

**硬拦截规则：** 中转时间低于以下物理最低值的方案，**不得列为候选**，只能在"已排除方案"里说明原因：
- 同站换乘（如高铁站内换乘）：最低 **15 分钟**
- 跨站换乘（如火车站→机场、不同车站之间）：最低值 = AMap 实测两点间驾车/接驳时间 + 安检缓冲

测试中出现过中转仅 15 分钟（南京 C3858）的方案被列为候选——这类应直接剔除而非标红，避免给出实际无法完成的"方案"。

## Overnight Transit Risk

- 机场过夜：安全风险较低，但需注意财物安全和休息质量
- 车站过夜：安全风险较高，优先选择有24小时候车区的车站
- 标记：含过夜中转的行程，风险等级额外 +1
- 提醒：女性独行需谨慎评估夜间安全

## Multi-Leg Risk Escalation

- LOW：所有缓冲满足，直达或最多1段中转（缓冲充足）
- MEDIUM：一项紧张，或2段联运，或中转缓冲30-60分钟
- HIGH：多项紧张，或3段以上联运，或需要过夜中转，或中转缓冲<30分钟
- NO VIABLE：所有组合均不可行（经过反向规划和扩展方式尝试后）

## Reverse Planning Trigger

- 当满足以下任一条件时，自动启动反向规划（参考 `reverse-planning-strategy.md`）：
  - flyai 搜索不到直达车次/航班
  - 用户返程时间窗口极紧（< 演唱会结束时间 + 4小时）
  - 演唱会城市与目的地之间无直达高铁/航班
- 触发后：优先搜索返程，再规划去程

## Updated No-Viable-Plan Conditions

- 在现有条件基础上新增：
  - "经过反向规划和扩展交通方式尝试后，仍无可行方案"
- 更新 Response Template：在"Safe next step"中增加"尝试放宽返程时间窗口"和"考虑附近城市中转"
