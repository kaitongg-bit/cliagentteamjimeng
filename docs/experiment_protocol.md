# Experiment Protocol

## 实验问题

同一个 10 分钟微电影创作 brief 下：

> Agent Team 是否比 Single Agent 产出更好的创意、剧本、视觉设计、分镜、即梦 prompt、审片反馈和最终视频？

## 对照组设计

### A 组：Single Agent

一个全能 Agent 一次性或少轮次完成：

- Logline
- 人物
- 剧本
- 美术风格
- 分镜
- 即梦 prompt
- 自评

优点：快、成本低、路径简单。

风险：审美判断混在一起，容易出现提示词噪音、镜头动机弱、风格漂移、审片反馈泛。

### B 组：Agent Team

按制作组拆分：

- 编剧
- 美术概念设计师
- 导演
- 粗分镜师
- 细分镜师
- 制片人
- 剪辑
- AI 演员演技指导
- 审片人
- 观众

并加入：

- debate loop
- critic-revise loop
- red team review
- decision log

优点：专业判断更细，过程产物可审查。

风险：更慢、更贵，可能互相拉扯，需要 Showrunner 做取舍。

## 固定输入

每次实验必须固定：

- 同一个 brief
- 同一个目标时长：10 分钟
- 同一个目标质量：可冲击微电影节/电影节短片审美
- 同一套生成工具：即梦 CLI 为主
- 同一套评分标准
- 同一批评审人或评审 Agent

## 必交过程产物

| 阶段 | Single Agent | Agent Team |
|---|---|---|
| 创意 | `single_concept.md` | `concept_debate.md`, `decision_log.md` |
| 剧本 | `single_screenplay.md` | `logline.md`, `four_act_outline.md`, `screenplay_v1.md`, `script_doctor_report.md`, `screenplay_v2.md` |
| 美术 | `single_visual_prompt.md` | `visual_bible.md`, `moodboard_spec.md`, `color_script.md` |
| 分镜 | `single_storyboard.md` | `coarse_storyboard.md`, `fine_storyboard.csv`, `continuity_check.md` |
| 表演 | 可选 | `performance_beats.md` |
| 制片 | 可选 | `production_plan.md`, `cost_risk_table.md` |
| 即梦 | `single_jimeng_prompts.md` | `team_jimeng_prompts.md`, `revision_prompts.md` |
| 审片 | `single_self_review.md` | `critic_review.md`, `audience_reaction.md` |

## 评分表

每项 1-5 分，允许半分。

| 维度 | 说明 |
|---|---|
| 创意新颖度 | 是否有独特命题、反差、形式或意象 |
| 剧本结构 | 钩子、冲突、升级、高潮、结尾是否成立 |
| 角色弧光 | Want / Need / Arc 是否清晰且不可逆 |
| 可拍性 | 是否能被镜头表达，而不是靠解释 |
| 视觉风格 | 色彩、材质、光影、时代语汇是否统一 |
| 镜头语言 | 景别、视线、轴线、运镜是否有叙事动机 |
| 分镜可执行性 | 是否能直接指导生成与剪辑 |
| Prompt 质量 | 结构化、无矛盾、少噪音、适配即梦 |
| 表演指导 | 情绪是否落到眼神、呼吸、停顿、动作 |
| 剪辑节奏 | 是否有节奏波形，是否避免 10 分钟疲劳 |
| 观众理解 | 是否能看懂核心冲突和结尾 |
| 记忆点 | 是否有 1-3 个离场后仍记得的画面 |
| 首轮可用率 | 生成素材首轮可用比例 |
| 迭代效率 | 达到可用版本所需轮数和人工干预 |
| 综合潜力 | 是否接近可投微电影节的完整度 |

## 评估方法

建议三层评估：

1. **盲评文本产物**：隐藏 A/B 来源，只看剧本、分镜、prompt。
2. **盲评视频素材**：隐藏来源，只看即梦生成片段。
3. **生产复盘**：公开 A/B 来源，比较时间、成本、可控性、返工点。

## 通过标准

如果 Agent Team 同时满足以下条件，可以认为值得进入产品化入口探索：

- 综合质量均分比 Single Agent 高 15% 以上。
- 至少 5 个关键维度显著更好：剧本、视觉、镜头、prompt、审片。
- 首轮可用率提高，或总返工时间下降。
- 用户能明确说出 Agent Team 的过程产物帮助其判断和修改。
- 成本/延迟在可接受范围内，或可作为专业模式/高级模式。

## 产品入口判断

不要把入口叫“Agent Team”。

更接近用户语言的入口可能是：

- AI 编剧室
- AI 导演组
- 电影级创作模式
- 多角色共创
- 让 AI 制作组打磨
- 专业分镜与审片

验证时记录用户更愿意点击哪种表达。
