# 第二阶段桌面验收

验收对象是 `feat/codex-core-workflow` 分支的 `0.2.0-alpha.1` 候选版本。第一阶段的 `0.1.0-alpha.1` 验收不覆盖这些新流程。开始时记下 Codex 桌面版本和本次 Git 提交；桌面结果与 CLI 结果分别记录。

## 1. 安装候选插件

仓库 marketplace 应指向当前 checkout 的 `plugins/pstack/`。在桌面插件目录中找到 **pstack for Codex (preview)**，若有旧安装，先卸载，再安装当前候选。确认插件版本是 `0.2.0-alpha.1`，必要时重启应用。

应能找到两个显式入口：`$pstack:poteto-mode` 和 `$pstack:setup-pstack`。已准备的项目链接另外提供短入口 `$poteto-mode`。安装插件不会自动启用工作流。

## 2. 打开临时项目，准备模型目录

使用聊天中提供的临时根目录，里面有 `feature`、`bug`、`investigation` 三个独立 Git 项目。每个项目已经放好 app.py、check.py、项目角色和短入口链接。分别以相应子目录作为聊天的工作目录，不要用正式项目。角色安装后需开始新聊天；若 Codex 提示项目配置尚未受信任，只确认本次临时项目，不要改全局信任设置。

开始验收时，在仓库 checkout 的终端执行：

```sh
python3 -B plugins/pstack/skills/poteto-mode/scripts/runtime.py models --output /tmp/pstack-desktop-catalog.json
```

这是当前账户的原生模型目录快照，一小时后过期。过期就重新运行，不要手工编造目录。它用于避免模型沙箱内无法嵌套运行 app-server 的限制。

为便于对齐已做的 CLI 测试，可在桌面选择 `gpt-6.1-sol` 和 `low` 推理强度。若桌面没有该选项，使用实际可用组合，并把下面提示词中的父模型/强度改为所选值；不要猜测当前设置。

## 3. Feature 和同任务跟进

以 `feature` 为工作目录新建测试聊天，发送：

```text
$pstack:poteto-mode
这是临时验收项目。父模型为 gpt-6.1-sol，推理强度 low。
模型解析使用 --catalog /tmp/pstack-desktop-catalog.json，不要嵌套启动 app-server。
在 app.py 增加 multiply(a,b)，保留 add。用 python3 -B check.py 验证。
清单保存在 task.md。只允许修改 app.py 和 task.md，不得改 check.py。
按流程委派并由主聊天检查结果；不要提交、开 PR、修改角色或配置、发送外部消息。
```

预期看到 Feature 路由、poteto-agent 实现、主聊天验证及 comment-sicko 审查；测试通过，check.py 保持不变。

随后在**同一聊天**发送，不再重复入口：

```text
继续刚才的任务，重新运行验收，读取并更新现有 task.md 清单。不要重新实现、委派或提交。
```

预期沿用同一份清单并追加本次验证结果。

## 4. Bug fix

以 `bug` 为工作目录新建测试聊天，发送：

```text
$poteto-mode
这是临时验收项目。父模型为 gpt-6.1-sol，推理强度 low。
模型解析使用 --catalog /tmp/pstack-desktop-catalog.json，不要嵌套启动 app-server。
app.py 的 average([2,4,6]) 目前返回 3，应为 4。
先用 python3 -B check.py 复现失败，再修复并重跑同一测试。
清单保存在 task.md。只允许修改 app.py 和 task.md，不得改 check.py。
按流程委派并由主聊天检查结果；不要提交、开 PR、修改角色或配置、发送外部消息。
```

预期同一测试先失败后通过；实际发生实现委派和主聊天复核。缺少角色或模型时，应说明阻塞，不能跳过委派自行完成后宣称通过。

## 5. 只读调查和普通聊天

以 `investigation` 为工作目录新建测试聊天，发送：

```text
$poteto-mode
解释 app.py 中 total(items) 的计算过程，给出文件与行号依据。
这是只读调查，不得修改任何文件、创建清单文件、安装角色或配置、执行远程写入。
如需委派，父模型为 gpt-6.1-sol、推理强度 low，使用 --catalog /tmp/pstack-desktop-catalog.json。
```

预期得到有依据的说明，项目里的已跟踪、未跟踪文件、链接及权限不变。

最后另开一个普通聊天，不带入口，发送：

```text
7+5，只输出数字
```

预期只回复 `12`，不创建清单、不委派、不进入 pstack 流程。

## 6. 反馈和保留证据

反馈 Codex 桌面版本，以及安装、Feature、跟进、Bug fix、调查、普通聊天、卸载各项的结果。遇到问题，只需说明卡在哪一步、看到什么。不要仅凭模型说“成功”就算通过，留意实际工具调用和测试输出。

临时安装的插件在验收后卸载。先保留三个项目和测试聊天，不要删除或重置文件；收到反馈后再核对文件差异。无需上传私人完整会话。

结果分别记录为 PASS、FAIL、BLOCKED 或 NOT RUN。人工报告会标明由仓库所有者确认，不会写成 agent 自动操作或截图验收。当前工具明确拒绝控制 Codex 应用，因此仍需手动完成桌面步骤；CLI 的通过不能替代这部分。
