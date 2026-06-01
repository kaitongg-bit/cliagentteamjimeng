# CLI Agent Team Jimeng

面向 **10 分钟 AI 微电影剧本开发** 的 Agent Team 验证仓库。

当前阶段先只看一件事：

> 同一个 10 分钟短片创意，Agent Team 是否比 Single Agent 更能把剧本从“顺着想法扩写”推进到“结构更硬、反转更清楚、可拍性更强”的版本。

Moodboard MVP、即梦出图、粗分镜、细分镜、prompt pack 都已经有过探索，但在这份 README 里先标为后续模块，可以先不看。

## 现在验证什么

本仓库当前重点是 **剧本阶段**。

验证方式很简单：

1. Human 给一个原始故事种子。
2. Single Agent 在干净上下文里直接写一版完整剧本。
3. Agent Team 按角色分工多轮推进：编剧先写，反方/观众/导演/审片人提出问题，Showrunner 综合取舍，再让编剧改版。
4. 对比两条链路的最终剧本和过程产物，看 Agent Team 到底带来了什么增益。

重点不是证明“多 agent 一定更好”，而是要能回答：

- 哪些问题是 single agent 没主动发现的？
- 哪些问题是 agent team 通过 debate / review / synthesis 找出来的？
- 多出来的 token、时间、复杂度，是否换来了更好的剧本质量和更可执行的过程产物？
- 这个流程未来是否值得产品化成创作入口？

## Agent Team 一般怎么做剧本

当前剧本链路采用 `Showrunner + 子 agent` 的方式。

### 1. Human 输入

Human 提供故事种子、目标、偏好和中途判断。Human 不是旁观者，而是创作总方向的重要输入源。

### 2. 编剧 Agent 首轮发力

编剧 agent 根据 brief 输出：

- 故事方向或多个方向
- 主要人物关系
- 10 分钟体量判断
- 初版剧本或关键场次

### 3. 反方 / 观众 / 导演 / 审片人复审

不同 agent 不负责“附和编剧”，而是从不同角度拆问题：

- **反方编剧**：找俗套、逻辑洞、价值偏向、误读风险。
- **观众**：判断看不看得懂、想不想继续看、哪些点会懵。
- **导演**：判断场次情绪、动作化表达、镜头调度和可拍性。
- **审片人**：按电影节短片标准给潜力评分和硬伤排序。

### 4. Showrunner 综合取舍

Showrunner 不把所有意见平均混合，而是做创作决策：

- 哪些建议必须采纳？
- 哪些漂亮但会误导的东西要删？
- 下一版只解决哪几个核心问题？
- 给编剧 agent 的下一轮任务是什么？

### 5. 编剧 Agent 改出新版

编剧 agent 不重新发散世界观，而是在 Showrunner 决策下改出 v2 / v3。这样可以看见 agent team 的真实价值：不是“多写几版”，而是让每一轮都有明确的质量提升目标。

## 子 Agent YAML 去哪看

精细设定在：

```text
agents/specs/
```

主要文件：

```text
agents/specs/showrunner.yaml                 # Showrunner / 总控取舍
agents/specs/screenwriter.yaml               # 编剧 Agent
agents/specs/opposition_writer.yaml          # 反方编剧
agents/specs/audience_panel.yaml             # 观众 Agent
agents/specs/director.yaml                   # 导演 Agent
agents/specs/critic.yaml                     # 审片人 / 评审
agents/specs/script_doctor.yaml              # 剧本医生
agents/specs/visual_concept_designer.yaml    # 美术概念，后续看
agents/specs/storyboard_agents.yaml          # 粗细分镜，后续看
agents/specs/prompt_structurer.yaml          # 即梦提示词结构化，后续看
agents/specs/prompt_compliance_reviewer.yaml # 提示词过审，后续看
```

补充说明见：

```text
agents/specs/README.md
```

其中编剧方法论会引用用户本机的 `screenwriting-master.skill`，仓库里的 `screenwriter.yaml` 主要定义它在 agent team runtime 里如何被调用。

## 当前 Case 测试情况

目前正式测了两个 **10 分钟戛纳 / 微电影节取向短片** 的剧本 case。

### Case 1：《定稿》/ 大明星隐形霸凌与剪辑师操控叙事

路径：

```text
runs/20260527_194857_invisible-bullying-world-trial/
```

看什么：

```text
00_brief/user_story_seed.md
01_single_agent/single_agent_clean_context_script.md
02_agent_team/drafts/dinggao_full_script_scenes1_7_round10_revised.md
02_agent_team/round9_showrunner_synthesis_full_script_review.md
```

这个 case 跑得更完整，除了剧本外还走到了美术概念、即梦提示词、moodboard、粗分镜、细分镜。  
但如果你现在只关心“剧本 agent team 是否有效”，优先看 `02_agent_team/` 和 `01_single_agent/` 即可。

### Case 2：《黑绳》/ 湖神献祭与灾祸转嫁制度

路径：

```text
runs/20260601_lake-sacrifice-misfortune/
```

Human 原始故事种子：

```text
runs/20260601_lake-sacrifice-misfortune/00_brief/user_story_seed.md
```

Agent Team 版本：

```text
runs/20260601_lake-sacrifice-misfortune/02_agent_team/drafts/lake_sacrifice_script_v1.md
runs/20260601_lake-sacrifice-misfortune/02_agent_team/drafts/lake_sacrifice_script_v2.md
```

Agent Team 过程产物：

