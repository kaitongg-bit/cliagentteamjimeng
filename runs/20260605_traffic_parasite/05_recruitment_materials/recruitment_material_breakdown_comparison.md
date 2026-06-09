# 招募/素材挖掘对比：agent team vs single agent

## 对比对象

agent team：

- `recruitment_material_breakdown_v1_by_recruitment_agent.md`
- `agent_reviews/recruitment_reviewer_screenwriter.md`
- `agent_reviews/recruitment_reviewer_visual_concept.md`
- `recruitment_material_breakdown_agent_team.md`

single agent：

- `baseline/recruitment_material_breakdown_single_agent.md`

## 实验隔离

single agent baseline 只拿到同样三个输入文件：

- 剧情梗概；
- `0:00-3:00` 即梦提示词；
- `3:00-6:00` 即梦提示词。

它没有拿到 reviewer 批评，也没有进入“主 agent 出 v1 -> 编剧审 -> 美术审 -> Showrunner 收敛”的流程。

## 主要差异

| 维度 | single agent baseline | agent team 最终版 | 增益 |
|---|---|---|---|
| 完整性 | 角色、场景、道具覆盖完整 | 在完整基础上补庆功宴摄影师/合影执行人员、法务 P0、关键动作资产包 | 从清单变成可执行资产体系 |
| 叙事必要性 | 大多按素材类别列出 | 区分“故事资产”和“氛围素材”，明确手机离身、屏幕背向他、低姿态回应不是道歉 | 降低素材多但剧情读不懂的风险 |
| 视觉统一 | 有冷白/暖金/服务通道等方向 | 增加视觉世界硬规则、视觉母题、人物服装细节和空间误读禁区 | 更利于后续视觉圣经 |
| 生成风险 | 禁止可读文字、logo、短剧感 | 升级为统一后期资产包，明确哪些屏幕/文件/文字交给后期 | 更符合 AIGC 视频生产 |
| 角色区分 | 助理、运营、公关、法务都有列出 | 明确四者视觉和动作职责，避免职业装群像混在一起 | 降低观众理解断裂 |
| Moodboard | 有搜索关键词 | 要求 P0 空间每个至少 6 张参考，并说明全景/材质/灯光/站位 | 更可指导 Human 找图 |

## 评分

| 维度 | single agent | agent team | 说明 |
|---|---:|---:|---|
| 完整性 | 8 | 9 | single 已覆盖主体；agent team 补了剧情关键动作和法务优先级 |
| 叙事必要性 | 6 | 9 | reviewer 明确哪些素材必须让观众一眼看懂 |
| 视觉统一性 | 7 | 9 | 美术 reviewer 增加硬规则和材质母题 |
| 生成风险意识 | 8 | 9 | 两者都知道禁文字；agent team 更明确后期资产包 |
| Human 可用性 | 7 | 9 | agent team 更适合指导 Human 找 moodboard 和确认素材 |
| 后续依赖价值 | 7 | 9 | agent team 最终版可直接进入视觉圣经/素材生成 |

平均：

- single agent：7.2
- agent team：9.0

## 可以给老板看的结论

single agent 在招募/素材挖掘节点已经能产出一份完整清单，说明这个节点不需要大量 agent 并行。

但 agent team 的价值在于：

1. 编剧 reviewer 把“素材清单”转成“故事资产”，指出哪些素材如果观众看不懂，剧情会断。
2. 美术 reviewer 把“素材清单”转成“视觉锁定包”，指出哪些人物、空间、道具必须先锁形状和材质。
3. Showrunner 把批评合并为最终表，避免 reviewer 只是增加意见噪音。

因此，招募/素材挖掘阶段推荐最小 agent team：

- 主：素材招募 agent；
- 审：编剧 reviewer；
- 审：美术概念 reviewer；
- 控：Showrunner。

不建议在这个节点启用太多 agent。

## 下一步

进入素材生成小样前，需要先执行：

1. 根据最终表制作 `visual_bible_v1_by_visual_concept_agent.md`。
2. Human 根据 moodboard 搜索清单找 P0 空间参考图。
3. 提示词 agent 基于视觉圣经写：
   - 沈砚三视图；
   - 张总三视图；
   - 高层酒店庆功区；
   - 酒店服务通道；
   - 临时公关房间；
   - 虚构奖杯/手机/文件夹等关键道具。
