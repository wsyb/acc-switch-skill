#!/usr/bin/env python3
"""
acc-switch - CC Switch 数据库操作参考模板

注意：这是一个参考模板，不是固定命令集。
AI 应该根据用户需求动态生成 Python 代码，而不是直接调用这些函数。

使用方式：
- AI 会根据用户需求生成 Python 代码
- 代码会使用这个模板中的函数作为参考
- 执行前会向用户展示计划并获得确认
"""

import sqlite3
import os
import sys
import json
import shutil
from datetime import datetime
from pathlib import Path


def find_db():
    """查找 CC Switch 数据库"""
    home = Path.home()
    default_path = home / ".cc-switch" / "cc-switch.db"

    if default_path.exists():
        return str(default_path)

    possible_paths = [
        home / "AppData" / "Local" / "com.ccswitch.desktop" / "cc-switch.db",
        home / ".config" / "cc-switch" / "cc-switch.db",
    ]

    for path in possible_paths:
        if path.exists():
            return str(path)

    return None


def backup_db(db_path):
    """备份数据库"""
    backup_dir = os.path.join(os.path.dirname(db_path), "backups")
    os.makedirs(backup_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = os.path.join(backup_dir, f"db_backup_{timestamp}.db")

    shutil.copy2(db_path, backup_path)
    print(f"✅ 已备份到: {backup_path}")
    return backup_path


def is_cc_switch_running():
    """检查 CC Switch 是否在运行"""
    import subprocess
    try:
        if sys.platform == "win32":
            result = subprocess.run(["tasklist"], capture_output=True, text=True)
            return "cc-switch.exe" in result.stdout.lower()
        else:
            # 使用 pgrep -x 精确匹配进程名，避免误匹配
            result = subprocess.run(["pgrep", "-x", "cc-switch"], capture_output=True)
            return result.returncode == 0
    except Exception:
        return False


def kill_cc_switch():
    """关闭 CC Switch"""
    import subprocess
    try:
        if sys.platform == "win32":
            subprocess.run(["taskkill", "/F", "/IM", "cc-switch.exe"], capture_output=True)
        else:
            # 使用 pkill -x 精确匹配进程名，避免误杀其他进程
            subprocess.run(["pkill", "-x", "cc-switch"], capture_output=True)
        print("✅ 已关闭 CC Switch")
        return True
    except Exception as e:
        print(f"❌ 关闭失败: {e}")
        return False


def validate_json(json_str, name="配置"):
    """验证 JSON 字符串语法是否正确"""
    try:
        json.loads(json_str)
        return True, "JSON 格式正确"
    except json.JSONDecodeError as e:
        return False, f"{name} JSON 语法错误: {e}"


def print_sync_reminder():
    """打印同步提醒"""
    print()
    print("=" * 60)
    print("⚠️  重要：配置已写入数据库，但尚未同步到具体软件")
    print("=" * 60)
    print()
    print("请执行以下操作之一使配置生效：")
    print()
    print("选项 1（推荐）：重启 CC Switch")
    print("  - 关闭 CC Switch")
    print("  - 重新打开 CC Switch")
    print("  - CC Switch 会自动将数据库配置同步到各软件")
    print()
    print("选项 2：在 CC Switch 界面手动同步")
    print("  - 打开 CC Switch 界面")
    print("  - 找到刚修改的配置")
    print("  - 点击'应用'或'保存'按钮")
    print()
    print("选项 3：如果 CC Switch 未运行")
    print("  - 直接打开 CC Switch")
    print("  - 它会自动读取数据库并同步配置")
    print()
    print("=" * 60)


# ========== 以下是参考函数，AI 可以根据需求动态生成类似代码 ==========

def list_providers(db_path):
    """列出所有 Provider（参考）"""
    with sqlite3.connect(db_path) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, name, app_type, website_url, provider_type, is_current, sort_index
            FROM providers
            ORDER BY sort_index
        """)

        print("=== Providers ===")
        for row in cursor.fetchall():
            current = " [当前]" if row["is_current"] else ""
            print(f"  {row['name']} ({row['app_type']}){current}")


def show_provider(db_path, keyword):
    """显示 Provider 详情（参考）"""
    with sqlite3.connect(db_path) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, name, app_type, settings_config, website_url, provider_type, is_current
            FROM providers
            WHERE name LIKE ? OR id LIKE ?
        """, (f"%{keyword}%", f"%{keyword}%"))

        rows = cursor.fetchall()
        if not rows:
            print(f"❌ 找不到匹配 '{keyword}' 的 Provider")
            return

        for row in rows:
            print(f"\n📋 Provider: {row['name']}")
            print(f"  ID: {row['id']}")
            print(f"  类型: {row['app_type']}")
            print(f"  Provider: {row['provider_type'] or 'N/A'}")
            print(f"  网站: {row['website_url'] or 'N/A'}")
            print(f"  当前使用: {'是' if row['is_current'] else '否'}")

            try:
                config = json.loads(row["settings_config"])
                if "env" in config:
                    env = config["env"]
                    if "ANTHROPIC_AUTH_TOKEN" in env:
                        token = env["ANTHROPIC_AUTH_TOKEN"]
                        print(f"  API Key: {token[:8]}...")
                    if "ANTHROPIC_BASE_URL" in env:
                        print(f"  Base URL: {env['ANTHROPIC_BASE_URL']}")
                    if "ANTHROPIC_MODEL" in env:
                        print(f"  Model: {env['ANTHROPIC_MODEL']}")
            except (json.JSONDecodeError, TypeError):
                pass


