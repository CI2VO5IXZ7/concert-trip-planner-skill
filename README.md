# 🎵 偷偷去看演唱会

一个专为特种兵式看演唱会设计的行程规划技能，帮你规划最紧凑、最省心的往返行程。

**v5.0.0** — 支持 Hermes Agent / OpenClaw / Claude Code

## 什么是特种兵行程？

特种兵行程 = **不怕苦、不怕累、时间优先于舒适**。当天或次日极限往返，不追求吃喝玩乐，只为看一场演唱会。

## 核心能力

### 1. 演唱会信息智能搜索
- 自动搜索并验证演唱会场地、日期、开场时间
- **历史时长验证**：搜索同主题/同艺人过往演唱会时长，不瞎猜 2.5 小时
- 所有信息标注来源和信心度

### 2. 强制搜索矩阵（不遗漏任何维度）
- **直达火车 + 直达航班 + 中转火车 + 飞机+地面交通** 四维度并行搜索
- **全量碰撞找中转**：基于 train_list.js 离线索引，遍历所有车站车次取交集
- 飞猪 flyai 实时数据（含临客），携程问道备用

### 3. 当地交通路线
- 基于**高德地图 REST API** 的精确路线规划（公交/地铁/打车/步行）
- 实测距离和时间，不估算
- 自动预留缓冲时间，应对突发状况

### 4. 分钟级行程单输出
- 从出发到回家的全程分钟级安排
- 风险等级评估（LOW / MEDIUM / HIGH / NO VIABLE）
- 即使不可行，也会展示最早可达时间和替代建议

## 项目结构

```
.
├── SKILL.md                              # 技能主文件（Hermes/OpenClaw）
├── .claude/commands/
│   └── concert-trip-planner.md           # Claude Code slash 命令入口
├── scripts/
│   └── train_index_builder.py            # train_list.js 下载+索引构建
├── data/                                 # 索引数据（git ignore）
│   ├── train_list.js                     # 12306 全国列车列表
│   ├── train_index.json                  # 倒排索引：车站→车次
│   ├── train_by_no.json                  # 正向索引：车次→信息
│   └── metadata.json                     # 元数据
├── references/
│   ├── concert-info-search.md            # 演唱会信息搜索指南
│   ├── transport-search.md               # 交通搜索（flyai + 高德）
│   ├── local-route-planning.md           # 当地路线规划（高德 REST API）
│   ├── trip-output-template.md           # 行程单输出模板
│   ├── risk-and-buffer-rules.md          # 风险与缓冲规则
│   ├── extended-transport-options.md     # 扩展交通方式
│   ├── reverse-planning-strategy.md      # 反向拼图规划策略
│   └── feasibility-examples.md           # 可行性判断示例
└── README.md
```

## 前置条件

| 工具 | 用途 | 安装/配置 |
|------|------|---------|
| **flyai** | 火车/航班/酒店/景点查询 | `npm i -g @fly-ai/flyai-cli` + `FLYAI_API_KEY` |
| **train_list.js 索引** | 某站所有车次（全量碰撞） | `python3 scripts/train_index_builder.py` |
| **高德地图** | 本地路线规划 | [高德开放平台](https://console.amap.com/dev/key/app) → Web服务 Key → `GAODE_API_KEY` |
| **携程问道** | 备用：经停站查询 | 见 ctrip-wendao skill（30次/天） |

## 工具栈

| 工具 | 用途 | 限额 |
|------|------|------|
| **flyai (飞猪)** | 火车/航班实时搜索（含中转推荐） | 100次/天 |
| **train_list.js 索引** | 某站所有车次 → 全量碰撞找中转 | 无限（静态） |
| **高德地图 REST API** | 地理编码、驾车/公交路线规划 | 无限 |
| **携程问道 API** | 备用：经停站查询、航班补充 | 30次/天 |
| **WebSearch** | 演唱会信息、顺风车、大巴 | 无限 |

## Agent 工作流程

1. **环境检查**：确认 flyai 可用、train 索引已建、高德 Key 就绪
2. **可行性粗判**：距离 + 是否有直达线 + 截止时间，先给高/中/低可行性
3. **收集信息**：出发城市、演唱会名称+日期、返程截止时间
4. **搜索演唱会**：WebSearch 验证场地、日期、开场时间
5. **执行搜索矩阵**（四维度并行，不可遗漏）：
   - ① 直达火车（flyai）
   - ② 直达航班（flyai）
   - ③ 中转火车（train_list.js 碰撞 + flyai 验证）
   - ④ 飞机+地面交通（flyai + 高德）
6. **规划当地路线**：高德 REST API 查询实测路线和时间
7. **输出行程单**：分钟级安排 + 风险评估

## 开发历程

### v1.0 / v2.0（2026-05-28 ~ 05-29）
基础功能搭建：演唱会搜索、往返交通规划、当地路线、分钟级行程单。

### v3.0（2026-05-29）
适配 Claude Code：入口改为 `.claude/commands/` slash 命令。

### v4.0（2026-07-15）
- 引入强制搜索矩阵，四维度并行搜索
- 新增全量碰撞找中转逻辑

### v5.0（2026-07-15）
- **工具栈重构**：flyai (飞猪) 替代携程问道/12306-skill
- **train_list.js 索引**：支持全量碰撞找中转点
- **限额优化**：飞猪100次/天，携程问道仅备用（30次/天）
- **移除12306-skill依赖**：12306 API 有反爬，改用飞猪实时数据
- 适配 Hermes Agent SKILL.md 格式

## 使用限制

- 需要 flyai CLI + FLYAI_API_KEY
- 需要高德 Web服务 Key
- 不处理购票/订酒店等交易操作
- 不提供吃喝玩乐推荐
- 搜索结果不保证实时准确，以官方渠道为准

## License

MIT

---

*你别管我今晚在哪，你就看我明天在不在工位就完了*
