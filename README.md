# CLI Agent Team Jimeng

面向 **10 分钟微电影级 AI 视频创作** 的 Agent Team 验证框架。

这个仓库的目标不是先证明“多 Agent 听起来高级”，而是严谨验证：

> 在生成一支可冲击微电影节审美标准的 10 分钟 AI 短片时，Agent Team 是否比 Single Agent 在最终成片和过程产物上都有显著增益。

## 你要验证什么

核心验证对象分三层：

1. **效果增益**：创意、剧本、视觉风格、分镜、表演、剪辑、审片反馈是否更专业。
2. **过程产物增益**：Agent Team 是否产出更可执行的 moodboard、角色卡、粗细分镜、即梦 prompt、审片报告。
3. **成本收益**：多 Agent 的额外时间和 token 成本，是否换来更高首轮可用率、更少废片、更少人工返工。

## 项目结构

```text
docs/
  agent_team_architecture.md     # Agent Team 总架构
  experiment_protocol.md         # Single Agent vs Agent Team 对照实验
  human_in_the_loop.md           # 人类参与点与 token 控制策略
  agent_chat_interface.md        # @agent 对话式协作方式
  jimeng_cli_integration.md      # 即梦 CLI 接入方式
agents/
  role_cards/core_team.md        # 核心角色卡
  specs/                         # 真 Agent runtime 的精细设定
  orchestration/                 # Orchestrator/runtime 配置草案
  workflows/cannes_10min_microfilm.yaml
ui/
  index.html                     # 轻量可视化流程界面
  moodboard.html                 # Moodboard MVP 工作台
schemas/
  artifacts.schema.json          # 过程产物结构
scripts/
  film_agent_team.py             # 本地实验脚手架
  moodboard_server.py            # Moodboard MVP 本地服务
examples/
  briefs/cannes_microfilm_brief.md
runs/
  # 每次实验生成在这里
```

## 快速开始

检查即梦 CLI：

```bash
python3 scripts/film_agent_team.py check-jimeng
```

初始化一次对照实验：

```bash
python3 scripts/film_agent_team.py init-run \
  --name cannes-test-001 \
  --brief examples/briefs/cannes_microfilm_brief.md
```

生成后会得到：

```text
runs/YYYYMMDD_HHMMSS_cannes-test-001/
  00_brief/
  01_single_agent/
  02_agent_team/
  03_jimeng/
  04_evaluation/
```

## 推荐验证方式

同一个创作 brief，跑两条链路：

- **Single Agent**：一个全能创作 agent 直接输出完整项目包。
- **Agent Team**：编剧、美术概念设计师、导演、粗/细分镜、制片人、剪辑、AI 演员演技指导、审片人、观众、Prompt Structurer、Prompt Compliance Reviewer 等角色分工协作，并引入 debate / critic / revision loop 与 human-in-the-loop。

然后用同一套评分表评估：

- 创意新颖度
- 剧本结构
- 角色弧光
- 视觉风格一致性
- 镜头语言专业度
- 分镜可执行性
- 即梦 prompt 可执行性
- 表演细腻度
- 剪辑节奏
- 观众记忆点
- 生成成本和迭代次数

## 轻量可视化

可以直接打开：

```text
ui/index.html
```

它展示 Agent Team 流程、人类参与点、提示词过审链路和 `@agent` 对话模板。第一阶段可以就在当前对话框里按 `@编剧`、`@导演`、`@审片人` 这种方式推进，不必先做复杂产品界面。

## Moodboard MVP

审美权重高的任务，不应该让 AI 先用一张生成图替用户决定想象。Moodboard MVP 用来先让 Agent 给关键镜头生成“寻图任务卡”，Human 把参考图放进本机文件夹并标注“只要站位 / 只要影调 / 远离”等判断，再让 Agent 抽取视觉规则。

启动：

```bash
python3 scripts/moodboard_server.py --port 8765
```

打开：

```text
http://127.0.0.1:8765/moodboard
```

使用说明见：

```text
docs/moodboard_mvp_runbook.md
```

## 当前定位

这是一个验证仓库。第一阶段先把流程、角色、产物、评分跑通；第二阶段再接具体 LLM / 多 Agent 框架 / 即梦 CLI 自动生成；第三阶段用真实成片和人工评审数据决定产品是否需要给 Agent Team 留入口。