```text
runs/20260601_lake-sacrifice-misfortune/02_agent_team/agent_outputs/round1_screenwriter_concept_options.md
runs/20260601_lake-sacrifice-misfortune/02_agent_team/agent_outputs/round1_opposition_risk_report.md
runs/20260601_lake-sacrifice-misfortune/02_agent_team/agent_outputs/round1_audience_reaction.md
runs/20260601_lake-sacrifice-misfortune/02_agent_team/round1_showrunner_synthesis.md
runs/20260601_lake-sacrifice-misfortune/02_agent_team/agent_outputs/round3_opposition_review_on_script_v1.md
runs/20260601_lake-sacrifice-misfortune/02_agent_team/agent_outputs/round3_audience_reaction_on_script_v1.md
runs/20260601_lake-sacrifice-misfortune/02_agent_team/agent_outputs/round3_director_review_on_script_v1.md
runs/20260601_lake-sacrifice-misfortune/02_agent_team/agent_outputs/round3_critic_review_on_script_v1.md
runs/20260601_lake-sacrifice-misfortune/02_agent_team/round3_showrunner_synthesis_script_v1_review.md
runs/20260601_lake-sacrifice-misfortune/02_agent_team/agent_outputs/round4_screenwriter_v2_revision_notes.md
```

Single Agent 干净上下文版本：

```text
runs/20260601_lake-sacrifice-misfortune/03_single_agent_baseline/single_agent_script_v1.md
```

这个 case 的对比最干净：  
Single Agent 只拿到原始故事种子；Agent Team 则经过编剧、反方、观众、导演、审片人和 Showrunner 多轮协作。

初步观察：

- Single Agent 版本更顺、更直接，像把原始故事扩写成完整短片。
- Agent Team 版本更关注“制度断链”的因果，反复修正了普通民俗故事里容易出现的误读：可怜少女献祭、湖神天罚、恋人被爱情祝福。
- 《黑绳》v2 把关键因果改成了可拍动作：黑绳替换规则、阿沅赴湖动机、阿澈家安全机制都更清楚。

## 怎么看过程产物时间线 HTML

时间线页面用于看 agent team 过程里每一步发生了什么：Human 输入、哪个 agent 产出、Showrunner 如何综合、最后形成什么文件。

### 默认打开 Case 1 时间线

生成静态页面：

```bash
python3 scripts/build_agent_timeline.py \
  --run runs/20260527_194857_invisible-bullying-world-trial
```

启动本地服务：

```bash
python3 scripts/moodboard_server.py \
  --run runs/20260527_194857_invisible-bullying-world-trial \
  --port 8767
```

浏览器打开：

```text
http://127.0.0.1:8767/timeline
```

也可以直接看静态文件：

```text
ui/agent_timeline.html
```

注意：当前 timeline 构建脚本主要为 Case 1 的完整流程写了详细时间线条目。Case 2 的文件已经完整落盘，但 timeline 模板还没有专门适配；目前建议直接看 Case 2 的文件路径列表。

## 暂时可以不看的后续模块

这些模块对“AI 视频完整生产链路”有价值，但如果你现在只向研发或老板解释 **剧本 agent team 是否有效**，可以先跳过：

```text
ui/moodboard.html
docs/moodboard_mvp_prd.md
docs/moodboard_mvp_runbook.md
runs/20260527_194857_invisible-bullying-world-trial/05_moodboard/
runs/20260527_194857_invisible-bullying-world-trial/03_storyboards/
runs/20260527_194857_invisible-bullying-world-trial/04_visual_concept/
runs/20260527_194857_invisible-bullying-world-trial/03_jimeng/
```

后续如果继续从剧本走到 AI 视频生产，它们会重新变重要：

- Moodboard MVP：让 Human 先找参考图，避免 AI 生图带偏审美。
- 美术概念：定义影片直观质感、影调、材质、媒介感。
- 粗分镜 / 细分镜：把剧本转成镜头和即梦可执行片段。
- Prompt Structurer：把人物设定、关键镜头、场景转成短而结构化的即梦提示词。

## 推荐给研发 / 老板的阅读顺序

如果时间很少，建议只看：

1. `agents/specs/README.md`
2. `agents/specs/screenwriter.yaml`
3. `agents/specs/opposition_writer.yaml`
4. `agents/specs/audience_panel.yaml`
5. `agents/specs/director.yaml`
6. `agents/specs/critic.yaml`
7. `runs/20260601_lake-sacrifice-misfortune/03_single_agent_baseline/single_agent_script_v1.md`
8. `runs/20260601_lake-sacrifice-misfortune/02_agent_team/drafts/lake_sacrifice_script_v2.md`
9. `runs/20260601_lake-sacrifice-misfortune/02_agent_team/round3_showrunner_synthesis_script_v1_review.md`

这样可以最快看见：同一个原始创意，Single Agent 写成什么，Agent Team 如何发现问题并把 v1 推进到 v2。

## 项目状态

这是验证仓库，不是最终产品。

当前已验证到：

- 有真实 sub-agent 参与的剧本协作流程可以跑通。
- 子 agent YAML 设定已经放在 `agents/specs/`。
- 两个 10 分钟短片 case 已经有可对比产物。
- 《黑绳》case 已经形成较清晰的 Single Agent vs Agent Team baseline。

下一步建议：

1. 给 Case 2 增加专属 timeline HTML。
2. 用统一评分表对 Single Agent 与 Agent Team 版本打分。
3. 继续让审片人 / Human 对《黑绳》v2 做最终剧本质量判断。
4. 再决定是否进入美术概念、moodboard、分镜和即梦生成。
