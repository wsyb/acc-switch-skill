# acc-switch

> 老板只说要什么，保姆搞定 CC Switch 配置。具体软件配置由 CC Switch 自己同步。

## ⚠️ 安全警告

**API Key 会上传到大语言模型！**

本技能会读取数据库中的 API Key 并发送给 AI 模型。虽然显示时做了脱敏（前 8 位），但完整 Key 会作为上下文发送给模型提供商。

**建议：**
- 敏感 Key 请手动在 CC Switch 界面操作
- 使用后建议轮换 Key
- 使用专用测试 Key，不要用生产 Key

## 核心原则

1. **先确认，后执行** - 每次操作前必须向用户展示计划并获得确认
2. **动态生成代码** - 不要使用固定命令，根据用户需求动态生成 Python 代码
3. **只操作数据库** - 不直接修改具体软件的配置文件
4. **提醒同步** - 操作后必须提醒用户重启 CC Switch 或手动同步
5. **使用参数化查询** - SQL 必须使用 `?` 占位符，防止注入
6. **使用上下文管理器** - 数据库连接用 `with` 语句，确保安全关闭
7. **JSON 语法检查** - 写入前必须验证 JSON 语法正确（`json.loads` 能成功解析）

## 触发条件

当用户提到以下关键词时激活：
- 配置、设置、config、setup
- provider、提供商、key、api key、url
- MCP、mcp server、扩展、插件、plugin、skill
- 清理、删除、remove、clean
- 诊断、修复、doctor、fix
- 同步、sync
- 截图配置、从浏览器获取

## 配置目录

CC Switch 配置目录默认为 `~/.cc-switch`，但用户可能自定义。

**查找策略：**
1. 检查默认路径 `~/.cc-switch/cc-switch.db`
2. 如果不存在，询问用户：
   > 找不到 CC Switch 配置目录，请告诉我路径（通常是 `~/.cc-switch`）

## 支持的平台

CC Switch 支持以下 AI Agent 平台：

| 平台 | app_type | 说明 |
|------|----------|------|
| Claude Code | claude | Anthropic Claude |
| Codex | codex | OpenAI Codex |
| Gemini CLI | gemini | Google Gemini |
| OpenCode | opencode | OpenCode |
| Hermes | hermes | Hermes |

## 数据库结构

### providers 表

```sql
CREATE TABLE providers (
  id TEXT PRIMARY KEY,
  app_type TEXT,           -- 'claude', 'codex', 'gemini', 'opencode', 'hermes'
  name TEXT,               -- 显示名称，如 'Xiaomi MiMo'
  settings_config TEXT,    -- JSON，包含 env、hooks 等完整配置
  website_url TEXT,
  category TEXT,           -- 'official', 'cn_official', 'aggregator'
  provider_type TEXT,      -- 'xiaomimimo', 'zhipu', 'nvidia', etc.
  is_current BOOLEAN,      -- 是否当前使用
  in_failover_queue BOOLEAN,
  cost_multiplier TEXT,
  limit_daily_usd TEXT,
  limit_monthly_usd TEXT,
  created_at INTEGER,
  sort_index INTEGER,
  notes TEXT,
  icon TEXT,
  icon_color TEXT,
  meta TEXT
);
```

### mcp_servers 表

```sql
CREATE TABLE mcp_servers (
  id TEXT PRIMARY KEY,
  name TEXT,
  server_config TEXT,      -- JSON: {type, command, args, url, headers, env}
  description TEXT,
  homepage TEXT,
  docs TEXT,
  tags TEXT,
  enabled_claude BOOLEAN,
  enabled_codex BOOLEAN,
  enabled_gemini BOOLEAN,
  enabled_opencode BOOLEAN,
  enabled_hermes BOOLEAN
);
```

### skills 表

```sql
CREATE TABLE skills (
  id TEXT PRIMARY KEY,
  name TEXT,
  description TEXT,
  directory TEXT,
  repo_owner TEXT,
  repo_name TEXT,
  repo_branch TEXT,
  readme_url TEXT,
  enabled_claude BOOLEAN,
  enabled_codex BOOLEAN,
  enabled_gemini BOOLEAN,
  enabled_opencode BOOLEAN,
  enabled_hermes BOOLEAN,
  installed_at INTEGER,
  content_hash TEXT,
  updated_at INTEGER
);
```

### settings 表

```sql
CREATE TABLE settings (
  key TEXT PRIMARY KEY,
  value TEXT
);
```

## 操作流程

### 第一步：理解需求

收到用户需求后，先理解用户想要做什么。

### 第二步：查询现状

在执行任何操作前，先查询当前状态（使用参数化查询）：

```python
import sqlite3, os, json

db_path = os.path.expanduser('~/.cc-switch/cc-switch.db')

with sqlite3.connect(db_path) as conn:
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # ✅ 正确：使用参数化查询
    cursor.execute("SELECT * FROM providers WHERE name LIKE ?", (f'%{keyword}%',))
    rows = cursor.fetchall()
```

### 第三步：展示计划

向用户展示将要执行的操作。

### 第四步：获得确认

