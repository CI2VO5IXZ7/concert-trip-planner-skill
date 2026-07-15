# Transport Search Reference

Use **flyai (飞猪)** for all major transport searches (train + flight). Search outbound and return as separate passes. Always choose the lowest-risk option first.

## Environment

```bash
# 飞猪 flyai CLI — 火车/航班查询（每日100次限额）
flyai --help 2>&1 | head -3
echo "FLYAI_API_KEY set: ${FLYAI_API_KEY:+yes}"

# train_list.js 索引 — 某站所有车次（无限，静态）
python3 scripts/train_index_builder.py 2>&1 | head -3

# 高德地图 — 本地路线（无限）
echo "GAODE_API_KEY set: ${GAODE_API_KEY:+yes}"
```

## Station and Airport Names

Use flyai results to get accurate station names. flyai returns structured data with station codes and names:
```json
{
  "depStationCode": "VNP",
  "depStationName": "北京南站",
  "arrStationCode": "WGH",
  "arrStationName": "无锡东站"
}
```

For station code lookup (if needed without flyai), fetch from 12306 directly:
```bash
curl -s "https://kyfw.12306.cn/otn/resources/js/framework/station_name.js" | grep "北京"
```

## Train Search

Use flyai `search-train` command. Supports filtering by time, seat class, price, and sorting.

**flyai search-train 参数：**

| 参数 | 说明 |
|------|------|
| `--origin` | 出发城市/车站 **(必填)** |
| `--destination` | 到达城市/车站 |
| `--dep-date` | 出发日期 (YYYY-MM-DD) |
| `--dep-hour-start/end` | 出发时间范围 (24h) |
| `--arr-hour-start/end` | 到达时间范围 (24h) |
| `--journey-type` | 1=直达, 2=中转 |
| `--seat-class-name` | 坐席: second class, first class, business class, hard sleeper, soft sleeper |
| `--sort-type` | 1=价格降 2=推荐 3=价格升 4=耗时升 5=耗时降 6=出发早 7=出发晚 8=直达优先 |
| `--max-price` | 最高价 (元) |
| `--total-duration-hour` | 最大总时长 (小时) |

**示例：**
```bash
# 直达：北京→无锡，12-16点出发，按出发时间排序
flyai search-train --origin "北京" --destination "无锡" --dep-date 2026-08-23 \
  --dep-hour-start 12 --dep-hour-end 16 --sort-type 6

# 中转：自动推荐中转方案
flyai search-train --origin "北京" --destination "无锡" --dep-date 2026-08-23 \
  --journey-type 2 --sort-type 6

# 夜车：22点后出发
flyai search-train --origin "北京" --destination "无锡" --dep-date 2026-08-23 \
  --dep-hour-start 22 --sort-type 6
```

### 特种兵返程：演唱会后搜索策略

演唱会结束后，需要搜索所有可能的返程交通。分两段搜索：

**凌晨段（演唱会结束 → 次日6点）：**
```bash
flyai search-train --origin "北京" --destination "无锡" --dep-date 2026-08-23 \
  --dep-hour-start 22 --sort-type 6
```

**早班段（次日6点 → 截止时间）：**
```bash
flyai search-train --origin "北京" --destination "无锡" --dep-date 2026-08-24 \
  --dep-hour-start 6 --arr-hour-end 12 --sort-type 6
```

## Flight Search

Use flyai `search-flight` command. Similar parameters to train search.

**flyai search-flight 参数：**

| 参数 | 说明 |
|------|------|
| `--origin` | 出发城市/机场 **(必填)** |
| `--destination` | 到达城市/机场 |
| `--dep-date` | 出发日期 (YYYY-MM-DD) |
| `--dep-hour-start/end` | 出发时间范围 (24h) |
| `--journey-type` | 1=直达, 2=中转 |
| `--seat-class-name` | 舱位: economy, business, first |
| `--sort-type` | 1=价格降 2=推荐 3=价格升 4=耗时升 5=耗时降 6=出发早 7=出发晚 8=直达优先 |
| `--max-price` | 最高价 (元) |

**示例：**
```bash
# 直达航班
flyai search-flight --origin "北京" --destination "无锡" --dep-date 2026-08-23 \
  --sort-type 3

# 深夜航班（演唱会后）
flyai search-flight --origin "北京" --destination "无锡" --dep-date 2026-08-23 \
  --dep-hour-start 22 --sort-type 6

# 附近机场
flyai search-flight --origin "北京" --destination "南京" --dep-date 2026-08-24 \
  --dep-hour-start 6 --sort-type 6
```

## 多机场搜索

大城市通常有多个机场，必须同时搜索：
```bash
# 北京出发：首都机场 + 大兴机场
flyai search-flight --origin "北京" --destination "无锡" --dep-date 2026-08-23

# 附近目的地机场
flyai search-flight --origin "北京" --destination "南京" --dep-date 2026-08-23
flyai search-flight --origin "北京" --destination "常州" --dep-date 2026-08-23
```

flyai 会自动搜索该城市所有机场的航班。

## 中转火车全量碰撞

当直达方案不可行时，用 train_list.js 索引做全量碰撞：

```bash
# Step A: 查询出发城市所有车站的车次
python3 scripts/train_index_builder.py --query "北京南"
python3 scripts/train_index_builder.py --query "北京"
python3 scripts/train_index_builder.py --query "北京西"

# Step B: 查询目的地所有车站的车次
python3 scripts/train_index_builder.py --query "无锡"
python3 scripts/train_index_builder.py --query "无锡东"

# Step C: 交叉匹配 → 得到候选中转城市

# Step D: 逐个验证
flyai search-train --origin "北京" --destination "南京" --dep-date 2026-08-23 --dep-hour-start 22
flyai search-train --origin "南京" --destination "无锡" --dep-date 2026-08-24 --arr-hour-end 9
```

## 扩展交通方式

当火车和飞机都不可行时，搜索替代方案：

**顺风车 / 大巴：**
```bash
# 用 web_search 搜索
web_search("北京到无锡 顺风车 8月23日晚上")
web_search("北京到无锡 大巴 夜班")
```

**自驾：**
```bash
# 用高德计算距离和时间
curl -s "https://restapi.amap.com/v3/direction/driving?origin={起点坐标}&destination={终点坐标}&key=$GAODE_API_KEY"
```

## Reliability Notes

1. **flyai 返回空结果** — 不要直接判无方案，标注数据可能不完整并提示人工复核。
2. **flyai 体验模式** — 未设置 FLYAI_API_KEY 时返回的结果可能受限（价格显示为"5xx"），必须设置 API Key。
3. **中转方案验证** — flyai 返回的中转方案需要验证换乘时间是否充足（同站≥15分钟，跨站≥实测交通时间+15分钟）。
4. **train_list.js 索引** — 索引基于12306静态数据，调图时更新（通常季度/半年）。索引只包含车次的起点和终点，不包含经停站。如需查询经停站，需用携程问道。
