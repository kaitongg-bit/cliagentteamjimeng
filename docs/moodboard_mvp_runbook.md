# Moodboard MVP 使用说明

## 启动

在项目根目录运行：

```bash
python3 scripts/moodboard_server.py --port 8765
```

然后打开：

```text
http://127.0.0.1:8765/moodboard
```

默认绑定《定稿》这轮实验：

```text
runs/20260527_194857_invisible-bullying-world-trial/
```

如果要绑定其他 run：

```bash
python3 scripts/moodboard_server.py --run runs/<run_id> --port 8765
```

## 文件夹

首次启动会自动创建：

```text
runs/<run_id>/05_moodboard/
  reference_cards.json
  reference_cards.yaml
  moodboard_items.json
  moodboard_synthesis.md
  inbox/
  accepted/
  rejected/
  exports/
```

把参考图放进：

```text
runs/<run_id>/05_moodboard/inbox/
```

支持：

- `.png`
- `.jpg`
- `.jpeg`
- `.webp`

页面里点“刷新文件夹”，新图片会出现在图片网格。

## 页面怎么用

左侧是 Agent 生成的寻图任务卡。

中间是参考图网格。

右侧是选中图片检查器，可以做三件事：

- 绑定图片到某张任务卡。
- 打标签：`靠近`、`远离`、`只要站位`、`只要空间`、`只要景别`、`只要影调`、`只要光线`、`只要质感`、`只要人物距离`、`危险但有一点可学`。
- 写一句 Human 备注，例如：`只要它的门框站位，不要它的电影感。`

点“保存标注”会写入：

```text
runs/<run_id>/05_moodboard/moodboard_items.json
```

点“生成总结”会写入：

```text
runs/<run_id>/05_moodboard/moodboard_synthesis.md
```

## 当前 MVP 已实现

- 8 张《定稿》关键镜头寻图任务卡。
- 本机 `inbox/` 文件夹扫描。
- 页面上传参考图。
- 图片绑定任务卡。
- Human 标签和备注保存。
- Moodboard 总结导出。
- 根页面入口：`http://127.0.0.1:8765/` 里可以打开 Moodboard。

## 当前 MVP 还没实现

- 真正的图像理解自动分析。
- 按 `accepted/`、`rejected/` 自动移动图片。
- AI 生成图与 moodboard 参考图并排对比。
- Prompt Agent 自动引用 moodboard 规则生成即梦提示词。

下一步建议先让 Human 放入 5-10 张参考图，完成一轮真实标注，再接 Agent 图像理解。这样分析会基于 Human 的审美选择，而不是模型先入为主。
