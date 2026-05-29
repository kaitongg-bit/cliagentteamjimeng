#!/usr/bin/env python3
"""Local Moodboard MVP server for the microfilm agent-team workspace."""

from __future__ import annotations

import argparse
import base64
import datetime as dt
import json
import mimetypes
import re
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlparse

from build_agent_timeline import build_items, timeline_payload


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_RUN = ROOT / "runs" / "20260527_194857_invisible-bullying-world-trial"
IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".webp"}
ARTIFACT_EXTS = {".md", ".json", ".yaml", ".yml", ".txt", ".csv"}

DEFAULT_CARDS = [
    {
        "card_id": "MB_001",
        "scene_id": "S01",
        "shot_name": "从门口看见许临在电脑前",
        "status": "unresolved",
        "dramatic_function": "第一次证明他不是操盘手，而是被生活压住的人。",
        "viewer_should_feel": "房间比人更有力量，人像被空间吞掉。",
        "look_for": ["门口视角", "狭小房间纵深", "背对镜头的人", "电脑屏幕作为实际光源", "正常当代显示器或 MacBook"],
        "avoid": ["赛博朋克剪辑室", "复古 CRT 电脑", "漂亮的电影化贫穷", "极端破败或漏水苦难", "年代戏感"],
        "suggested_search_terms": {
            "zh": ["上海里弄老旧小区 出租屋 电脑桌", "一线城市 老小区 单间 MacBook 工作", "屏幕光 背影 出租屋"],
            "en": ["old urban apartment room laptop desk screen light", "messy lived-in apartment laptop work desk"],
        },
        "reference_targets": [
            {"title": "纪录片式出租屋/打工人影像", "watch_for": "空间如何压过人物，而不是人物摆拍。"},
            {"title": "《宇宙探索编辑部》式生活质感", "watch_for": "普通旧空间、偏冷影调、湿闷但不卖惨的质感。"},
        ],
        "human_notes": "",
    },
    {
        "card_id": "MB_002",
        "scene_id": "S01",
        "shot_name": "不打理的工作台：桌面、线缆、屏幕反光",
        "status": "unresolved",
        "dramatic_function": "把失业处境和剪辑劳动压缩进一个长期无人整理的生活/工作混合空间。",
        "viewer_should_feel": "不是穷苦奇观，而是一个人被工作和生活慢慢堆住。",
        "look_for": ["正常电脑或 MacBook", "桌面杂物层次", "线缆和充电器", "外卖/纸张/硬盘", "屏幕反光"],
        "avoid": ["惊悚片电火花", "过度戏剧化漏水", "摆拍道具清单", "复古电脑房", "极端贫穷化"],
        "suggested_search_terms": {
            "zh": ["出租屋 电脑桌 杂物 MacBook", "老小区单间 工作台 生活杂物", "剪辑师 房间 电脑桌"],
            "en": ["lived in apartment laptop desk clutter", "freelance editor messy desk apartment"],
        },
        "reference_targets": [{"title": "真实居住工作台照片", "watch_for": "东西如何自然堆积，不要故意摆乱。"}],
        "human_notes": "",
    },
    {
        "card_id": "MB_003",
        "scene_id": "S02",
        "shot_name": "剪辑屏幕制造第一轮“男明星有罪”叙事",
        "status": "unresolved",
        "dramatic_function": "让观众意识到立场来自剪辑，而不是事实本身。",
        "viewer_should_feel": "屏幕比人更像施暴者。",
        "look_for": ["屏摄质感", "剪辑软件界面", "标题遮脸", "人物脸部反光", "信息过载但不可读"],
        "avoid": ["真实平台 Logo", "真实明星脸", "长段可读文字", "黑客房间"],
        "suggested_search_terms": {
            "zh": ["剪辑软件 屏幕 背影", "电脑屏摄 时间线 人脸反光", "视频剪辑 工作台"],
            "en": ["editing software screen over shoulder", "video timeline screen reflection face"],
        },
        "reference_targets": [{"title": "幕后剪辑工作照", "watch_for": "屏幕如何成为光源和叙事机器。"}],
        "human_notes": "",
    },
    {
        "card_id": "MB_004",
        "scene_id": "S03",
        "shot_name": "外卖骑手在雨夜看竖屏舆论视频",
        "status": "unresolved",
        "dramatic_function": "把网络审判从房间扩散到普通劳动者的等待时间里。",
        "viewer_should_feel": "舆论不是抽象热搜，而是进入每个疲惫缝隙。",
        "look_for": ["雨棚下的等待", "手机支架竖屏", "湿反光地面", "骑手和屏幕比例", "普通小区门口"],
        "avoid": ["品牌 Logo", "英雄化骑手", "广告片质感", "漂亮霓虹"],
        "suggested_search_terms": {
            "zh": ["外卖骑手 雨夜 小区门口 手机", "雨棚 电动车 手机支架", "雨夜 小区门口 外卖"],
            "en": ["delivery rider rain phone mount residential gate", "rainy night scooter phone screen"],
        },
        "reference_targets": [{"title": "短视频/新闻里的雨夜骑手", "watch_for": "廉价公共光和等待姿态。"}],
        "human_notes": "",
    },
    {
        "card_id": "MB_005",
        "scene_id": "S04",
        "shot_name": "电梯走廊：道歉涂鸦和广告脸",
        "status": "unresolved",
        "dramatic_function": "让线上道德要求污染线下公共空间。",
        "viewer_should_feel": "便宜广告和道歉两个词把人压扁。",
        "look_for": ["老旧电梯间", "墙面小广告残胶", "广告脸", "手写涂鸦", "荧光灯"],
        "avoid": ["恐怖片走廊", "高级美术馆墙面", "真实品牌", "太干净"],
        "suggested_search_terms": {
            "zh": ["旧小区 电梯间 广告 墙面", "电梯走廊 小广告 涂鸦", "老楼道 荧光灯"],
            "en": ["old apartment elevator lobby advertisement wall", "cheap elevator hallway fluorescent"],
        },
        "reference_targets": [{"title": "老旧小区电梯间照片", "watch_for": "公共空间的脏、旧、临时感。"}],
        "human_notes": "",
    },
    {
        "card_id": "MB_006",
        "scene_id": "S05",
        "shot_name": "父亲餐饮店被差评流冲击",
        "status": "unresolved",
        "dramatic_function": "把娱乐舆论转化为真实家庭经济损伤。",
        "viewer_should_feel": "被惩罚的人甚至不在原事件里。",
        "look_for": ["小餐饮店门脸", "收银台", "老人/父亲姿态", "手机评价界面反光", "冷清饭点"],
        "avoid": ["苦情剧", "夸张砸店", "豪华餐厅", "煽情特写"],
        "suggested_search_terms": {
            "zh": ["小餐馆 收银台 老板 手机 评价", "街边餐饮店 冷清 雨天", "餐馆 差评 手机"],
            "en": ["small restaurant owner phone review empty dining", "family restaurant counter rain night"],
        },
        "reference_targets": [{"title": "街边小餐饮纪录照片", "watch_for": "经营压力，不要戏剧控诉。"}],
        "human_notes": "",
    },
    {
        "card_id": "MB_007",
        "scene_id": "S06",
        "shot_name": "廉价屏幕上的公共舆论蒙太奇",
        "status": "unresolved",
        "dramatic_function": "显示舆论如何通过各种廉价屏幕复制自己。",
        "viewer_should_feel": "世界不是在讨论真相，而是在同步一种表情。",
        "look_for": ["公交/电梯/餐馆/出租屋屏幕", "竖屏视频", "低清压缩", "屏幕反光", "人群不看镜头"],
        "avoid": ["未来城市屏幕墙", "科技感数据流", "宏大社会隐喻", "过度设计"],
        "suggested_search_terms": {
            "zh": ["手机屏幕 人群 低清", "公交 乘客 手机 视频", "餐馆 电视 手机 短视频"],
            "en": ["cheap screen public video montage", "people watching phones low quality screen"],
        },
        "reference_targets": [{"title": "公共场所手机观看照片", "watch_for": "舆论如何寄生在小屏幕。"}],
        "human_notes": "",
    },
    {
        "card_id": "MB_008",
        "scene_id": "S07",
        "shot_name": "最终空房间：人离开，系统还在同步",
        "status": "unresolved",
        "dramatic_function": "结尾让观众发现机器/流程比人更持久。",
        "viewer_should_feel": "不是反转炫技，而是冷掉：人退场，生产继续。",
        "look_for": ["空椅子", "还亮着的电脑或 MacBook", "清晨灰光", "未收拾的桌面", "房间无人但仍运行"],
        "avoid": ["恐怖空房", "科幻 AI 接管", "诗意过度", "完美构图"],
        "suggested_search_terms": {
            "zh": ["空房间 电脑 亮着 清晨", "出租屋 空椅子 电脑", "雨后 房间 电脑桌"],
            "en": ["empty room computer still on morning", "abandoned desk computer screen rain"],
        },
        "reference_targets": [{"title": "空工作间/空出租屋照片", "watch_for": "人不在，但劳动痕迹还在。"}],
        "human_notes": "",
    },
]

