# Moodboard MVP PRD

## 1. 产品判断

对于审美权重很高的创作任务，Agent Team 不应该太早生成一张“看起来像答案”的图。

这个 MVP 的核心目的，是在 AI 生图/生视频之前，帮助 Human 先建立自己的视觉预期。Agent 要做的不是抢先给答案，而是把用户模糊的审美感觉拆成可寻找、可标注、可分析、可复用的参考任务。

核心信念：

> AI 应该帮助用户长出自己的想象，而不是用第一张还不错的 AI 图替用户决定想象。

## 2. 当前问题

在《定稿》的视觉测试里，Agent Team 在 Human 尚未形成清晰视觉预期前，就直接生成了概念图。

这暴露了几个问题：

- AI 图会变成过早的答案，把 Human 的判断带跑。
- 提示词会把太多美术、摄影、导演判断塞进一段长描述。
- 结果容易变成“脏一点的电影剧照”，而不是 Human 真正想找的“廉价设备拍坏了的现实”。
- Human 会更难说清楚“哪里不对”，因为生成图已经先占据了想象空间。

所以，在生图之前需要增加一个阶段：

- Agent 先提出应该找什么参考。
- Human 自己收集图，并标注图里哪些东西有用、哪些东西不要。
- Agent 对参考图做图像理解，抽取镜头、空间、站位、影调、质感规则。
- Prompt Agent 最后才把这些规则转成生图/生视频提示词。

## 3. 用户

主要用户：

- AI 视频创作者 / 导演 / 编剧型创作者。
- 有审美直觉，但不一定有完整电影语言词汇。
- 想做短片、短剧、广告、MV、动画、平台热播内容等。
- 需要在 AI 生成前，先把脑中感觉外化成可讨论的视觉资产。

次级用户：

- 编剧：用参考图明确气质与情绪。
- 导演 Agent：把感觉转成场面调度和观众体验。
- 摄影 Agent：把感觉转成机位、景别、光线、运动。
- 美术概念 Agent：把感觉转成空间、材质、道具、色彩。
- Prompt Agent：把已确认的视觉规则转成短而可控的提示词。

## 4. MVP 目标

做一个轻量本地 Moodboard 工作台，让用户可以：

- 看到 Agent 为关键镜头生成的“寻图任务卡”。
- 把参考图直接丢进本机文件夹。
- 在前端看到这些图片。
- 给每张图标注“只要它的什么 / 不要它的什么”。
- 让 Agent 根据标注做图像理解和视觉规则总结。
- 把这些规则交给后续分镜、提示词、生图、生视频环节。

## 5. 非目标

MVP 暂时不做：

- 完整设计工具，不做 Figma。
- 云端账号系统。
- 自动爬取版权图片。
- 在 Human 完成感觉校准前生成最终风格图。
- 让参考图被直接复制，只抽取结构、光线、空间、站位等可迁移规则。

## 6. 成功标准

这个 MVP 有价值的判断标准：

- Human 可以在 5 分钟内放入 10-30 张参考图。
- 每张图可以被标注为“靠近 / 远离 / 只要某个维度”。
- Agent 能把参考图总结成具体镜头规则，而不是泛泛说“氛围压抑”。
- 后续提示词更短、更结构化、更容易被 Human 判断对错。
- Human 在看到下一张 AI 图之前，已经能说出自己期待什么、不期待什么。

## 7. 核心流程

### Step 1：Agent 生成寻图任务卡

Showrunner 先挑出需要视觉校准的关键镜头，再让相关 Agent 为每个镜头生成一张卡。

参与 Agent：

- Showrunner：判断哪些镜头必须先做 Moodboard，避免过早生图。
- 导演：定义镜头的戏剧功能和观众感受。
- 摄影：定义机位、景别、人物距离、光源、镜头运动。
- 美术概念：定义空间、材质、道具、色彩和参考方向。
- 剪辑：定义这个镜头在节奏中的作用。
- Prompt Structurer：记录哪些视觉事实未来可进入提示词，但此阶段不急着写最终 prompt。

任务卡字段：

```yaml
card_id:
scene_id:
shot_name:
dramatic_function:
viewer_should_feel:
look_for:
  - 人物站位
  - 空间关系
  - 景别
  - 机位
  - 光线 / 色温
  - 质感 / 媒介
avoid:
  - 错误类型
  - 错误年代
  - 错误阶层信号
  - 过度风格化风险
suggested_search_terms:
  zh:
  en:
reference_film_or_video_targets:
  - title:
    watch_for:
human_notes:
```

