# acc-switch - 常用场景示例

> **重要：** 所有操作前必须先向用户展示计划并获得确认！
> 修改数据库后，必须提醒用户重启 CC Switch 或手动同步！
> **所有 SQL 必须使用参数化查询（`?` 占位符），防止注入！**

## 场景 1: 配置新的 Provider

**用户说：**
> 这是我的 key: sk-xxx123456789，url 是 https://api.example.com/v1，给我配上

**AI 做：**

1. 备份并查询现有配置：
```python
import sqlite3, os, json, shutil
from datetime import datetime

db_path = os.path.expanduser('~/.cc-switch/cc-switch.db')

# 备份
backup_dir = os.path.join(os.path.dirname(db_path), 'backups')
os.makedirs(backup_dir, exist_ok=True)
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
shutil.copy2(db_path, os.path.join(backup_dir, f'db_backup_{timestamp}.db'))

with sqlite3.connect(db_path) as conn:
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # ✅ 参数化查询
    cursor.execute("SELECT * FROM providers WHERE name LIKE ?", ('%example%',))
    rows = cursor.fetchall()

    if rows:
        print("找到现有配置：")
        for row in rows:
            print(f"  - {row['name']} ({row['app_type']})")
    else:
        print("未找到相关配置")
```

2. 展示计划并获得确认

3. 执行操作（用户确认后）：
```python
import sqlite3, os, json, uuid

db_path = os.path.expanduser('~/.cc-switch/cc-switch.db')

with sqlite3.connect(db_path) as conn:
    cursor = conn.cursor()

    provider_id = str(uuid.uuid4())
    config = {
        "env": {
            "ANTHROPIC_AUTH_TOKEN": "sk-xxx123456789",
            "ANTHROPIC_BASE_URL": "https://api.example.com/v1"
        }
    }

    # ✅ 参数化插入
    cursor.execute("""
        INSERT INTO providers (id, app_type, name, settings_config, is_current)
        VALUES (?, ?, ?, ?, ?)
    """, (provider_id, 'claude', 'my-provider', json.dumps(config), 0))

    conn.commit()
    print("✅ 已添加 Provider: my-provider")
```

4. 提醒同步

---

## 场景 2: 添加 MCP 服务器

**用户说：**
> 给我加一个 fetch MCP，npm 包是 @anthropic/fetch-mcp

**AI 做：**

1. 备份并查询现有 MCP：
```python
import sqlite3, os, shutil
from datetime import datetime

db_path = os.path.expanduser('~/.cc-switch/cc-switch.db')

# 备份
backup_dir = os.path.join(os.path.dirname(db_path), 'backups')
os.makedirs(backup_dir, exist_ok=True)
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
shutil.copy2(db_path, os.path.join(backup_dir, f'db_backup_{timestamp}.db'))

with sqlite3.connect(db_path) as conn:
    cursor = conn.cursor()

    # ✅ 参数化查询
    cursor.execute("SELECT name FROM mcp_servers WHERE name = ?", ('fetch',))
    if cursor.fetchone():
        print("MCP 'fetch' 已存在")
    else:
        print("MCP 'fetch' 不存在，可以添加")
```

2. 展示计划并获得确认

3. 执行操作（用户确认后）：
```python
import sqlite3, os, json

db_path = os.path.expanduser('~/.cc-switch/cc-switch.db')

with sqlite3.connect(db_path) as conn:
    cursor = conn.cursor()

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
    print("✅ 已添加 MCP: fetch")
```

4. 提醒同步

---

## 场景 3: 批量清理

**用户说：**
> 所有智谱相关的 MCP 都不要了，给我清理干净

**AI 做：**

1. 备份并查询匹配的 MCP：
```python
import sqlite3, os, shutil
from datetime import datetime

db_path = os.path.expanduser('~/.cc-switch/cc-switch.db')

# 备份
backup_dir = os.path.join(os.path.dirname(db_path), 'backups')
os.makedirs(backup_dir, exist_ok=True)
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
shutil.copy2(db_path, os.path.join(backup_dir, f'db_backup_{timestamp}.db'))

with sqlite3.connect(db_path) as conn:
    cursor = conn.cursor()

    # ✅ 参数化查询
    cursor.execute("""
        SELECT name FROM mcp_servers 
        WHERE name LIKE ? OR name LIKE ? OR name LIKE ? OR name LIKE ?
    """, ('%zread%', '%zai%', '%web-search%', '%web-reader%'))
    rows = cursor.fetchall()

    print("找到以下匹配的 MCP：")
    for row in rows:
        print(f"  - {row[0]}")
```

2. 展示计划并获得确认

