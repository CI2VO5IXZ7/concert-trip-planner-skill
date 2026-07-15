# Feasibility Pre-Check Examples

Real-world examples from concert trip planning sessions to calibrate the pre-check.

## Example 1: 泰州→北京鸟巢 (NO VIABLE)

**Scenario:**
- Departure: 江苏泰州
- Concert: 汪苏泷「明日世界」, 北京鸟巢, 2026-08-23 18:30-22:00 (3.5h)
- Deadline: 2026-08-24 08:30 到岗泰州

**Pre-check calculation:**
- 泰州→北京 高铁约 4-5h（直达）或飞机 2h+机场
- 北京→泰州: 高德驾车 1005km / 10h20min, 高铁直达 4-5h
- 演唱会结束: 22:00
- 次日到岗: 08:30 → 可用返程时间仅 ~10.5h

**Verdict: 低可行性**

**Search results:**
| 方案 | 出发 | 到达泰州 | 可行 |
|---|---|---|---|
| Z29 夜车 | 21:40（演唱会未结束）| 次日 08:37 | ❌ 需提前离场 |
| K101→南京 | 23:20 | 次日 13:47 | ❌ |
| 深夜航班 | 无航班 | — | ❌ |
| 自驾 | 22:00 | 次日 08:20 | ⚠️ 10分钟余量，疲劳驾驶 |

**Conclusion: NO VIABLE PLAN** — 公共交通无一能在 22:00 后出发且次日 08:30 前到达。自驾理论上能到但风险极高（单人10小时夜间驾驶，10分钟余量）。

**User rejected:** 提前离场方案（Z29 21:40）。最终建议请半天假或接受迟到半天。

---

## Calibrated Thresholds (from real cases)

| 条件 | 判定 |
|---|---|
| 距离 > 800km + 次日早班硬约束（<10h窗口）| **低可行性**，直接告知 |
| 距离 400-800km + 次日早班 | **中可行性**，夜车/红眼航班可能可行 |
| 距离 < 400km + 次日早班 | **高可行性**，早班高铁即可 |
| 演唱会 > 3h + 返程无直达夜车 | 返程几乎必然需要过夜方案 |
| 用户不接受提前离场 | 必须搜索结束后所有交通方式 + 自驾耗时 |