TAG_OPTIONS = [
    "靠近",
    "远离",
    "只要站位",
    "只要空间",
    "只要景别",
    "只要影调",
    "只要光线",
    "只要质感",
    "只要人物距离",
    "危险但有一点可学",
]


def safe_filename(name: str) -> str:
    stem = Path(name).stem.strip() or "image"
    suffix = Path(name).suffix.lower()
    stem = re.sub(r"[^A-Za-z0-9._\-\u4e00-\u9fff]+", "_", stem).strip("._")
    if suffix not in IMAGE_EXTS:
        suffix = ".png"
    return f"{stem[:80]}{suffix}"


def read_json(path: Path, fallback):
    if not path.exists():
        return fallback
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return fallback


def write_json(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def card_yaml(cards: list[dict]) -> str:
    lines = ["cards:"]
    for card in cards:
        lines.append(f"  - card_id: {card['card_id']}")
        lines.append(f"    scene_id: {card['scene_id']}")
        lines.append(f"    shot_name: {card['shot_name']}")
        lines.append(f"    status: {card.get('status', 'unresolved')}")
        lines.append(f"    dramatic_function: {card['dramatic_function']}")
        lines.append(f"    viewer_should_feel: {card['viewer_should_feel']}")
        lines.append("    look_for:")
        lines.extend(f"      - {item}" for item in card.get("look_for", []))
        lines.append("    avoid:")
        lines.extend(f"      - {item}" for item in card.get("avoid", []))
        lines.append("    suggested_search_terms:")
        lines.append("      zh:")
        lines.extend(f"        - {item}" for item in card.get("suggested_search_terms", {}).get("zh", []))
        lines.append("      en:")
        lines.extend(f"        - {item}" for item in card.get("suggested_search_terms", {}).get("en", []))
        lines.append(f"    human_notes: {card.get('human_notes', '')}")
    return "\n".join(lines) + "\n"


class MoodboardStore:
    def __init__(self, run_dir: Path):
        self.run_dir = run_dir.resolve()
        self.board_dir = self.run_dir / "05_moodboard"
        self.inbox_dir = self.board_dir / "inbox"
        self.accepted_dir = self.board_dir / "accepted"
        self.rejected_dir = self.board_dir / "rejected"
        self.exports_dir = self.board_dir / "exports"
        self.cards_path = self.board_dir / "reference_cards.json"
        self.cards_yaml_path = self.board_dir / "reference_cards.yaml"
        self.items_path = self.board_dir / "moodboard_items.json"
        self.synthesis_path = self.board_dir / "moodboard_synthesis.md"

    def ensure(self) -> None:
        for folder in [self.inbox_dir, self.accepted_dir, self.rejected_dir, self.exports_dir]:
            folder.mkdir(parents=True, exist_ok=True)
        if not self.cards_path.exists():
            write_json(self.cards_path, {"cards": DEFAULT_CARDS})
        if not self.cards_yaml_path.exists():
            self.cards_yaml_path.write_text(card_yaml(DEFAULT_CARDS), encoding="utf-8")
        if not self.items_path.exists():
            write_json(self.items_path, [])
        self.scan()

    def cards(self) -> list[dict]:
        return read_json(self.cards_path, {"cards": DEFAULT_CARDS}).get("cards", [])

    def items(self) -> list[dict]:
        return read_json(self.items_path, [])

    def save_items(self, items: list[dict]) -> None:
        write_json(self.items_path, items)

    def rel(self, path: Path) -> str:
        return path.resolve().relative_to(self.board_dir.resolve()).as_posix()

    def scan(self) -> list[dict]:
        self.inbox_dir.mkdir(parents=True, exist_ok=True)
        items = self.items()
        seen = {item.get("file_path") for item in items}
        next_index = len(items) + 1
        for image in sorted(self.inbox_dir.iterdir()):
            if not image.is_file() or image.suffix.lower() not in IMAGE_EXTS:
                continue
            rel_path = self.rel(image)
            if rel_path in seen:
                continue
            items.append(
                {
                    "image_id": f"IMG_{next_index:04d}",
                    "file_path": rel_path,
                    "linked_card_id": "",
                    "status": "unreviewed",
                    "human_tags": [],
                    "human_note": "",
                    "agent_analysis": {
                        "shot_size": "",
                        "camera_position": "",
                        "subject_position": "",
                        "what_to_learn": [],
                        "what_to_avoid": [],
                        "prompt_ready_rules": [],
                    },
                    "created_at": dt.datetime.now().isoformat(timespec="seconds"),
                }
            )
            next_index += 1
        self.save_items(items)
        return items

    def file_for_url(self, rel_path: str) -> Path | None:
        decoded = unquote(rel_path).lstrip("/")
        target = (self.board_dir / decoded).resolve()
        try:
            target.relative_to(self.board_dir.resolve())
        except ValueError:
            return None
        if not target.exists() or not target.is_file():
            return None
        return target

    def state(self) -> dict:
        self.scan()
        return {
            "project": "定稿",
            "run_dir": str(self.run_dir),
            "board_dir": str(self.board_dir),
            "inbox_dir": str(self.inbox_dir),
            "cards": self.cards(),
            "items": self.items(),
            "tag_options": TAG_OPTIONS,
        }

    def upload(self, payload: dict) -> dict:
        filename = safe_filename(str(payload.get("filename", "image.png")))
        raw_data = str(payload.get("data", ""))
        if "," in raw_data:
            raw_data = raw_data.split(",", 1)[1]
        content = base64.b64decode(raw_data)
        target = self.inbox_dir / filename
        counter = 2
        while target.exists():
            target = self.inbox_dir / f"{Path(filename).stem}_{counter}{Path(filename).suffix}"
            counter += 1
        target.write_bytes(content)
        self.scan()
        return {"ok": True, "file_path": self.rel(target)}

    def synthesize(self) -> dict:
        cards_by_id = {card["card_id"]: card for card in self.cards()}
        items = self.items()
        lines = [
            "# Moodboard Synthesis",
            "",
            f"生成时间：{dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            "## Human 标注总览",
            "",
        ]
        if not items:
            lines.append("还没有参考图。先把图片放入 `inbox/`，或在页面中上传。")
        for card in self.cards():
            linked = [item for item in items if item.get("linked_card_id") == card["card_id"]]
            if not linked:
                continue
            lines.extend([f"### {card['card_id']} {card['shot_name']}", ""])
            lines.append(f"- 戏剧功能：{card['dramatic_function']}")
            lines.append(f"- 观众感受：{card['viewer_should_feel']}")
            for item in linked:
                tags = "、".join(item.get("human_tags", [])) or "未标注"
                note = item.get("human_note", "").strip() or "无备注"
                lines.append(f"- `{item['image_id']}` `{item['file_path']}`：{tags}。Human 备注：{note}")
            accepted = [item for item in linked if "靠近" in item.get("human_tags", [])]
            rejected = [item for item in linked if "远离" in item.get("human_tags", [])]
            if accepted:
                lines.append("- 可学习方向：" + "；".join(item.get("human_note", "") or item["image_id"] for item in accepted))
            if rejected:
                lines.append("- 需要避开：" + "；".join(item.get("human_note", "") or item["image_id"] for item in rejected))
            lines.append("")
        unlinked = [item for item in items if not item.get("linked_card_id")]
        if unlinked:
            lines.extend(["## 未绑定任务卡的图片", ""])
            lines.extend(f"- `{item['image_id']}` `{item['file_path']}`" for item in unlinked)
            lines.append("")
        lines.extend(
            [
                "## 下一步 Agent 分析要求",
                "",
                "- 摄影 Agent：把 Human 标注转成景别、机位、人物距离、镜头高度。",
                "- 美术 Agent：把 Human 标注转成空间、材质、道具、色彩规则。",
                "- Prompt Agent：只使用被 Human 标注为可学习的维度，不复制整张参考图。",
                "- Showrunner：把 `远离` 和 `危险但有一点可学` 变成负面约束。",
            ]
        )
        self.synthesis_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        return {"ok": True, "path": str(self.synthesis_path), "content": "\n".join(lines)}


def make_handler(store: MoodboardStore):
    class Handler(BaseHTTPRequestHandler):
        def log_message(self, format: str, *args) -> None:  # noqa: A002
            return

        def send_json(self, value, status=HTTPStatus.OK) -> None:
            body = json.dumps(value, ensure_ascii=False).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def send_text(self, text: str, status=HTTPStatus.OK, content_type="text/plain; charset=utf-8") -> None:
            body = text.encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def send_file(self, path: Path) -> None:
            content_type = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
            body = path.read_bytes()
            self.send_response(HTTPStatus.OK)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def read_payload(self) -> dict:
            length = int(self.headers.get("Content-Length", "0"))
            raw = self.rfile.read(length).decode("utf-8")
            return json.loads(raw or "{}")

        def send_timeline(self) -> None:
            items = build_items(store.run_dir, include_content=False)
            self.send_json(timeline_payload(items, store.run_dir))

        def send_artifact(self) -> None:
            query = parse_qs(urlparse(self.path).query)
            rel_path = query.get("path", [""])[0]
            if not rel_path:
                self.send_json({"error": "missing path"}, HTTPStatus.BAD_REQUEST)
                return
            target = (ROOT / unquote(rel_path).lstrip("/")).resolve()
            try:
                target.relative_to(ROOT.resolve())
            except ValueError:
                self.send_json({"error": "path outside workspace"}, HTTPStatus.BAD_REQUEST)
                return
            if not target.is_file() or target.suffix.lower() not in ARTIFACT_EXTS:
                self.send_json({"error": "artifact not found"}, HTTPStatus.NOT_FOUND)
                return
            content = target.read_text(encoding="utf-8", errors="replace")
            self.send_json(
                {
                    "path": target.relative_to(ROOT).as_posix(),
                    "content": content,
                    "extension": target.suffix.lower().lstrip("."),
                    "size": len(content),
                }
            )

        def do_GET(self) -> None:  # noqa: N802
            path = urlparse(self.path).path
            if path in {"/", "/moodboard", "/moodboard.html"}:
                self.send_file(ROOT / "ui" / "moodboard.html")
                return
            if path in {"/timeline", "/agent-timeline", "/agent_timeline.html"}:
                self.send_file(ROOT / "ui" / "agent_timeline.html")
                return
            if path == "/api/state":
                self.send_json(store.state())
                return
            if path == "/api/timeline":
                self.send_timeline()
                return
            if path == "/api/artifact":
                self.send_artifact()
                return
            if path == "/api/scan":
                self.send_json({"ok": True, "items": store.scan()})
                return
            if path.startswith("/files/"):
                target = store.file_for_url(path.removeprefix("/files/"))
                if target:
                    self.send_file(target)
                    return
                self.send_json({"error": "file not found"}, HTTPStatus.NOT_FOUND)
                return
            self.send_json({"error": "not found"}, HTTPStatus.NOT_FOUND)

        def do_POST(self) -> None:  # noqa: N802
            path = urlparse(self.path).path
            try:
                payload = self.read_payload()
                if path == "/api/items":
                    items = payload.get("items")
                    if not isinstance(items, list):
                        self.send_json({"error": "items must be a list"}, HTTPStatus.BAD_REQUEST)
                        return
                    store.save_items(items)
                    self.send_json({"ok": True, "items": store.items()})
                    return
                if path == "/api/upload":
                    self.send_json(store.upload(payload))
                    return
                if path == "/api/synthesize":
                    self.send_json(store.synthesize())
                    return
            except Exception as exc:  # pragma: no cover - local diagnostic surface
                self.send_json({"error": str(exc)}, HTTPStatus.INTERNAL_SERVER_ERROR)
                return
            self.send_json({"error": "not found"}, HTTPStatus.NOT_FOUND)

    return Handler


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the local Moodboard MVP server.")
    parser.add_argument("--run", default=str(DEFAULT_RUN), help="Run directory to attach the moodboard to.")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", default=8765, type=int)
    args = parser.parse_args()

    store = MoodboardStore(Path(args.run))
    store.ensure()
    server = ThreadingHTTPServer((args.host, args.port), make_handler(store))
    print(f"Moodboard MVP: http://{args.host}:{args.port}/moodboard")
    print(f"Inbox folder: {store.inbox_dir}")
    server.serve_forever()


if __name__ == "__main__":
    main()