def list_mcps(db_path):
    """列出所有 MCP（参考）"""
    with sqlite3.connect(db_path) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("""
            SELECT name, enabled_claude, enabled_codex, enabled_gemini, enabled_opencode, enabled_hermes
            FROM mcp_servers
        """)

        print("=== MCP Servers ===")
        for row in cursor.fetchall():
            platforms = []
            if row["enabled_claude"]:
                platforms.append("claude")
            if row["enabled_codex"]:
                platforms.append("codex")
            if row["enabled_gemini"]:
                platforms.append("gemini")
            if row["enabled_opencode"]:
                platforms.append("opencode")
            if row["enabled_hermes"]:
                platforms.append("hermes")
            print(f"  {row['name']} [{', '.join(platforms)}]")


def doctor(db_path):
    """诊断配置（参考）"""
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
                if row["enabled_claude"]:
                    platforms.append("claude")
                if row["enabled_codex"]:
                    platforms.append("codex")
                if row["enabled_gemini"]:
                    platforms.append("gemini")
                if row["enabled_opencode"]:
                    platforms.append("opencode")
                if row["enabled_hermes"]:
                    platforms.append("hermes")
                print(f"  {row['name']} [{', '.join(platforms)}]")
        else:
            print("  (无)")

        # 备份目录
        print()
        print("--- 备份目录 ---")
        backup_dir = os.path.join(os.path.dirname(db_path), "backups")
        if os.path.exists(backup_dir):
            total_size = sum(
                os.path.getsize(os.path.join(backup_dir, f))
                for f in os.listdir(backup_dir)
                if os.path.isfile(os.path.join(backup_dir, f))
            )
            print(f"  {backup_dir} ({total_size / 1024 / 1024:.1f} MB)")
        else:
            print("  不存在")

        # CC Switch 状态
        print()
        print("--- CC Switch 状态 ---")
        if is_cc_switch_running():
            print("⚠️ CC Switch 正在运行")
        else:
            print("✅ CC Switch 未运行")


def print_help():
    """打印帮助信息"""
    print("acc-switch - CC Switch 数据库操作参考模板")
    print()
    print("用法: python db_helper.py [命令]")
    print()
    print("命令:")
    print("  doctor      诊断配置")
    print("  list        列出所有 Provider 和 MCP")
    print("  --help, -h  显示此帮助信息")
    print()
    print("注意：这是一个参考模板，AI 会根据用户需求动态生成代码。")
    print()
    print("数据库位置：")
    db_path = find_db()
    if db_path:
        print(f"  {db_path}")
    else:
        print("  未找到")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="acc-switch - CC Switch 数据库操作参考模板")
    parser.add_argument("command", nargs="?", help="命令: doctor, list")
    args = parser.parse_args()

    if not args.command:
        print_help()
    elif args.command == "doctor":
        db_path = find_db()
        if db_path:
            doctor(db_path)
        else:
            print("❌ 找不到 CC Switch 数据库")
    elif args.command == "list":
        db_path = find_db()
        if db_path:
            list_providers(db_path)
            print()
            list_mcps(db_path)
        else:
            print("❌ 找不到 CC Switch 数据库")
    else:
        print(f"❌ 未知命令: {args.command}")
        print_help()