等待用户确认后才执行。如果用户说"直接执行"或"确认"，则继续。

### 第五步：执行操作

根据用户需求动态生成 Python 代码执行操作。

**重要：所有 SQL 必须使用参数化查询！**

```python
import sqlite3, os, json

db_path = os.path.expanduser('~/.cc-switch/cc-switch.db')

with sqlite3.connect(db_path) as conn:
    cursor = conn.cursor()

    # ✅ 正确：参数化查询
    cursor.execute("SELECT name FROM mcp_servers WHERE name = ?", ('fetch',))

    # ✅ 正确：参数化插入
    config = {"type": "stdio", "command": "npx", "args": ["-y", "@anthropic/fetch-mcp"]}
    cursor.execute("""
        INSERT OR REPLACE INTO mcp_servers 
        (id, name, server_config, enabled_claude)
        VALUES (?, ?, ?, ?)
    """, ('fetch', 'fetch', json.dumps(config), 1))

    # ✅ 正确：参数化删除
    cursor.execute("DELETE FROM providers WHERE name LIKE ?", (f'%{keyword}%',))

    conn.commit()
```

**❌ 错误示例（不要这样写）：**
```python
# ❌ SQL 注入风险！
cursor.execute(f"SELECT * FROM providers WHERE name LIKE '%{keyword}%'")
cursor.execute("DELETE FROM mcp_servers WHERE name LIKE '%nvidia%'")
```

### 第六步：提醒同步

操作完成后，必须提醒用户：

```
✅ 操作完成！

⚠️ 重要：配置已写入数据库，但尚未同步到具体软件。

请执行以下操作之一使配置生效：

选项 1（推荐）：重启 CC Switch
  - 关闭 CC Switch
  - 重新打开 CC Switch

选项 2：在 CC Switch 界面手动同步
  - 打开 CC Switch 界面
  - 点击"应用"或"保存"按钮
```

## 动态代码生成示例

### 示例 1：用户说"给我配置 mimo"

```python
import sqlite3, os, json

db_path = os.path.expanduser('~/.cc-switch/cc-switch.db')

with sqlite3.connect(db_path) as conn:
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # ✅ 参数化查询
    cursor.execute("SELECT * FROM providers WHERE name LIKE ?", ('%mimo%',))
    rows = cursor.fetchall()

    if rows:
        print("找到现有配置：")
        for row in rows:
            print(f"  - {row['name']} ({row['app_type']})")
    else:
        print("未找到 mimo 配置")
```

### 示例 2：用户说"删除所有 nvidia 的 provider"

```python
import sqlite3, os

db_path = os.path.expanduser('~/.cc-switch/cc-switch.db')

with sqlite3.connect(db_path) as conn:
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # ✅ 参数化查询
    cursor.execute("SELECT name, app_type FROM providers WHERE name LIKE ?", ('%nvidia%',))
    rows = cursor.fetchall()

    print("将要删除的 Provider：")
    for row in rows:
        print(f"  - {row['name']} ({row['app_type']})")

    # 等待用户确认后执行
    # cursor.execute("DELETE FROM providers WHERE name LIKE ?", ('%nvidia%',))
    # conn.commit()
```

### 示例 3：用户说"添加一个 fetch MCP"

```python
import sqlite3, os, json

db_path = os.path.expanduser('~/.cc-switch/cc-switch.db')

with sqlite3.connect(db_path) as conn:
    cursor = conn.cursor()

    # ✅ 参数化查询
    cursor.execute("SELECT name FROM mcp_servers WHERE name = ?", ('fetch',))
    if cursor.fetchone():
        print("MCP 'fetch' 已存在")
    else:
        config = {
            "type": "stdio",
            "command": "npx",
            "args": ["-y", "@anthropic/fetch-mcp"]
        }

        # ✅ 参数化插入
        cursor.execute("""
            INSERT INTO mcp_servers 
            (id, name, server_config, enabled_claude)
            VALUES (?, ?, ?, ?)
        """, ('fetch', 'fetch', json.dumps(config), 1))

        conn.commit()
        print("已添加 MCP: fetch")
```

## 安全规范

1. **API Key 脱敏** - 只显示前 8 位 + `...`
2. **操作前确认** - 必须获得用户确认
3. **自动备份** - 修改前调用 `backup_db()` 备份数据库
4. **检查运行状态** - 操作前检查 CC Switch 是否在运行
5. **参数化查询** - 所有 SQL 必须使用 `?` 占位符
6. **上下文管理器** - 使用 `with sqlite3.connect()` 确保连接安全关闭

## 输出规范

### 操作计划
```
📋 操作计划

当前状态：...
将要执行：...

确认执行吗？
```

### 操作成功
```
✅ 操作完成！

⚠️ 重要：配置已写入数据库，但尚未同步到具体软件。
请重启 CC Switch 或在界面中手动同步。
```

### 操作失败
```
❌ 操作失败：<原因>
建议：<修复方案>
```

### 诊断报告
```
📋 CC Switch 配置诊断

✅ 正常：...
⚠️ 警告：...
❌ 错误：...

要我修复吗？
```
