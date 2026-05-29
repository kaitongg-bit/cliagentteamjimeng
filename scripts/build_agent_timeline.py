#!/usr/bin/env python3
"""Build a static HTML timeline of the Dinggao agent-team artifacts."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_RUN = ROOT / "runs" / "20260527_194857_invisible-bullying-world-trial"
DEFAULT_OUTPUT = ROOT / "ui" / "agent_timeline.html"


TIMELINE_SPEC = [
    ("00", "Human", "输入", "固定创作 brief", "00_brief/brief.md", "固定实验输入。"),
    ("00", "Human", "输入", "原始故事种子", "00_brief/user_story_seed.md", "用户提供的明星隐形霸凌事件种子。"),
    ("00", "Single Agent", "对照组", "Single Agent baseline prompt", "01_single_agent/baseline_prompt.md", "A/B 实验中的单 Agent 基线提示词，当前尚未正式跑完产物。"),
    ("01", "Showrunner", "概念辩论", "概念辩论总表", "02_agent_team/01_concept_debate.md", "第一轮把故事问题、辩论角色和取舍框起来。"),
    ("01", "编剧", "概念辩论", "编剧初始结果", "02_agent_team/agent_outputs/screenwriter_agent_result.md", "编剧 Agent 的首轮故事判断。"),
    ("01", "反方编剧", "概念辩论", "反方编剧初始结果", "02_agent_team/agent_outputs/opposition_writer_agent_result.md", "反方 Agent 对故事风险与偏向的挑战。"),
    ("01", "观众", "概念辩论", "观众初始反馈", "02_agent_team/agent_outputs/audience_agent_result.md", "观众 Agent 对理解、站队和记忆点的首轮反馈。"),
    ("02", "编剧", "剧本结构", "第二轮剧本结构", "02_agent_team/agent_outputs/round2_screenwriter_structure.md", "确立剪辑师许临作为主角后的结构推进。"),
    ("03", "Human", "关键介入", "剪辑师揭示灵感", "02_agent_team/human_notes/editor_reveal_idea.md", "Human 提出结尾揭示：观众看到的故事也是剪出来的。"),
    ("03", "编剧", "关键介入反馈", "剪辑师揭示：编剧反馈", "02_agent_team/agent_outputs/editor_reveal_screenwriter_feedback.md", "编剧 Agent 吸收剪辑师主角/揭示结构。"),
    ("03", "反方编剧", "关键介入反馈", "剪辑师揭示：反方反馈", "02_agent_team/agent_outputs/editor_reveal_opposition_feedback.md", "反方 Agent 检查形式反转是否伤害主题。"),
    ("03", "观众", "关键介入反馈", "剪辑师揭示：观众反馈", "02_agent_team/agent_outputs/editor_reveal_audience_feedback.md", "观众 Agent 判断反转是否可理解和有余味。"),
    ("03", "Showrunner", "综合取舍", "剪辑师揭示综合", "02_agent_team/editor_reveal_showrunner_synthesis.md", "Showrunner 聚合三方反馈并定方向。"),
    ("04", "Human", "关键介入", "先男明星有罪，再女明星有罪", "02_agent_team/human_notes/guilt_curve_male_then_female.md", "Human 明确站队曲线：先让观众觉得男明星有罪，再反转到女明星有罪。"),
    ("04", "编剧", "剧本密度", "第三轮场次密度", "02_agent_team/agent_outputs/round3_screenwriter_scene_beats_density.md", "编剧继续填 10 分钟体量与场次节拍。"),
    ("04", "Human", "关键介入", "10 分钟密度疑问", "02_agent_team/human_notes/runtime_density_question.md", "Human 质疑内容是否能撑满 10 分钟，触发环境与动作补充。"),
    ("05", "编剧", "剧本草稿", "第四轮：场景 1-2", "02_agent_team/agent_outputs/round4_screenwriter_scene1_2_draft.md", "前两场剧本草稿。"),
    ("06", "编剧", "剧本草稿", "第五轮：场景 3-4", "02_agent_team/agent_outputs/round5_screenwriter_scene3_4_draft.md", "中段剪辑与舆论推进。"),
    ("07", "编剧", "剧本修正", "第六轮：女方责任再平衡", "02_agent_team/agent_outputs/round6_scene4_rebalance_female_guilt.md", "Human 提醒不要把女明星写得完全无辜后的修正。"),
    ("08", "观众", "阶段审片", "第七轮：观众反馈 1-4 场", "02_agent_team/agent_outputs/round7_audience_feedback_on_scenes1_4.md", "观众 Agent 对前四场可理解性和站队风险的反馈。"),
    ("08", "反方编剧", "阶段审片", "第七轮：反方反馈 1-4 场", "02_agent_team/agent_outputs/round7_opposition_feedback_on_scenes1_4.md", "反方 Agent 对倾斜和剧本风险的挑战。"),
    ("08", "Showrunner", "综合取舍", "第七轮综合", "02_agent_team/round7_showrunner_synthesis.md", "Showrunner 汇总前四场问题和下一轮 brief。"),
    ("09", "编剧", "剧本草稿", "第八轮：场景 5-7", "02_agent_team/agent_outputs/round8_screenwriter_scene5_7_draft.md", "剩余场次草稿。"),
    ("10", "编剧", "完整剧本", "完整剧本 1-7 场", "02_agent_team/drafts/dinggao_full_script_scenes1_7_round9.md", "当前最完整的剧本草稿。"),
    ("11", "审片人", "完整审片", "第九轮：审片人反馈", "02_agent_team/agent_outputs/round9_reviewer_feedback_on_full_script.md", "审片人对完整剧本的问题分类与质量判断。"),
    ("11", "导演", "完整审片", "第九轮：导演反馈", "02_agent_team/agent_outputs/round9_director_feedback_on_full_script.md", "导演 Agent 对场面调度、视觉母题和节奏的反馈。"),
    ("11", "Showrunner", "综合取舍", "第九轮综合", "02_agent_team/round9_showrunner_synthesis_full_script_review.md", "Showrunner 聚合导演与审片人反馈。"),
    ("12", "粗分镜师", "分镜", "第十轮：粗分镜", "03_storyboards/round10_rough_storyboard_v1.md", "将剧本转成镜头节拍与关键镜头。"),
    ("13", "美术概念", "视觉", "第十一轮：视觉圣经", "04_visual_concept/round11_visual_bible_v1.md", "美术概念与 Human 校准后的视觉规则。"),
    ("14", "Prompt Structurer", "即梦", "第十二轮：低质量真实概念图提示词", "03_jimeng/prompts/round12_low_quality_real_concept_images.md", "Prompt Agent 把视觉方向转成即梦概念图提示词。"),
    ("14", "工具执行", "即梦", "第十二轮：即梦命令", "03_jimeng/commands_round12_concept_images.md", "即梦 CLI 命令记录。"),
    ("14", "工具执行", "即梦", "第十二轮：生成记录", "03_jimeng/generation_log_round12_low_quality_real_concepts.md", "概念图生成结果和 Showrunner 读片。"),
    ("14", "Prompt Structurer", "即梦", "Prompt Ledger", "03_jimeng/prompt_ledger.md", "提示词公开账本，记录 prompt 自审、人类反馈和改法。"),
    ("15", "Showrunner", "Moodboard", "Moodboard 任务卡", "05_moodboard/reference_cards.yaml", "Human 找图前的关键镜头寻图任务卡。"),
    ("15", "Human", "Moodboard", "Human 参考图标注", "05_moodboard/moodboard_items.json", "Human 给参考图绑定任务卡、标签和备注。"),
    ("15", "Showrunner", "Moodboard", "Moodboard 自动总结", "05_moodboard/moodboard_synthesis.md", "从 Human 标签生成的结构化总结。"),
    ("16", "Showrunner", "Moodboard", "Moodboard Round 1 解读", "05_moodboard/moodboard_reference_read_round1.md", "把 Human 找来的图翻译成镜头、空间、影调、prompt 规则。"),
    ("17", "评估", "评分", "A/B 评分表", "04_evaluation/rubric.md", "Single Agent vs Agent Team 的正式评分表。"),
    ("17", "评估", "成本", "成本记录表", "04_evaluation/cost_log.md", "记录 token、Human 时间、生成次数和返工轮数。"),
]


AGENT_COLORS = {
    "Human": "human",
    "Showrunner": "showrunner",
    "编剧": "writer",
    "反方编剧": "opposition",
    "观众": "audience",
    "导演": "director",
    "审片人": "critic",
    "粗分镜师": "storyboard",
    "美术概念": "visual",
    "Prompt Structurer": "prompt",
    "工具执行": "tool",
    "Single Agent": "single",
    "评估": "eval",
}


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def content_excerpt(text: str) -> str:
    stripped = "\n".join(line.strip() for line in text.splitlines() if line.strip())
    return stripped[:220] + ("..." if len(stripped) > 220 else "")


def build_items(run_dir: Path, include_content: bool = False) -> list[dict]:
    items = []
    for index, (round_id, agent, stage, title, rel_path, note) in enumerate(TIMELINE_SPEC, start=1):
        path = run_dir / rel_path
        if not path.exists():
            continue
        content = read_text(path)
        item = {
            "index": index,
            "round": round_id,
            "agent": agent,
            "agentClass": AGENT_COLORS.get(agent, "default"),
            "stage": stage,
            "title": title,
            "path": path.relative_to(ROOT).as_posix(),
            "note": note,
            "excerpt": content_excerpt(content),
            "extension": path.suffix.lower().lstrip("."),
            "size": len(content),
        }
        if include_content:
            item["content"] = content
        items.append(item)
    return items


def timeline_payload(items: list[dict], run_dir: Path) -> dict:
    return {
        "project": "《定稿》",
        "run": run_dir.name,
        "items": items,
        "agents": sorted({item["agent"] for item in items}),
        "stages": sorted({item["stage"] for item in items}),
    }


def render_html() -> str:
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>《定稿》Agent Team 时间线</title>
  <style>
    :root {{
      --bg: #f5f6f8;
      --panel: #ffffff;
      --ink: #202532;
      --muted: #667085;
      --line: #d9dee8;
      --soft: #eef1f5;
      --blue: #2457c5;
      --human: #9a6a13;
      --showrunner: #2457c5;
      --writer: #137a63;
      --opposition: #b33a3a;
      --audience: #6b4cb3;
      --director: #255f85;
      --critic: #8f3d3d;
      --visual: #3f7d57;
      --prompt: #7447a6;
      --tool: #5d6678;
      --eval: #3f4b5f;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      background: var(--bg);
      color: var(--ink);
      font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      line-height: 1.5;
    }}
    header {{
      position: sticky;
      top: 0;
      z-index: 5;
      display: grid;
      grid-template-columns: minmax(0, 1fr) auto;
      gap: 18px;
      align-items: center;
      padding: 18px 22px;
      border-bottom: 1px solid var(--line);
      background: rgba(255,255,255,0.96);
      backdrop-filter: blur(8px);
    }}
    h1 {{
      margin: 0;
      font-size: 22px;
      letter-spacing: 0;
    }}
    .subtitle {{
      margin: 4px 0 0;
      color: var(--muted);
      font-size: 13px;
    }}
    .toolbar {{
      display: flex;
      gap: 8px;
      align-items: center;
      flex-wrap: wrap;
      justify-content: flex-end;
    }}
    input, select, button {{
      border: 1px solid var(--line);
      border-radius: 7px;
      background: var(--panel);
      color: var(--ink);
      font: inherit;
      font-size: 13px;
      padding: 8px 10px;
    }}
    button {{
      cursor: pointer;
    }}
    main {{
      display: grid;
      grid-template-columns: 270px minmax(420px, 1fr) 42%;
      min-height: calc(100vh - 78px);
    }}
    aside, section {{
      min-width: 0;
    }}
    .filters {{
      padding: 14px;
      border-right: 1px solid var(--line);
      background: #eef1f5;
      max-height: calc(100vh - 78px);
      overflow: auto;
    }}
    .timeline {{
      padding: 18px;
      max-height: calc(100vh - 78px);
      overflow: auto;
    }}
    .detail {{
      border-left: 1px solid var(--line);
      background: var(--panel);
      max-height: calc(100vh - 78px);
      overflow: auto;
    }}
    .panel-title {{
      margin: 0 0 10px;
      color: var(--muted);
      font-size: 12px;
      font-weight: 700;
      letter-spacing: 0.04em;
      text-transform: uppercase;
    }}
    .filter-group {{
      display: grid;
      gap: 7px;
      margin-bottom: 18px;
    }}
    .filter-button {{
      width: 100%;
      display: flex;
      justify-content: space-between;
      gap: 8px;
      text-align: left;
      background: var(--panel);
    }}
    .filter-button.active {{
      border-color: var(--blue);
      outline: 2px solid rgba(36, 87, 197, 0.16);
    }}
    .count {{
      color: var(--muted);
    }}
    .summary-grid {{
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 10px;
      margin-bottom: 14px;
    }}
    .summary-box {{
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 10px;
      background: var(--panel);
    }}
    .summary-box strong {{
      display: block;
      font-size: 20px;
    }}
    .summary-box span {{
      color: var(--muted);
      font-size: 12px;
    }}
    .timeline-list {{
      position: relative;
      display: grid;
      gap: 12px;
    }}
    .item {{
      display: grid;
      grid-template-columns: 54px minmax(0, 1fr);
      gap: 12px;
      cursor: pointer;
    }}
    .round {{
      display: flex;
      justify-content: center;
      align-items: flex-start;
      padding-top: 8px;
      color: var(--muted);
      font-size: 12px;
      font-weight: 700;
    }}
    .card {{
      border: 1px solid var(--line);
      border-left-width: 5px;
      border-radius: 8px;
      background: var(--panel);
      padding: 12px;
    }}
    .item.selected .card {{
      border-color: var(--blue);
      outline: 2px solid rgba(36, 87, 197, 0.16);
    }}
    .card.human {{ border-left-color: var(--human); }}
    .card.showrunner {{ border-left-color: var(--showrunner); }}
    .card.writer {{ border-left-color: var(--writer); }}
    .card.opposition {{ border-left-color: var(--opposition); }}
    .card.audience {{ border-left-color: var(--audience); }}
    .card.director {{ border-left-color: var(--director); }}
    .card.critic {{ border-left-color: var(--critic); }}
    .card.storyboard {{ border-left-color: var(--director); }}
    .card.visual {{ border-left-color: var(--visual); }}
    .card.prompt {{ border-left-color: var(--prompt); }}
    .card.tool {{ border-left-color: var(--tool); }}
    .card.single {{ border-left-color: #8a6a00; }}
    .card.eval {{ border-left-color: var(--eval); }}
    .meta {{
      display: flex;
      flex-wrap: wrap;
      gap: 6px;
      align-items: center;
      color: var(--muted);
      font-size: 12px;
      margin-bottom: 6px;
    }}
    .pill {{
      border: 1px solid var(--line);
      border-radius: 999px;
      padding: 2px 7px;
      background: #fff;
      color: var(--muted);
      font-size: 12px;
    }}
    h2 {{
      margin: 0 0 6px;
      font-size: 16px;
      letter-spacing: 0;
    }}
    .note, .excerpt {{
      margin: 0;
      color: var(--muted);
      font-size: 13px;
    }}
    .excerpt {{
      margin-top: 6px;
      color: #4d586b;
    }}
    .detail-head {{
      padding: 18px;
      border-bottom: 1px solid var(--line);
      background: #fbfcfe;
    }}
    .detail-head h2 {{
      font-size: 20px;
    }}
    .path {{
      margin-top: 10px;
      padding: 9px;
      border: 1px solid var(--line);
      border-radius: 7px;
      background: #fff;
      color: var(--muted);
      font-size: 12px;
      overflow-wrap: anywhere;
    }}
    .content {{
      padding: 18px;
    }}
    .markdown {{
      white-space: pre-wrap;
      overflow-wrap: anywhere;
      font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, "Liberation Mono", monospace;
      font-size: 13px;
      line-height: 1.55;
      background: #172033;
      color: #eef4ff;
      border-radius: 8px;
      padding: 14px;
    }}
    .empty {{
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 18px;
      color: var(--muted);
      background: var(--panel);
    }}
    .loading {{
      color: var(--muted);
      padding: 18px;
    }}
    .error {{
      color: #9a3412;
      background: #fff7ed;
      border-color: #fed7aa;
    }}
    @media (max-width: 1180px) {{
      main {{
        grid-template-columns: 240px minmax(0, 1fr);
      }}
      .detail {{
        grid-column: 1 / -1;
        border-left: 0;
        border-top: 1px solid var(--line);
        max-height: none;
      }}
    }}
    @media (max-width: 760px) {{
      header {{
        grid-template-columns: 1fr;
      }}
      main {{
        grid-template-columns: 1fr;
      }}
      .filters, .timeline, .detail {{
        max-height: none;
      }}
      .filters {{
        border-right: 0;
        border-bottom: 1px solid var(--line);
      }}
      .summary-grid {{
        grid-template-columns: 1fr;
      }}
    }}
  </style>
</head>
<body>
  <header>
    <div>
      <h1>《定稿》Agent Team 时间线</h1>
      <p class="subtitle">按真实推进顺序展示 Human、各 Agent、Showrunner、工具执行和评估产物。点开任意节点可查看原始文件。</p>
    </div>
    <div class="toolbar">
      <input id="searchInput" type="search" placeholder="搜索标题/agent/摘要">
      <select id="stageSelect"></select>
      <button id="resetButton" type="button">重置</button>
    </div>
  </header>

  <main>
    <aside class="filters">
      <p class="panel-title">Agent Filter</p>
      <div id="agentFilters" class="filter-group"></div>
      <p class="panel-title">说明</p>
      <p class="note">这个页面展示的是过程产物，不等同于评分结论。Single Agent 目前只有 baseline prompt，还没有完整对照产物。</p>
    </aside>
    <section class="timeline">
      <div class="summary-grid">
        <div class="summary-box"><strong id="totalCount">0</strong><span>过程节点</span></div>
        <div class="summary-box"><strong id="agentCount">0</strong><span>参与角色</span></div>
        <div class="summary-box"><strong id="visibleCount">0</strong><span>当前显示</span></div>
      </div>
      <div id="timelineList" class="timeline-list"></div>
    </section>
    <aside class="detail" id="detailPanel">
      <div class="empty">请选择一个时间线节点。</div>
    </aside>
  </main>

  <script>
    let data = {{ project: "《定稿》", run: "", items: [], agents: [], stages: [] }};
    const contentCache = new Map();
    const state = {{
      agent: "全部",
      stage: "全部",
      query: "",
      selectedIndex: null
    }};

    const agentFilters = document.getElementById("agentFilters");
    const stageSelect = document.getElementById("stageSelect");
    const searchInput = document.getElementById("searchInput");
    const timelineList = document.getElementById("timelineList");
    const detailPanel = document.getElementById("detailPanel");

    function escapeHtml(value) {{
      return String(value).replace(/[&<>"']/g, char => ({{
        "&": "&amp;",
        "<": "&lt;",
        ">": "&gt;",
        "\\"": "&quot;",
        "'": "&#039;"
      }}[char]));
    }}

    function countByAgent(agent) {{
      if (agent === "全部") return data.items.length;
      return data.items.filter(item => item.agent === agent).length;
    }}

    function showLoadError(message) {{
      timelineList.innerHTML = `<div class="empty error">${{escapeHtml(message)}}</div>`;
      detailPanel.innerHTML = `<div class="empty">时间线索引页需要通过本地服务打开：<br>http://127.0.0.1:8765/timeline</div>`;
    }}

    function setupFilters() {{
      const agents = ["全部", ...data.agents];
      agentFilters.innerHTML = "";
      agents.forEach(agent => {{
        const button = document.createElement("button");
        button.className = "filter-button";
        button.type = "button";
        button.dataset.agent = agent;
        button.innerHTML = `<span>${{escapeHtml(agent)}}</span><span class="count">${{countByAgent(agent)}}</span>`;
        button.addEventListener("click", () => {{
          state.agent = agent;
          render();
        }});
        agentFilters.appendChild(button);
      }});

      stageSelect.innerHTML = `<option value="全部">全部阶段</option>` + data.stages.map(stage => `<option value="${{escapeHtml(stage)}}">${{escapeHtml(stage)}}</option>`).join("");
      stageSelect.addEventListener("change", () => {{
        state.stage = stageSelect.value;
        render();
      }});
      searchInput.addEventListener("input", () => {{
        state.query = searchInput.value.trim().toLowerCase();
        render();
      }});
      document.getElementById("resetButton").addEventListener("click", () => {{
        state.agent = "全部";
        state.stage = "全部";
        state.query = "";
        searchInput.value = "";
        stageSelect.value = "全部";
        render();
      }});
    }}

    function visibleItems() {{
      return data.items.filter(item => {{
        if (state.agent !== "全部" && item.agent !== state.agent) return false;
        if (state.stage !== "全部" && item.stage !== state.stage) return false;
        if (!state.query) return true;
        const haystack = `${{item.title}} ${{item.agent}} ${{item.stage}} ${{item.path}} ${{item.note}} ${{item.excerpt}}`.toLowerCase();
        return haystack.includes(state.query);
      }});
    }}

    function renderTimeline(items) {{
      timelineList.innerHTML = "";
      if (!items.length) {{
        timelineList.innerHTML = `<div class="empty">没有匹配的产物。</div>`;
        return;
      }}
      items.forEach(item => {{
        const row = document.createElement("article");
        row.className = `item ${{item.index === state.selectedIndex ? "selected" : ""}}`;
        row.innerHTML = `
          <div class="round">R${{escapeHtml(item.round)}}</div>
          <div class="card ${{item.agentClass}}">
            <div class="meta">
              <span class="pill">${{escapeHtml(item.agent)}}</span>
              <span class="pill">${{escapeHtml(item.stage)}}</span>
              <span>${{escapeHtml(item.extension)}} · ${{item.size}} 字符</span>
            </div>
            <h2>${{escapeHtml(item.title)}}</h2>
            <p class="note">${{escapeHtml(item.note)}}</p>
            <p class="excerpt">${{escapeHtml(item.excerpt)}}</p>
          </div>
        `;
        row.addEventListener("click", async () => {{
          state.selectedIndex = item.index;
          render();
          await renderDetail();
        }});
        timelineList.appendChild(row);
      }});
    }}

    async function loadContent(item) {{
      if (contentCache.has(item.path)) return contentCache.get(item.path);
      const response = await fetch(`/api/artifact?path=${{encodeURIComponent(item.path)}}`);
      if (!response.ok) {{
        const error = await response.json().catch(() => ({{ error: "加载失败" }}));
        throw new Error(error.error || "加载失败");
      }}
      const payload = await response.json();
      const content = payload.content || "";
      contentCache.set(item.path, content);
      return content;
    }}

    async function renderDetail() {{
      const item = data.items.find(entry => entry.index === state.selectedIndex);
      if (!item) {{
        detailPanel.innerHTML = `<div class="empty">请选择一个时间线节点。页面只预加载索引，点开节点后才读取原始 md/json。</div>`;
        return;
      }}
      detailPanel.innerHTML = `
        <div class="detail-head">
          <div class="meta">
            <span class="pill">${{escapeHtml(item.agent)}}</span>
            <span class="pill">${{escapeHtml(item.stage)}}</span>
            <span class="pill">R${{escapeHtml(item.round)}}</span>
          </div>
          <h2>${{escapeHtml(item.title)}}</h2>
          <p class="note">${{escapeHtml(item.note)}}</p>
          <div class="path">${{escapeHtml(item.path)}}</div>
        </div>
        <div class="content">
          <div class="loading">正在加载这份过程产物...</div>
        </div>
      `;
      try {{
        const content = await loadContent(item);
        const contentNode = detailPanel.querySelector(".content");
        contentNode.innerHTML = `<pre class="markdown">${{escapeHtml(content)}}</pre>`;
      }} catch (error) {{
        const contentNode = detailPanel.querySelector(".content");
        contentNode.innerHTML = `<div class="empty error">${{escapeHtml(error.message)}}</div>`;
      }}
    }}

    function render() {{
      const items = visibleItems();
      document.getElementById("totalCount").textContent = data.items.length;
      document.getElementById("agentCount").textContent = data.agents.length;
      document.getElementById("visibleCount").textContent = items.length;
      [...agentFilters.children].forEach(button => {{
        button.classList.toggle("active", button.dataset.agent === state.agent);
      }});
      renderTimeline(items);
    }}

    async function boot() {{
      timelineList.innerHTML = `<div class="empty">正在读取 Agent Team 时间线索引...</div>`;
      try {{
        const response = await fetch("/api/timeline");
        if (!response.ok) throw new Error("没有读到时间线索引");
        data = await response.json();
        state.selectedIndex = data.items[0]?.index || null;
        setupFilters();
        render();
        await renderDetail();
      }} catch (error) {{
        showLoadError(error.message || "时间线加载失败");
      }}
    }}

    boot();
  </script>
</body>
</html>
"""


def main() -> None:
    parser = argparse.ArgumentParser(description="Build the Dinggao agent-team timeline HTML.")
    parser.add_argument("--run", default=str(DEFAULT_RUN), help="Run directory.")
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT), help="Output HTML path.")
    args = parser.parse_args()

    run_dir = Path(args.run)
    output = Path(args.output)
    items = build_items(run_dir, include_content=False)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_html(), encoding="utf-8")
    print(f"Wrote {output} with {len(items)} timeline items.")


if __name__ == "__main__":
    main()
