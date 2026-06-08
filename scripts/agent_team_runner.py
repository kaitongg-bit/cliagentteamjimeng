#!/usr/bin/env python3
"""Run a local screenplay-review agent team with Doubao as showrunner and agents.

This runner is intentionally small and file-based:
- reads role specs from agents/specs/*.yaml
- reads a single brief/outline file
- calls Doubao Ark for showrunner, opposition, audience, and screenwriter roles
- writes every artifact into the run directory for review and comparison
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import textwrap
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Optional

from providers.doubao_ark import ArkProviderError, DoubaoArkProvider


ROOT = Path(__file__).resolve().parents[1]
SPECS = ROOT / "agents" / "specs"


def load_dotenv(path: Path) -> None:
    if not path.exists():
        return
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def role_spec(role: str) -> str:
    return read_text(SPECS / f"{role}.yaml")


def clip(text: str, limit: int = 28000) -> str:
    if len(text) <= limit:
        return text
    return text[:limit] + "\n\n[TRUNCATED BY RUNNER]\n"


def display_path(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return str(path)


@dataclass
class StepRecord:
    step: str
    role: str
    model: str
    output: str
    latency_s: float
    usage: dict


class AgentTeamRunner:
    def __init__(
        self,
        *,
        run_dir: Path,
        brief_path: Path,
        output_dir: Path,
        model: str,
        showrunner_model: str,
        temperature: float,
        dry_run: bool,
    ) -> None:
        self.run_dir = run_dir
        self.brief_path = brief_path
        self.output_dir = output_dir
        self.model = model
        self.showrunner_model = showrunner_model
        self.temperature = temperature
        self.dry_run = dry_run
        self.agent_outputs = output_dir / "agent_outputs"
        self.drafts = output_dir / "drafts"
        self.records: list[StepRecord] = []
        self.provider = None if dry_run else DoubaoArkProvider()

    def call(
        self,
        *,
        step: str,
        role: str,
        model: str,
        system: str,
        user: str,
        output_path: Path,
        max_tokens: Optional[int] = None,
    ) -> str:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        if self.dry_run:
            content = textwrap.dedent(
                f"""\
                # DRY RUN - {step}

                Role: {role}
                Model: {model}
                Output path: {display_path(output_path)}

                This placeholder was written without calling Ark.
                """
            )
            write_text(output_path, content)
            self.records.append(StepRecord(step, role, model, str(output_path), 0.0, {}))
            return content

        assert self.provider is not None
        result = self.provider.chat(
            model=model,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            temperature=self.temperature,
            max_tokens=max_tokens,
        )
        write_text(output_path, result.content)
        self.records.append(
            StepRecord(step, role, result.model, str(output_path), result.latency_s, result.usage)
        )
        return result.content

    def write_manifest(self) -> None:
        payload = {
            "created_at": time.strftime("%Y-%m-%d %H:%M:%S"),
            "provider": "doubao_ark",
            "run_dir": str(self.run_dir),
            "brief_path": str(self.brief_path),
            "output_dir": str(self.output_dir),
            "model": self.model,
            "showrunner_model": self.showrunner_model,
            "dry_run": self.dry_run,
            "steps": [asdict(record) for record in self.records],
        }
        write_text(self.output_dir / "run_manifest.json", json.dumps(payload, ensure_ascii=False, indent=2))

    def screenplay_review(self) -> None:
        brief = clip(read_text(self.brief_path))
        showrunner_spec = role_spec("showrunner")
        opposition_spec = role_spec("opposition_writer")
        audience_spec = role_spec("audience_panel")
        screenwriter_spec = role_spec("screenwriter")

        showrunner_system = (
            "你是一个豆包驱动的 Agent Team Showrunner。"
            "你必须做动态创作总控、上下文隔离、取舍和可追溯决策。"
            "以下是你的角色设定：\n\n"
            f"{showrunner_spec}"
        )

        plan = self.call(
            step="round0_showrunner_plan",
            role="showrunner",
            model=self.showrunner_model,
            system=showrunner_system,
            user=textwrap.dedent(
                f"""\
                这是一个全新剧本评审 run。请不要引用任何历史故事。

                你将总控一个三步 agent team：
                1. 反方编剧评审；
                2. 观众评审；
                3. 编剧根据两份评审改写，并说明吸收了什么意见。

                请先产出本轮 Showrunner 评审计划，要求：
                - 判断这个 brief 最该被反方编剧检查的风险；
                - 判断这个 brief 最该被观众检查的体验问题；
                - 明确编剧改稿时不应丢掉的题材核心；
                - 明确输出路径和上下文隔离规则。

                原始 brief:
                {brief}
                """
            ),
            output_path=self.agent_outputs / "round0_showrunner_plan.md",
            max_tokens=2500,
        )

        opposition = self.call(
            step="round1_opposition_review",
            role="opposition_writer",
            model=self.model,
            system=(
                "你是反方编剧 agent。你只根据用户 brief 和 showrunner 计划评审，"
                "不要重写剧本。以下是你的角色设定：\n\n"
                f"{opposition_spec}"
            ),
            user=textwrap.dedent(
                f"""\
                请评审以下剧本梗概，重点找结构、可信度、俗套、价值风险和可执行修法。

                Showrunner 计划:
                {clip(plan, 10000)}

                原始 brief:
                {brief}

                输出要求：
                - 核心判断；
                - 最严重的 5 个问题，按严重程度排序；
                - 每个问题给具体修法；
                - 明确哪些地方必须保留。
                """
            ),
            output_path=self.agent_outputs / "round1_opposition_review.md",
            max_tokens=4500,
        )

        audience = self.call(
            step="round1_audience_reaction",
            role="audience_panel",
            model=self.model,
            system=(
                "你是观众 agent。你只根据用户 brief 和 showrunner 计划评审观看体验，"
                "不要重写剧本。以下是你的角色设定：\n\n"
                f"{audience_spec}"
            ),
            user=textwrap.dedent(
                f"""\
                请从普通观众、类型片观众、短视频传播观众、严肃/电影节观众四类视角，
                评价以下剧本梗概。

                Showrunner 计划:
                {clip(plan, 10000)}

                原始 brief:
                {brief}

                输出要求：
                - 0-10 分评分；
                - 哪里想继续看；
                - 哪里会出戏/划走；
                - 主角弧线是否能跟；
                - 结尾是否满足、是否说教；
                - 最希望编剧修改的 5 点。
                """
            ),
            output_path=self.agent_outputs / "round1_audience_reaction.md",
            max_tokens=4500,
        )

        synthesis = self.call(
            step="round1_showrunner_synthesis",
            role="showrunner",
            model=self.showrunner_model,
            system=showrunner_system,
            user=textwrap.dedent(
                f"""\
                请综合反方编剧和观众评审，给编剧 agent 一个明确改稿 brief。
                不要平均混合意见，请做取舍。

                原始 brief:
                {brief}

                反方编剧评审:
                {clip(opposition, 12000)}

                观众评审:
                {clip(audience, 12000)}

                输出要求：
                - 必须保留什么；
                - 必须修正什么；
                - 可以不吸收什么以及原因；
                - 编剧下一版交付格式。
                """
            ),
            output_path=self.agent_outputs / "round1_showrunner_synthesis.md",
            max_tokens=3500,
        )

        revised = self.call(
            step="round2_screenwriter_revision",
            role="screenwriter",
            model=self.model,
            system=(
                "你是编剧 agent。请根据原始 brief、两份评审和 showrunner synthesis 改写。"
                "不要写完整台词剧本，交付更强的长片剧情梗概/分段大纲。"
                "以下是你的角色设定：\n\n"
                f"{screenwriter_spec}"
            ),
            user=textwrap.dedent(
                f"""\
                请改写原始梗概。必须保留题材核心，但吸收评审意见。

                原始 brief:
                {brief}

                反方编剧评审:
                {clip(opposition, 10000)}

                观众评审:
                {clip(audience, 10000)}

                Showrunner 综合:
                {clip(synthesis, 10000)}

                输出要求：
                - 标题；
                - 核心改写方向；
                - 主要人物关系；
                - 按 10-15 分钟段落重写完整长片梗概；
                - 结尾必须用行动和画面表达，不靠主题口号。
                """
            ),
            output_path=self.drafts / "revised_outline_v1.md",
            max_tokens=7000,
        )

        self.call(
            step="round2_screenwriter_revision_notes",
            role="screenwriter",
            model=self.model,
            system=(
                "你是编剧 agent。请只写本轮改稿吸收说明，必须具体、可追溯。"
                "以下是你的角色设定：\n\n"
                f"{screenwriter_spec}"
            ),
            user=textwrap.dedent(
                f"""\
                请说明你在 revised_outline_v1.md 中吸收了哪些意见。

                反方编剧评审:
                {clip(opposition, 10000)}

                观众评审:
                {clip(audience, 10000)}

                Showrunner 综合:
                {clip(synthesis, 10000)}

                改写稿:
                {clip(revised, 16000)}

                输出要求：
                - 来自反方编剧的意见：已吸收哪些；
                - 来自观众 agent 的意见：已吸收哪些；
                - 来自 showrunner 的取舍：如何执行；
                - 没有吸收哪些意见以及原因；
                - 本轮最大改动一句话。
                """
            ),
            output_path=self.agent_outputs / "round2_screenwriter_revision_notes.md",
            max_tokens=4500,
        )

        self.write_manifest()


def default_brief(run_dir: Path) -> Path:
    candidates = [
        run_dir / "00_brief" / "jimeng_outline.md",
        run_dir / "00_brief" / "user_story_seed.md",
        run_dir / "00_brief" / "brief.md",
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return candidates[0]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run local agent-team workflows with Doubao Ark.")
    parser.add_argument("--env", default=str(ROOT / ".env"), help="Path to .env file.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    run = subparsers.add_parser("screenplay-review", help="Run showrunner + opposition + audience + screenwriter.")
    run.add_argument("--run", required=True, help="Run directory.")
    run.add_argument("--brief", help="Brief/outline file. Defaults to 00_brief/jimeng_outline.md.")
    run.add_argument("--output-dir", help="Output directory. Defaults to <run>/02_agent_team_doubao.")
    run.add_argument("--model", default=os.getenv("ARK_MODEL", "doubao-seed-2-0-lite-260215"))
    run.add_argument("--showrunner-model", default=os.getenv("ARK_SHOWRUNNER_MODEL") or os.getenv("ARK_MODEL", "doubao-seed-2-0-lite-260215"))
    run.add_argument("--temperature", type=float, default=0.35)
    run.add_argument("--dry-run", action="store_true", help="Write placeholders without calling Ark.")
    return parser


def main(argv: Optional[list[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    load_dotenv(Path(args.env).expanduser())

    if args.command == "screenplay-review":
        run_dir = Path(args.run).expanduser()
        if not run_dir.is_absolute():
            run_dir = ROOT / run_dir
        run_dir = run_dir.resolve()
        brief_path = Path(args.brief).expanduser() if args.brief else default_brief(run_dir)
        if not brief_path.is_absolute():
            brief_path = (ROOT / brief_path).resolve()
        output_dir = Path(args.output_dir).expanduser() if args.output_dir else run_dir / "02_agent_team_doubao"
        if not output_dir.is_absolute():
            output_dir = (ROOT / output_dir).resolve()

        if not brief_path.exists():
            parser.error(f"Brief file not found: {brief_path}")
        if not args.dry_run and not os.getenv("ARK_API_KEY"):
            parser.error("Missing ARK_API_KEY. Copy .env.example to .env and fill it, or use --dry-run.")

        runner = AgentTeamRunner(
            run_dir=run_dir,
            brief_path=brief_path,
            output_dir=output_dir,
            model=args.model,
            showrunner_model=args.showrunner_model,
            temperature=args.temperature,
            dry_run=args.dry_run,
        )
        runner.screenplay_review()
        print(f"Wrote Doubao agent-team outputs to {output_dir}")
        return 0

    return 1


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ArkProviderError as exc:
        print(f"Ark error: {exc}", file=sys.stderr)
        raise SystemExit(2)
