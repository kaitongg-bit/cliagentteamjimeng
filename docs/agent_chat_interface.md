# @Agent Chat Interface

第一阶段可以不做复杂产品界面，直接在当前对话框里用 `@agent` 推进。

## 使用规则

每次 @ 一个或多个 Agent，明确输入、任务、输出格式。

推荐格式：

```text
@编剧 @剧本医生
输入：<brief 或上一版产物>
任务：生成 3 个 10 分钟微电影创意，并互相质疑。
输出：
1. 三个 logline
2. 每个方案的核心冲突
3. 剧本医生反对意见
4. 推荐排序
```

## 常用 Agent 名称

```text
@Showrunner
@编剧
@剧本医生
@反方编剧
@美术概念设计师
@风格策展人
@导演
@摄影指导
@粗分镜师
@细分镜师
@PromptStructurer
@PromptCompliance
@制片人
@剪辑
@AI演技指导
@审片人
@观众
@Human
```

## 推荐推进顺序

### 1. 创意辩论

```text
@编剧 @反方编剧 @观众 @Human @Showrunner
基于 brief 做创意 debate。
编剧给 3 个方案，反方逐个攻击，观众判断理解和观看欲，Human 给直觉，Showrunner 最终选择。
```

### 2. 剧本开发

```text
@编剧 @剧本医生
把选中的方案扩成 10 分钟四段式结构、人物弧光、场景列表。
剧本医生保持原强度审查，不降级。
```

### 3. 风格共创

```text
@美术概念设计师 @风格策展人 @Human
请先启发我应该去找哪些电影、截图、色彩、布光、导演参考。
等我粘贴 style skill 的解析词后，再整理成 visual bible。
```

### 4. 导演统筹

```text
@导演 @摄影指导 @剪辑 @AI演技指导
把剧本和 visual bible 统一成导演阐述、场景意图、镜头语言和表演策略。
```

### 5. 粗细分镜

```text
@粗分镜师 @细分镜师 @导演 @摄影指导 @剪辑 @AI演技指导
不需要 Human 逐镜头参与。
请输出 coarse storyboard 和 fine storyboard，包含 shot_id、时长、景别、动作、镜头运动、表演、连续性。
```

### 6. 即梦 Prompt

```text
@PromptStructurer @PromptCompliance @导演 @摄影指导 @细分镜师 @AI演技指导 @审片人
把 fine storyboard 转成即梦 prompts。
要求：
- 结构化字段
- 不冗长
- 不自相矛盾
- 保留 continuity
- 合规过审
- 每个 prompt 说明从哪个 shot spec 来
```

### 7. 审片

```text
@审片人 @观众 @Human @Showrunner
审片人先机器审一轮，观众给观看反应，Human 拍板，Showrunner 输出下一轮 revision brief。
```

## Prompt Structurer 输出模板

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
style_rules:
continuity:
negative:
compliance_notes:
final_jimeng_prompt:
```

## Human 输入模板

```text
@Human
我对这一版的直觉：
喜欢：
不喜欢：
看不懂：
最有记忆点：
必须保留：
必须删：
我粘贴的 style skill 解析词：
```
