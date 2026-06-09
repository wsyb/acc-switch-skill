#!/bin/bash
# acc-switch 安装脚本
# 支持：macOS, Linux

set -e

# 使用方式：bash install.sh [github_url]
REPO_URL="${1:-https://github.com/your-username/acc-switch.git}"
INSTALL_DIR="$HOME/.claude/skills/acc-switch"

echo "=== acc-switch 安装 ==="
echo "仓库: $REPO_URL"
echo "目标: $INSTALL_DIR"
echo ""

# 检查 Python
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
else
    echo "❌ 未找到 Python，请先安装 Python 3.6+"
    echo "  macOS: brew install python3"
    echo "  Ubuntu/Debian: sudo apt install python3"
    exit 1
fi

echo "✅ Python: $($PYTHON_CMD --version)"

# 克隆仓库
if [ -d "$INSTALL_DIR" ]; then
    echo "⚠️ 目录已存在，更新中..."
    cd "$INSTALL_DIR"
    git pull
else
    echo "📥 克隆仓库..."
    git clone "$REPO_URL" "$INSTALL_DIR"
fi

# 测试
echo "🧪 测试..."
cd "$INSTALL_DIR"
$PYTHON_CMD src/db_helper.py --help > /dev/null 2>&1

echo ""
echo "✅ 安装完成！"
echo ""
echo "使用方法："
echo "  在 Claude Code / Codex / Gemini 等工具中直接说："
echo "  'doctor 一下' 或 '列出所有 provider'"
echo ""
echo "手动测试："
echo "  cd $INSTALL_DIR"
echo "  $PYTHON_CMD src/db_helper.py doctor"