### Step 2：Human 收集参考图

MVP 为项目创建本地文件夹：

```text
runs/<project_id>/05_moodboard/inbox/
```

Human 可以把截图、电影帧、网页图片、手机照片、短视频截帧放进去。

支持格式：

- `.png`
- `.jpg`
- `.jpeg`
- `.webp`

前端可以通过刷新按钮扫描这个文件夹并展示新图片。

### Step 3：Human 标注图片

Human 不需要写正式审美报告，只需要标注这张图“哪里有用”。

基础标签：

- `靠近`
- `远离`
- `只要站位`
- `只要空间`
- `只要景别`
- `只要影调`
- `只要光线`
- `只要质感`
- `只要人物距离`
- `危险但有一点可学`

自由备注示例：

```text
我只要它的门框站位，不要它的电影感。
```

```text
这个空间压迫感对，但电脑太复古，不要年代戏感。
```

```text
只要这种人物被房间吞掉的比例，不要这种漂亮打光。
```

### Step 4：Agent 做图像理解

对被 Human 标注过的图，Agent 分析：

```yaml
image_id:
linked_card_id:
human_tags:
scene_type:
shot_size:
camera_position:
camera_height:
subject_position:
foreground:
background:
space_pressure:
light_source:
color_temperature:
medium_texture:
what_to_learn:
what_to_avoid:
prompt_ready_rules:
```

Agent 必须区分：

- Human 想学习的是结构，还是影调，还是站位，还是空间。
- 哪些东西不能学。
- 哪些规则应该进入分镜。
- 哪些规则应该进入提示词。
- 哪些规则应该进入负面提示词。

### Step 5：Agent 生成 Moodboard 总结

输出文件：

```text
runs/<project_id>/05_moodboard/moodboard_synthesis.md
```

总结内容：

- Human 当前审美倾向。
- 被接受的参考图和原因。
- 被拒绝的参考图和原因。
- 按镜头整理的空间 / 景别 / 机位 / 影调规则。
- 可进入提示词的正向规则。
- 可进入负面提示词的排除规则。
- 还需要 Human 补充判断的问题。

## 8. MVP 界面

### 页面布局

三栏工作台：

```text
左侧：寻图任务卡
中间：Moodboard 图片网格
右侧：选中图片检查器
```

### 左栏：任务卡

每张卡展示：

- 镜头名。
- 戏剧功能。
- 要找什么。
- 不要什么。
- 推荐搜索词。
- 推荐参考片 / 影像方向。

操作：

- 选中任务卡。
- 标记已解决 / 未解决。
- 添加 Human 备注。

### 中栏：图片网格

展示来自本地文件夹的图片：

```text
runs/<project_id>/05_moodboard/inbox/
```

每张图显示：

- 缩略图。
- 文件名。
- 绑定的任务卡。
- Human 标签。
- Agent 分析状态。

操作：

- 绑定到当前任务卡。
- 添加标签。
- 标记接受 / 拒绝。
- 放大预览。

### 右栏：图片检查器

展示选中图片和它的分析信息：

- 大图预览。
- Human 标签。
- Human 备注。
- Agent 图像理解结果。
- “用它的什么”清单。
- “不要学它的什么”清单。

## 9. 数据结构

### 文件结构

```text
runs/<project_id>/05_moodboard/
  reference_cards.yaml
  moodboard_items.json
  moodboard_synthesis.md
  inbox/
  accepted/
  rejected/
  exports/
```

### reference_cards.yaml

```yaml
cards:
  - card_id: MB_001
    scene_id: S01
    shot_name: 从门口看见许临在电脑前
    status: unresolved
    dramatic_function: 第一次证明他不是操盘手，而是被生活压住的人。
    viewer_should_feel: 房间比人更有力量，人像被空间吞掉。
    look_for:
      - 门口视角
      - 狭小房间纵深
      - 背对镜头的人
      - 电脑屏幕作为实际光源
    avoid:
      - 赛博朋克剪辑室
      - 复古 CRT 电脑
      - 漂亮的电影化贫穷
    suggested_search_terms:
      zh:
        - 出租屋 门口 电脑 背影
        - 旧小区出租屋 漏水 电脑桌
      en:
        - cramped apartment doorway computer back view
        - low income room computer screen light
```

### moodboard_items.json

