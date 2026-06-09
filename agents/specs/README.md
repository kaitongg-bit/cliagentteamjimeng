# Agent Specs

这里放真正 runtime 可用的精细 Agent 设定。

每个 Agent Spec 都必须说明：

- 使命
- 可见输入
- 不可见输入
- 工作规则
- 输出格式
- 自检清单
- 与其他 Agent 的交接点
- Human 参与点

## 编剧 Agent 的特殊规则

编剧与剧本医生不在这里重写完整方法论，而是引用用户提供的：

```text
/Users/bytedance/Downloads/screenwriting-master.skill
```

这个 `.skill` 包是编剧 Agent 的 canonical source。

原因：

- 它已经包含 5-10 分钟短片路由。
- 它有完整八步流程。
- 它有写作红线和自检纪律。
- 它要求按步骤暂停，不一次性生成所有内容。

仓库内的 `screenwriter.yaml` 只定义如何在 Agent Team runtime 中调用该 skill，而不复制其全部内容。

## 素材招募 Agent 的特殊规则

素材招募不是完整场务清单，而是给 AIGC 生成用的“高价值资产短表”。具体设定见：

```text
agents/specs/material_recruitment_agent.yaml
```

它只应该保留：

- 跨多个镜头复用的角色、空间、道具；
- 会影响人物一致性、空间一致性、叙事理解的东西；
- 需要单独生图、做三视图、做 moodboard 或后期锁定的东西。

一次性出现的普通道具、群演、背景装饰，不应进入素材表。它们可以在后续镜头提示词里顺手描述，不值得单独花 token 生成。
