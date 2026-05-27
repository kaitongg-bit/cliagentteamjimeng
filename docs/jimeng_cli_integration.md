# Jimeng CLI Integration

## 安装

用户给定安装方式：

```bash
curl -s https://jimeng.jianying.com/cli | bash
```

本仓库不把即梦 CLI 包进 repo，只做检查和产物组织。

## 检查

```bash
python3 scripts/film_agent_team.py check-jimeng
```

脚本会尝试寻找：

- `jimeng`
- `dreamina`
- `jimeng-cli`

如果 CLI 安装后没有进入 PATH，先重启终端或检查安装脚本输出的路径。

## 推荐目录

每次实验中，把即梦相关内容放在：

```text
runs/<run_id>/03_jimeng/
  prompts/
  commands.md
  generation_log.md
  jimeng_outputs/
```

## Prompt 结构建议

每个镜头建议写成结构化块，而不是一整段长文本：

```text
shot_id:
duration:
story_function:
subject:
action:
performance:
camera:
composition:
lighting:
palette:
environment:
style:
negative:
continuity:
```

来自创作者访谈的关键注意事项：

- 不要把“高级感”“电影感”当作主要描述。
- 不要在大特写里详细描述看不见的背景。
- 不要堆互相矛盾的词。
- 人物视线、景别、焦段、光线要服务叙事。
- 即梦大镜头和运镜能力强，特写表演需要更精细指导。

## 生成记录

每次生成都记录：

- shot_id
- prompt version
- CLI command
- seed / model / aspect ratio / duration
- output path
- 是否可用
- 失败原因
- 下一轮修改 brief

这样才能比较 Single Agent 与 Agent Team 的生成效率。