3. 执行操作（用户确认后）：
```python
import sqlite3, os

db_path = os.path.expanduser('~/.cc-switch/cc-switch.db')

with sqlite3.connect(db_path) as conn:
    cursor = conn.cursor()

    # ✅ 参数化删除
    cursor.execute("""
        DELETE FROM mcp_servers 
        WHERE name LIKE ? OR name LIKE ? OR name LIKE ? OR name LIKE ?
    """, ('%zread%', '%zai%', '%web-search%', '%web-reader%'))
    count = cursor.rowcount
    conn.commit()

    print(f"✅ 已删除 {count} 个 MCP")
```

4. 提醒同步

---

## 场景 4: 配置诊断

**用户说：**
> 给我 doctor 一下，看看配置有没有问题

**AI 做：**

```python
import sqlite3, os, json

db_path = os.path.expanduser('~/.cc-switch/cc-switch.db')

with sqlite3.connect(db_path) as conn:
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    print("📋 CC Switch 配置诊断")
    print()

    # 数据库完整性
    print("--- 数据库完整性 ---")
    cursor.execute("PRAGMA integrity_check")
    result = cursor.fetchone()
    if result[0] == "ok":
        print("✅ 数据库完整")
    else:
        print(f"❌ 数据库损坏: {result[0]}")

    # Providers
    print()
    print("--- Providers ---")
    cursor.execute("SELECT name, app_type, is_current FROM providers ORDER BY sort_index")
    rows = cursor.fetchall()
    if rows:
        for row in rows:
            current = " [当前]" if row["is_current"] else ""
            print(f"  {row['name']} ({row['app_type']}){current}")
    else:
        print("  (无)")

    # MCP Servers
    print()
    print("--- MCP Servers ---")
    cursor.execute("""
        SELECT name, enabled_claude, enabled_codex, enabled_gemini, enabled_opencode, enabled_hermes
        FROM mcp_servers
    """)
    rows = cursor.fetchall()
    if rows:
        for row in rows:
            platforms = []
            if row["enabled_claude"]: platforms.append("claude")
            if row["enabled_codex"]: platforms.append("codex")
            if row["enabled_gemini"]: platforms.append("gemini")
            if row["enabled_opencode"]: platforms.append("opencode")
            if row["enabled_hermes"]: platforms.append("hermes")
            print(f"  {row['name']} [{', '.join(platforms)}]")
    else:
        print("  (无)")

    # CC Switch 状态
    print()
    print("--- CC Switch 状态 ---")
    import subprocess, sys
    try:
        if sys.platform == "win32":
            result = subprocess.run(["tasklist"], capture_output=True, text=True)
            running = "cc-switch.exe" in result.stdout.lower()
        else:
            result = subprocess.run(["pgrep", "-x", "cc-switch"], capture_output=True)
            running = result.returncode == 0
    except:
        running = False

    if running:
        print("⚠️ CC Switch 正在运行")
    else:
        print("✅ CC Switch 未运行")
```

---

## 场景 5: 从浏览器获取配置

**用户说：**
> 我在 mimo 网站上登录了，帮我把 key 和 url 配上

**AI 做：**

1. 使用 chrome-devtools MCP 连接浏览器
2. 导航到 mimo 的 API 管理页面
3. 提取 key 和 url
4. 展示计划并获得确认
5. 写入 CC Switch 数据库（使用参数化查询）
6. 提醒同步

---

## 场景 6: 推荐扩展

**用户说：**
> 分析一下我的项目目录，推荐一些有用的 MCP

**AI 做：**

1. 分析项目类型（Rust、Flutter、Node.js 等）
2. 检查 CC Switch 数据库中已有的 MCP
3. 推荐缺失的工具
4. 展示计划并获得确认
5. 添加到 CC Switch 数据库（使用参数化查询）
6. 提醒同步

---

## 场景 7: 截图配置

**用户说：**
> [粘贴截图] 看这个截图，给我配上

**AI 做：**

1. 识别截图中的关键信息
2. 展示识别结果并获得确认
3. 写入 CC Switch 数据库（使用参数化查询）
4. 提醒同步

---

## 场景 8: 一键重置

**用户说：**
> 配置太乱了，给我重置到最干净的状态

**AI 做：**

1. 备份当前数据库
2. 展示将要清空的内容
3. 获得确认
4. 清空 MCP 和 Provider 表（使用参数化查询）
5. 只添加用户指定的配置
6. 提醒同步

---

## 场景 9: 跨工具配置复制

**用户说：**
> codex 的 provider 配置挺好，我也想在 claude 里用

**AI 做：**

1. 查询 CC Switch 数据库中 codex 的 provider（使用参数化查询）
2. 展示将要复制的内容
3. 获得确认
4. 复制一份，app_type 改为 claude
5. 插入数据库（使用参数化查询）
6. 提醒同步

---

## 场景 10: 批量导入

**用户说：**
> 我有一批 MCP 配置，帮我导入

**AI 做：**

1. 读取用户提供的配置列表
2. 验证格式
3. 展示将要导入的内容
4. 获得确认
5. 批量写入 CC Switch 数据库（使用参数化查询）
6. 报告导入结果
7. 提醒同步
