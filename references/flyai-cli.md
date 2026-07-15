# flyai (飞猪) CLI 参考

## 概述

阿里巴巴官方发布的旅行技能 CLI，基于飞猪 MCP 协议。覆盖火车、航班、酒店、景点、活动票务。

## 安装

```bash
npm i -g @fly-ai/flyai-cli
```

## 环境变量

```bash
# 正确的变量名（注意大小写）
FLYAI_API_KEY=sk-xxxxx

# ❌ 错误：FlyAI_API_KEY（CLI 不识别）
```

不设置 API Key 时进入"体验模式"，价格显示为"5xx"等模糊值，部分结果受限。

## 每日限额

**100次/天**（非官方文档，实测观察）。需合理分配：
- 火车查询：~10-15次/次行程规划
- 航班查询：~5-10次/次行程规划
- 中转查询：~5次/次行程规划

## 核心命令

### search-train（火车查询）

```bash
flyai search-train \
  --origin "北京" \
  --destination "无锡" \
  --dep-date 2026-08-23 \
  --dep-hour-start 12 \
  --dep-hour-end 16 \
  --journey-type 1 \
  --sort-type 6
```

| 参数 | 说明 |
|------|------|
| `--origin` | 出发城市/车站 **(必填)** |
| `--destination` | 到达城市/车站 |
| `--dep-date` | 出发日期 (YYYY-MM-DD) |
| `--dep-hour-start/end` | 出发时间范围 (24h) |
| `--arr-hour-start/end` | 到达时间范围 (24h) |
| `--journey-type` | 1=直达, 2=中转 |
| `--seat-class-name` | second class, first class, business class, hard sleeper, soft sleeper |
| `--sort-type` | 1=价格降 2=推荐 3=价格升 4=耗时升 5=耗时降 6=出发早 7=出发晚 8=直达优先 |
| `--max-price` | 最高价 (元) |
| `--total-duration-hour` | 最大总时长 (小时) |

### search-flight（航班查询）

参数与 search-train 类似，额外支持：
- `--seat-class-name`: economy, business, first

### search-hotel / search-poi / keyword-search / ai-search

见 `flyai --help`。

## 返回格式

JSON，结构：
```json
{
  "data": {
    "itemList": [{
      "journeys": [{
        "journeyType": "直达|中转",
        "segments": [{
          "depStationCode": "VNP",
          "depStationName": "北京南站",
          "depDateTime": "2026-08-23 12:21:00",
          "arrStationCode": "WGH",
          "arrStationName": "无锡东站",
          "arrDateTime": "2026-08-23 17:43:00",
          "marketingTransportNo": "G745",
          "duration": "322",
          "stopInfos": null
        }]
      }],
      "price": "555.00",
      "jumpUrl": "https://a.feizhu.com/xxx"
    }]
  },
  "message": "success",
  "status": 0
}
```

## 已知限制

1. **stopInfos 始终为 null** — 不返回经停站信息。如需经停站查询，需用携程问道。
2. **无结果时返回 `data: null`** — message 为"智慧交通结果为空"，不是错误。
3. **体验模式** — 未设 API Key 时价格模糊，结果可能不全。
4. **中转推荐是飞猪算法** — 不是全量碰撞，可能遗漏冷门中转方案。需要全量碰撞时需用 train_list.js 离线索引。
5. **station_code 格式** — 返回的是12306电报码（如 VNP=北京南），不是 IATA 码。

## 与携程问道的对比

| | flyai | 携程问道 |
|---|---|---|
| 每日限额 | 100次 | 30次 |
| 火车查询 | ✅ 结构化+筛选 | ✅ 自然语言 |
| 航班查询 | ✅ 结构化+筛选 | ✅ 自然语言 |
| 经停站查询 | ❌ stopInfos=null | ✅ |
| 中转查询 | ✅ journey-type=2 | ❌ |
| API Key | FLYAI_API_KEY | TRIPAI_API_KEY |
| 返回格式 | JSON | 纯文本 Markdown |
