#!/usr/bin/env python3
"""Local scaffolding for AI microfilm agent-team experiments."""

from __future__ import annotations

import argparse
import datetime as dt
import re
import shutil
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUNS_DIR = ROOT / "runs"

RUBRIC = [
    "创意新颖度",
    "剧本结构",
    "角色弧光",
    "可拍性",
    "视觉风格",
    "镜头语言",
    "分镜可执行性",
    "Prompt 质量",
    "表演指导",
    "剪辑节奏",
    "观众理解",
    "记忆点",
    "首轮可用率",
    "迭代效率",
    "综合潜力",
]


def slugify(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9\u4e00-\u9fff]+", "-", value)
    value = value.strip("-")
    return value or "microfilm-run"


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def copy_brief(brief: Path, run_dir: Path) -> None:
    if brief.exists():
        shutil.copyfile(brief, run_dir / "00_brief" / "brief.md")
        return
    write_text(
        run_dir / "00_brief" / "brief.md",
        "# Brief\n\n在这里粘贴本轮 10 分钟微电影创作 brief。\n",
    )


def single_agent_template() -> str:
    return """# Single Agent Baseline Prompt

你是一个全能 AI 视频创作 Agent。请基于 `00_brief/brief.md`，一次性完成一支 10 分钟微电影项目包。

必须输出：

1. Logline
2. 人物与弧光
3. 10 分钟四段式结构
4. 完整剧本
5. 美术风格
6. 粗细分镜
7. 即梦可执行 prompts
8. 自评与修改建议

约束：

- 只讲一个核心事件。
- 主要角色不超过 3 个。
- 主要场景不超过 5 个。
- 不靠旁白解释主题。
- 结尾用画面展示变化。
"""


def agent_team_index() -> str:
    return """# Agent Team Workbench

按顺序填充本目录中的产物。每一步都要保留过程，不要只保留终稿。

## 推荐顺序

1. `01_concept_debate.md`
2. `02_project_bible.md`
3. `03_screenplay/`
4. `04_visual/`
5. `05_director/`
6. `06_storyboard/`
7. `07_production/`
8. `08_jimeng_prompts/`
9. `09_review/`

## 核心规则

- Showrunner 做最终取舍。
- 编剧室负责故事核和结构。
- 美术概念设计师负责视觉规则。
- 导演统一情绪、镜头和表演。
- 分镜师把意图变成可生成 shot spec。
- 审片人必须指出问题归因和下一轮修改 brief。
"""


def rubric_table() -> str:
    rows = [
        "| 维度 | Single Agent 1-5 | Agent Team 1-5 | 差值 | 证据 / 备注 |",
        "|---|---:|---:|---:|---|",
    ]
    rows.extend(f"| {item} |  |  |  |  |" for item in RUBRIC)
    return "# A/B Evaluation Rubric\n\n" + "\n".join(rows) + "\n"


def jimeng_command_template() -> str:
    return """# Jimeng Commands

把即梦 CLI 命令和生成记录写在这里。

建议每条记录包含：

```text
shot_id:
prompt_version:
command:
output_path:
usable: yes/no
failure_reason:
next_revision:
```
"""


def init_run(args: argparse.Namespace) -> None:
    timestamp = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
    run_name = f"{timestamp}_{slugify(args.name)}"
    run_dir = RUNS_DIR / run_name

    folders = [
        "00_brief",
        "01_single_agent",
        "02_agent_team/03_screenplay",
        "02_agent_team/04_visual",
        "02_agent_team/05_director",
        "02_agent_team/06_storyboard",
        "02_agent_team/07_production",
        "02_agent_team/08_jimeng_prompts",
        "02_agent_team/09_review",
        "03_jimeng/prompts",
        "03_jimeng/jimeng_outputs",
        "04_evaluation",
    ]
    for folder in folders:
        (run_dir / folder).mkdir(parents=True, exist_ok=False)

    copy_brief(Path(args.brief), run_dir)
    write_text(run_dir / "README.md", run_readme(run_name))
    write_text(run_dir / "01_single_agent" / "baseline_prompt.md", single_agent_template())
    write_text(run_dir / "02_agent_team" / "README.md", agent_team_index())
    write_text(run_dir / "03_jimeng" / "commands.md", jimeng_command_template())
    write_text(run_dir / "04_evaluation" / "rubric.md", rubric_table())
    write_text(run_dir / "04_evaluation" / "cost_log.md", cost_log_template())

    print(f"Created run: {run_dir}")


def run_readme(run_name: str) -> str:
    return f"""# Run {run_name}

本轮实验目标：同一个 brief 下，对比 Single Agent 与 Agent Team 的过程产物和最终生成效果。

## 路径

- `00_brief/brief.md`: 固定输入
- `01_single_agent/`: 单 Agent 基线
- `02_agent_team/`: 多角色制作组流程
- `03_jimeng/`: 即梦 prompt、命令、生成结果
- `04_evaluation/`: 评分、成本、结论

## 结论要求

最终结论不要只写“Agent Team 更好”。必须写清：

- 哪些维度更好
- 哪些维度没有明显差异
- 多出来的成本是什么
- 哪些过程产物最有产品价值
- 是否建议产品保留入口
"""


def cost_log_template() -> str:
    return """# Cost Log

| Item | Single Agent | Agent Team | Notes |
|---|---:|---:|---|
| Prompt / token cost |  |  |  |
| Human review time |  |  |  |
| Jimeng generations |  |  |  |
| Usable first-pass clips |  |  |  |
| Revision rounds |  |  |  |
| Total time |  |  |  |
"""


def check_jimeng(_: argparse.Namespace) -> None:
    candidates = ["jimeng", "dreamina", "jimeng-cli"]
    found = []
    for name in candidates:
        path = shutil.which(name)
        if path:
            found.append((name, path))

    if not found:
        print("No Jimeng/Dreamina CLI found in PATH.")
        print("Install with: curl -s https://jimeng.jianying.com/cli | bash")
        return

    for name, path in found:
        print(f"Found {name}: {path}")
        try:
            result = subprocess.run(
                [path, "--help"],
                check=False,
                text=True,
                capture_output=True,
                timeout=10,
            )
        except Exception as exc:  # pragma: no cover - diagnostic only
            print(f"  Could not run --help: {exc}")
            continue
        output = (result.stdout or result.stderr).strip()
        if output:
            print(output.splitlines()[0][:200])
        else:
            print("  CLI ran but returned no help text.")


def main() -> None:
    parser = argparse.ArgumentParser(description="AI microfilm agent-team experiment helper")
    sub = parser.add_subparsers(required=True)

    init = sub.add_parser("init-run", help="Create a new A/B experiment run folder")
    init.add_argument("--name", required=True, help="Human-readable run name")
    init.add_argument(
        "--brief",
        default=str(ROOT / "examples" / "briefs" / "cannes_microfilm_brief.md"),
        help="Path to the fixed creative brief",
    )
    init.set_defaults(func=init_run)

    check = sub.add_parser("check-jimeng", help="Check whether Jimeng/Dreamina CLI is installed")
    check.set_defaults(func=check_jimeng)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
