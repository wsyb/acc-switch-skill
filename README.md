# acc-switch

> 老板只说要什么，保姆搞定 CC Switch 配置。具体软件配置由 CC Switch 自己同步。

## 简介

acc-switch 是一个 AI Agent 技能，让你用自然语言管理 CC Switch 配置。无需手动操作 CC Switch 界面，直接告诉 AI 你要什么就行。

**🎯 最佳使用场景：批量操作！**

```
"删除所有配置中关于 gitnexus 的配置"
"清理所有 nvidia 的 provider"
"给所有平台启用 fetch MCP"
```

## 核心特性

- **先确认，后执行** - 每次操作前向用户展示计划并获得确认
- **动态生成代码** - AI 根据用户需求动态生成 Python 代码
- **只操作数据库** - 不直接修改具体软件的配置文件
- **提醒同步** - 操作后提醒用户重启 CC Switch 或手动同步

## 支持的平台

CC Switch 支持以下 AI Agent 平台：

| 平台 | app_type | 说明 |
|------|----------|------|
| Claude Code | claude | Anthropic Claude |
| Codex | codex | OpenAI Codex |
| Gemini CLI | gemini | Google Gemini |
| OpenCode | opencode | OpenCode |
| Hermes | hermes | Hermes |

## 安装

### Claude Code

```bash
# 克隆到 Claude skills 目录
git clone https://github.com/wsyb/acc-switch-skill.git ~/.claude/skills/acc-switch
```

### Codex

```bash
git clone https://github.com/wsyb/acc-switch-skill.git ~/.codex/skills/acc-switch
```

### Gemini

```bash
git clone https://github.com/wsyb/acc-switch-skill.git ~/.gemini/skills/acc-switch
```

### OpenCode

```bash
git clone https://github.com/wsyb/acc-switch-skill.git ~/.opencode/skills/acc-switch
```

### Hermes

```bash
git clone https://github.com/wsyb/acc-switch-skill.git ~/.hermes/skills/acc-switch
```

### 使用安装脚本

```bash
# macOS/Linux
bash install/install.sh

# Windows
install\install.bat
```

## 使用示例

```
# 配置 Provider
"我的 key 是 xxx，url 是 yyy，配上"

# 添加 MCP
"给我加一个 fetch MCP"

# 批量清理
"所有 nvidia 的 provider 都删掉"

# 配置诊断
"doctor 一下"

# 从浏览器获取
"从浏览器获取 mimo 的 key"
```

## 工作流程

1. **理解需求** - AI 解析用户意图
2. **查询现状** - 查询 CC Switch 数据库当前状态
3. **展示计划** - 向用户展示将要执行的操作
4. **获得确认** - 等待用户确认后才执行
5. **执行操作** - 动态生成 Python 代码执行
6. **提醒同步** - 提醒用户重启 CC Switch 或手动同步

## ⚠️ 安全与隐私限制

**重要：使用本技能前请了解以下风险。**

### API Key 会上传到大语言模型

本技能的工作原理是：
1. 读取 CC Switch 数据库中的配置（包含 API Key）
2. 将查询结果发送给 AI 模型进行处理
3. AI 模型会在对话中显示配置信息

**这意味着：**
- 你的 API Key 会作为上下文发送给 AI 模型提供商
- Key 会出现在对话历史中
- 本技能只对 Key 做了简单的脱敏（显示前 8 位），但完整 Key 仍会发送给模型

### 建议

1. **敏感操作请手动处理** - 如果担心 Key 泄露，建议直接在 CC Switch 界面操作
2. **定期轮换 Key** - 使用本技能后，建议定期更换 API Key
3. **使用专用 Key** - 为测试/调试使用独立的 API Key，不要使用生产环境的 Key
4. **了解模型提供商的隐私政策** - 你的对话数据可能被模型提供商存储或用于训练

### 我们做了什么

- ✅ 显示时对 Key 进行脱敏（只显示前 8 位）
- ✅ 操作前需要用户确认
- ❌ 无法阻止 Key 作为上下文发送给模型

**如果你对隐私有严格要求，请不要使用本技能，直接在 CC Switch 界面操作。**

## 依赖

- Python 3.6+（用于 SQLite 操作）
- SQLite3（Python 内置）

## 跨平台支持

- ✅ Windows
- ✅ macOS
- ✅ Linux

**注意：** 
- macOS/Linux 使用 `python3` 命令
- Windows 使用 `python` 命令
- 如果不确定，先运行 `python3 --version` 或 `python --version` 检查

## 文件结构

```
acc-switch/
├── README.md              # 项目说明
├── SKILL.md               # 技能文件（AI 读取）
├── LICENSE                 # MIT 许可证
├── .gitignore
├── src/
│   └── db_helper.py       # 参考模板（不是固定命令集）
├── docs/
│   ├── DATABASE_SCHEMA.md # 数据库结构文档
│   └── EXAMPLES.md        # 使用示例
└── install/
    ├── install.sh         # macOS/Linux 安装脚本
    └── install.bat        # Windows 安装脚本
```

## 许可证

MIT
