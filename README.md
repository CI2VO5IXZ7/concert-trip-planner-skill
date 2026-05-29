# 🎵 演唱会特种兵行程规划器

一个专为特种兵式看演唱会设计的 Claude Code 自定义命令，帮你规划最紧凑、最省心的往返行程。

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
- 基于**高德地图 REST API** 的精确路线规划（公交/地铁/打车/步行）
- 实测距离和时间，不估算
- 自动预留缓冲时间，应对突发状况

### 4. 分钟级行程单输出
- 从出发到回家的全程分钟级安排
- 风险等级评估（LOW / MEDIUM / HIGH）
- 即使不可行，也会展示最早可达时间和替代建议

## 项目结构

```
.
├── .claude/
│   └── commands/
│       └── concert-trip-planner.md       # slash 命令入口
├── references/
│   ├── concert-info-search.md            # 演唱会信息搜索指南
│   ├── transport-search.md               # 交通搜索（FlyAI + 12306）
│   ├── local-route-planning.md           # 当地路线规划（高德 REST API）
│   ├── trip-output-template.md           # 行程单输出模板
│   ├── risk-and-buffer-rules.md          # 风险与缓冲规则
│   ├── extended-transport-options.md     # 扩展交通方式
│   └── reverse-planning-strategy.md      # 反向拼图规划策略
└── README.md
```

## 使用方法

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

### 前置条件

| 工具 | 安装/配置 |
|------|---------|
| FlyAI CLI | `npm i -g @fly-ai/flyai-cli` |
| 高德地图 Web服务 Key | [高德开放平台](https://console.amap.com/dev/key/app) → 添加Key → 服务平台选「Web服务」 |

### Agent 工作流程

1. **环境检查**：确认 FlyAI 已安装、AMap Key 已就绪
2. **收集信息**：出发城市、演唱会名称+日期、最早出发时间、返程截止时间
3. **搜索演唱会**：WebSearch 验证场地、日期、开场时间、历史时长
4. **规划去程**：FlyAI 搜索大交通（高铁/飞机），预留场馆缓冲
5. **规划当地路线**：高德 REST API 查询机场/车站 → 场馆的实测路线和时间
6. **规划返程路线**：高德 REST API 查询场馆 → 返程出发点
7. **规划返程交通**：FlyAI 双段搜索（凌晨段 + 早班段），必要时启动反向规划
8. **输出行程单**：分钟级安排 + 风险评估 + 不可行时给出最早可达时间

### 用户示例

> "我在某城市，想去看异地演唱会，次日上午前回到出发地"

Agent 会：
1. WebSearch 验证演唱会场地和历史时长
2. FlyAI 搜索出发城市→目的地去程高铁
3. 高德 REST API 查询到站→场馆的地铁路线（实测时间）
4. **反向规划返程**（凌晨段 + 早班段双次搜索）：
   - 若无直达夜间高铁，评估最早班次能否满足截止时间
   - 尝试多段联运：目的地→中转城市（凌晨动车）→换乘高铁→自驾/打车回目的地
5. 找到可行链条后输出完整分钟级行程单，附风险评估
6. 若不可行，给出最早可达时间供用户判断是否放宽约束

## 工具栈

| 工具 | 用途 |
|------|------|
| **FlyAI CLI** | 火车/航班实时搜索，站名/航班号来自票务数据库 |
| **高德地图 REST API** | 地理编码、驾车/公交路线规划，实测距离和时间 |
| **WebSearch / WebFetch** | 演唱会信息、顺风车、大巴班次等补充搜索 |

## 文件说明

### .claude/commands/concert-trip-planner.md
slash 命令主入口，定义工作流程、环境检查、输入要求、优化目标、缓冲规则、Must Have / Must NOT Have。

### references/transport-search.md
交通搜索指南。FlyAI CLI 为主、12306 skill 为备。**返程强制双段搜索**（凌晨段 + 早班段），防止漏掉演唱会后的关键班次。

### references/local-route-planning.md
当地路线规划指南。基于高德 Web服务 REST API（`/v3/geocode/geo`、`/v3/direction/driving`、`/v3/direction/transit`），含完整 curl 调用模板。

### references/concert-info-search.md
演唱会信息搜索指南。包含历史时长搜索策略，以及用户直接提供信息时的处理规范。

### references/risk-and-buffer-rules.md
风险与缓冲规则。定义固定缓冲，风险分级（LOW/MEDIUM/HIGH/NO VIABLE），不可行时强制输出最早可达时间。

### references/extended-transport-options.md
扩展交通方式：火车/飞机/顺风车/自驾/夜间大巴/机场过夜/车站过夜/多段联运，明确排除包车/专车。

### references/reverse-planning-strategy.md
反向拼图规划策略。从返程截止时间反向锁定可行链条，返程优先原则，中转城市选择规则。

### references/trip-output-template.md
行程单输出模板，含分钟级时间轴、风险摘要、来源引用、不可行处理模板。

## 开发历程

### v1.0 / v2.0（2026-05-28 ~ 05-29）
基础功能搭建：演唱会搜索、往返交通规划、当地路线、分钟级行程单、历史时长搜索、扩展交通方式、反向拼图规划。

### v3.0（2026-05-29）
适配 Claude Code：入口改为 `.claude/commands/` slash 命令，工具层重写。

### v3.1（2026-05-29）
经模拟测试发现并修复的问题：
- 火车/航班查询从 WebSearch 改为 **FlyAI CLI**（消除站名幻觉问题）
- 本地路线从估算改为 **高德 REST API** 实测（明确 Web服务 Key 要求）
- 返程搜索改为**凌晨 + 早班双段强制执行**，防止漏掉关键班次
- No-Viable-Plan 时强制输出**最早可达时间**
- 新增用户直接提供演唱会信息的处理规范

## 使用限制

- 需在 Claude Code 环境中使用
- 需要 FlyAI CLI 和高德 Web服务 Key
- 不处理购票/订酒店等交易操作
- 不提供吃喝玩乐推荐
- 搜索结果不保证实时准确，以官方渠道为准

## License

MIT

---

*Made with 💪 特种兵精神 — 不怕苦，不怕累，直达不是唯一选择*
