# Doubao Agent Team Runner

这是 **方案 B：豆包做 showrunner，豆包也做子 agent** 的本地 runner。

它不替换 Codex 本体。Codex 仍然负责改文件、跑命令、提交代码；这个 runner 负责调用豆包 / 火山方舟 API，让豆包分别扮演：

- Showrunner
- 反方编剧
- 观众
- 编剧

## 1. 配置密钥

复制示例配置：

```bash
cp .env.example .env
```

填写：

```bash
ARK_API_KEY=your_ark_api_key
ARK_BASE_URL=https://ark.cn-beijing.volces.com/api/v3
ARK_MODEL=your_doubao_model_id
ARK_SHOWRUNNER_MODEL=your_doubao_model_id
```

`.env` 已经被 `.gitignore` 忽略，不会提交到 GitHub。

## 2. Dry Run

Dry run 不会调用豆包，只写占位产物，用来检查路径和流程：

```bash
python3 scripts/agent_team_runner.py screenplay-review \
  --run runs/20260605_traffic_parasite \
  --dry-run
```

## 3. 真实调用豆包

```bash
python3 scripts/agent_team_runner.py screenplay-review \
  --run runs/20260605_traffic_parasite
```

默认输出到：

```text
runs/<run_name>/02_agent_team_doubao/
  agent_outputs/
    round0_showrunner_plan.md
    round1_opposition_review.md
    round1_audience_reaction.md
    round1_showrunner_synthesis.md
    round2_screenwriter_revision_notes.md
  drafts/
    revised_outline_v1.md
  run_manifest.json
```

## 4. 当前 workflow 做了什么

`screenplay-review` workflow 会按下面顺序调用豆包：

1. 豆包 Showrunner 读取原始 brief，产出 `round0_showrunner_plan.md`。
2. 豆包反方编剧读取 brief + showrunner plan，产出 `round1_opposition_review.md`。
3. 豆包观众读取 brief + showrunner plan，产出 `round1_audience_reaction.md`。
4. 豆包 Showrunner 综合两份评审，产出 `round1_showrunner_synthesis.md`。
5. 豆包编剧改稿，产出 `drafts/revised_outline_v1.md`。
6. 豆包编剧说明吸收了哪些意见，产出 `round2_screenwriter_revision_notes.md`。

## 5. 这个方案验证什么

它可以让我们比较：

```text
Single Agent
Codex showrunner + Codex sub-agents
Doubao showrunner + Doubao sub-agents
```

编排方法基本一致，但模型提供方变化。这样可以评估：效果提升到底来自 agent team 架构，还是来自某个底座模型。
