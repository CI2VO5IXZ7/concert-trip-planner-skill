# 🎵 演唱会特种兵行程规划器 (Claude Code Skill)

一个专为特种兵式看演唱会设计的 Claude Code 技能，帮你规划最紧凑、最省心的往返行程。

## 什么是特种兵行程？

特种兵行程 = **不怕苦、不怕累、时间优先于舒适**。当天或次日极限往返，不追求吃喝玩乐，只为看一场演唱会。

## 核心能力

### 1. 演唱会信息智能搜索
- 自动搜索并验证演唱会场地、日期、开场时间
- **历史时长验证**：搜索同主题/同艺人过往演唱会时长，不瞎猜 2.5 小时
- 所有信息标注来源和信心度

### 2. 往返大交通规划
- 高铁/飞机/大巴/顺风车/自驾，多种方式联动
- **反向拼图规划**：当直达不可行时，从目的地截止时间反向搜索，拼接多段联运
- 支持附近城市中转、机场/车站过夜

### 3. 当地交通路线
- 基于 WebSearch 的路线规划（公交/地铁/打车/步行）
- 自动预留缓冲时间，应对突发状况

### 4. 分钟级行程单输出
- 从出发到回家的全程分钟级安排
- 风险等级评估（LOW / MEDIUM / HIGH）
- 即使不可行，也会展示所有尝试过程和替代建议

## 项目结构

```
.
├── .claude/
│   └── commands/
│       └── concert-trip-planner.md       # Claude Code slash 命令入口
├── references/
│   ├── concert-info-search.md            # 演唱会搜索指南
│   ├── transport-search.md               # 交通搜索（WebSearch 版）
│   ├── local-route-planning.md           # 当地路线规划（WebSearch 版）
│   ├── trip-output-template.md           # 行程单输出模板
│   ├── risk-and-buffer-rules.md          # 风险与缓冲规则
│   ├── extended-transport-options.md     # 扩展交通方式
│   └── reverse-planning-strategy.md      # 反向拼图规划策略
└── README.md
```

## 使用方法

这是一个 **Claude Code Skill**，通过 slash 命令激活。

### 激活方式

在 Claude Code 中输入：

```
/concert-trip-planner
```

然后按提示提供：
- 出发城市
- 演唱会名称 + 日期
- 最早出发时间 / 最晚到达要求
- 返程截止时间
- 返程目的地

### Agent 工作流程

1. **收集信息**：出发城市、演唱会名称+日期、最早出发时间、返程截止时间
2. **搜索演唱会**：验证场地、日期、开场时间、历史时长
3. **规划去程**：WebSearch 搜索大交通（高铁/飞机等），预留场馆缓冲
4. **规划当地路线**：机场/车站 → 场馆（WebSearch 查询路线时间）
5. **规划返程路线**：场馆 → 返程出发点
6. **规划返程交通**：搜索返程车次/航班，必要时启动反向规划
7. **输出行程单**：分钟级安排 + 风险评估

### 用户示例

> "我在泰州，想去看汪苏泷6月13日太原演唱会，次日8点前回到泰州"

Agent 会：
1. WebSearch 汪苏泷"明日世界"巡演信息，验证历史时长约 150 分钟
2. WebSearch 泰州→太原去程高铁班次
3. WebSearch 太原南站→山西体育中心体育场当地路线
4. **尝试返程**（难点）：
   - 直达高铁：次日最早到达泰州为下午 → 不满足 8:00 约束
   - 反向规划：WebSearch 8:00 前到泰州的车次，发现主要来自南京/徐州方向
   - 扩展方式：尝试顺风车、夜间大巴、自驾等
   - 多段联运：评估太原→南京过夜→南京→泰州的可行性
5. 最终结论：当前约束下不可行，给出替代方案（改看6/14场次 或 放宽返程时间）

## 技能特色

### v2 核心升级

| 功能 | v1 | v2 |
|------|-----|-----|
| 演唱会时长 | 固定估算 2.5h | **搜索历史场次时长** |
| 交通方式 | 高铁/飞机 | **+ 顺风车/大巴/自驾/过夜** |
| 返程规划 | 只查直达 | **反向拼图 + 多段联运** |
| 不可行处理 | 直接说 NO | **展示所有尝试 + 替代建议** |

### 特种兵精神

- 不怕苦不怕累
- 直达不是唯一选择
- 时间优先于舒适
- 最低风险优先（不是最便宜或最快）

## 工具栈

- **Claude Code Skill**：`.claude/commands/` slash 命令
- **WebSearch**：演唱会信息、往返交通、当地路线、顺风车、大巴班次等
- **WebFetch**：读取具体页面获取详细信息

## 文件说明

### .claude/commands/concert-trip-planner.md
技能主入口（slash 命令），定义工作流程、输入要求、优化目标、缓冲规则、Must Have / Must NOT Have。

### references/concert-info-search.md
演唱会信息搜索指南。要求搜索艺人+城市+日期，验证场地和时间，搜索历史时长数据。

### references/transport-search.md
交通搜索参考（Claude Code 版）。包含 WebSearch 查询模板，以及当找不到直达方案时的 fallback 策略。

### references/local-route-planning.md
当地路线规划参考（Claude Code 版）。基于 WebSearch 的地址解析和路线查询，不依赖 AMap Skills API。

### references/extended-transport-options.md
扩展交通方式指南，包含8种允许方式（火车/飞机/顺风车/自驾/夜间大巴/机场过夜/车站过夜/多段联运），明确排除包车/专车。

### references/reverse-planning-strategy.md
反向拼图规划策略。5步反向搜索流程、中转城市选择规则、太原→泰州示例、返程优先原则。

### references/risk-and-buffer-rules.md
风险与缓冲规则。定义固定缓冲，风险分级（LOW/MEDIUM/HIGH/NO VIABLE），多段联运风险升级规则。

### references/trip-output-template.md
行程单输出模板。包含分钟级安排、风险摘要、来源引用、不可行处理模板。

## 开发历程

### v1.0（2026-05-28）
- 基础功能：演唱会搜索、往返交通规划、当地路线、分钟级行程单
- 平台：OpenClaw

### v2.0（2026-05-29）
- 历史时长搜索、扩展交通方式、反向拼图规划
- 平台：OpenClaw

### v3.0（Claude Code 适配版，2026-05-29）
- 从 OpenClaw Skill → Claude Code slash 命令
- FlyAI 工具 → WebSearch / WebFetch
- AMap Skills → WebSearch 路线查询
- 入口从 `SKILL.md` 移至 `.claude/commands/concert-trip-planner.md`

## 使用限制

- 这是一个 **Claude Code 技能**，需在 Claude Code 环境中使用
- 不处理购票/订酒店等交易操作
- 不提供吃喝玩乐推荐
- 搜索结果不保证实时准确，以官方渠道为准

## License

MIT

---

*Made with 💪 特种兵精神 — 不怕苦，不怕累，直达不是唯一选择*