```json
[
  {
    "image_id": "IMG_0001",
    "file_path": "inbox/example.png",
    "linked_card_id": "MB_001",
    "human_tags": ["只要站位", "远离"],
    "human_note": "站位接近，但太电影化。",
    "agent_analysis": {
      "shot_size": "全景",
      "camera_position": "门口向内看",
      "subject_position": "人物在画面右侧三分之一，背对镜头",
      "what_to_learn": ["门框作为前景压迫"],
      "what_to_avoid": ["过于精致的布光"]
    }
  }
]
```

## 10. 《定稿》首批任务卡

第一版 MVP 先为这些镜头生成任务卡：

1. 从出租屋门口看见许临在电脑前。
2. 漏水房间：盆、剧本、插线板、屏幕反光。
3. 剪辑屏幕制造第一轮“男明星有罪”叙事。
4. 外卖骑手在雨夜看竖屏舆论视频。
5. 电梯走廊：道歉涂鸦和广告脸。
6. 许临父亲餐饮店被差评流冲击。
7. 廉价屏幕上的公共舆论蒙太奇。
8. 最终空房间：人离开，系统还在同步。

每张卡都应该引导 Human 找：

- 人物站位。
- 空间压迫。
- 景别。
- 机位。
- 实际光源。
- 影像质感。
- 必须避开的错误方向。

## 11. Agent Team 分工

### Showrunner

- 判断什么时候必须进入 Moodboard 阶段。
- 选择关键镜头。
- 阻止过早生图。
- 记录 Human 的决定。

### 导演 Agent

- 定义每个镜头的情绪功能。
- 拒绝“看起来好看但伤害主题”的参考。

### 摄影 Agent

- 把参考图转成摄影语言。
- 追踪景别、机位、高度、光线、运动和画面逻辑。

### 美术概念 Agent

- 推荐参考领域。
- 把 Human 的感觉翻译成空间、道具、材质、色彩规则。

### 剪辑 Agent

- 判断参考图是否支持影片节奏。
- 标记太像单张海报、太解释性、太抢戏的图。

### Prompt Structurer Agent

- 在 Moodboard 总结完成前，不写最终生图/生视频提示词。
- 把已接受的视觉规则转成短提示词块。
- 把被拒绝的方向写进负面约束。

### 观众 Agent

- 判断视觉方向是否会按照预期操控观众。
- 标记过度说教、过度直白、过度站队的图像风险。

### Human Creative Director

- 添加参考图。
- 标注每张图有用和无用的部分。
- 做最终审美拍板。

## 12. 实现计划

### Phase 1：静态本地 MVP

做一个简单 HTML/JS 页面：

- 读取 `reference_cards.yaml`。
- 读取 `moodboard_items.json`。
- 展示本地图片缩略图。
- 支持手动标注和写备注。
- 支持导出更新后的 JSON。

### Phase 2：文件夹联动

加入刷新/扫描能力：

- 扫描 `05_moodboard/inbox/`。
- 把新图片写入 `moodboard_items.json`。
- 在前端自动展示。

### Phase 3：Agent 图像分析

增加一个命令：

```text
analyze-moodboard
```

它读取：

- `reference_cards.yaml`
- `moodboard_items.json`
- Human 标签和备注

然后写出：

- `moodboard_synthesis.md`

### Phase 4：提示词交接

Prompt Structurer 读取：

- `moodboard_synthesis.md`
- 被接受参考图规则
- 被拒绝参考图规则

然后写：

- `team_jimeng_prompts.md`
- `prompt_ledger.md`
- `prompt_contradiction_check.md`

## 13. 产品问题

还需要决定：

- 图片被接受/拒绝后，是复制到 `accepted/`、`rejected/`，还是只在 JSON 里标记？
- MVP 是否需要拖拽上传，还是本机文件夹投放就够？
- 图像分析是点击按钮触发，还是标签变化后自动触发？
- 是否需要把 AI 生成结果和 Moodboard 参考图并排比较？
- 如何记录参考图来源，避免版权和隐私风险？

## 14. MVP 验收标准

对《定稿》来说，MVP 通过验收需要满足：

- UI 能展示 8 张寻图任务卡。
- Human 能把至少 5 张图片放进 `inbox/` 并在页面看到。
- Human 能给图片打上 `只要站位` 等标签，并写备注。
- Agent 能读取这些标签，生成 Moodboard 总结。
- 下一次生图提示词必须明确引用：用了哪些 Moodboard 规则，避开了哪些被拒绝方向。
