# Draft: Concert Trip Planner Skill Optimization

## Optimization Requests (from user)

### 1. 历史演唱会时长搜索
**需求**: 不能简单用 start time + 2.5h 估算结束时间。
**策略**: 
- 搜索到具体主题（如"汪苏泷 明日世界"）后，主动搜索该主题的历史场次时长
- 如果该主题是新主题/第一场，则搜索该艺人过往演唱会主题的平均时长
- 在 concert-info-search.md 中增加"时长验证"章节

### 2. 特种兵交通方式扩展
**需求**: 特种兵不怕苦不怕累，交通方式要全面。
**允许的方式**:
- ✅ 火车/高铁/动车
- ✅ 飞机
- ✅ 顺风车（滴滴/哈啰等）
- ✅ 自驾（含租车）
- ✅ 机场过夜
- ✅ 车站过夜
- ✅ 凌晨大巴
- ✅ 夜间大巴
- ✅ 附近城市中转（多段联运）
- ❌ 包车/专车（费用过高，用户明确排除）

**新增文件**: references/extended-transport-options.md

### 3. 反向凑行程策略（拼图规划）
**需求**: 不能只看直达，要具备拼图能力。
**策略**:
- 先看"几点前有哪些车次到目的地"
- 再看"这些车次的来源方向是否靠近演唱会城市"
- 支持多段联运：演唱会城市→中转城市→目的地
- 中转城市选择：优先考虑距离演唱会城市较近、且交通便利的城市
- 新增文件: references/reverse-planning-strategy.md

## 技术决策
- **最小修改原则**: 尽量复用现有文件结构，新增2个reference文件
- **向后兼容**: 现有功能保持不变，只做增量增强
- **优先级**: 改进3（反向规划）影响最大，改进2（交通扩展）次之，改进1（时长搜索）相对独立

## 修改文件清单
1. `SKILL.md` - 更新workflow、新增步骤
2. `references/concert-info-search.md` - 新增"时长验证"章节
3. `references/flyai-transport-search.md` - 扩展交通方式列表
4. `references/risk-and-buffer-rules.md` - 新增反向规划规则
5. `references/extended-transport-options.md` - **新建** - 特种兵交通方式详细指南
6. `references/reverse-planning-strategy.md` - **新建** - 反向拼图规划策略

## 测试策略
- 用同一个测试案例（汪苏泷6/13太原→泰州，次日8:00前到）重新验证
- 评估改进后是否能产出可行的特种兵方案
