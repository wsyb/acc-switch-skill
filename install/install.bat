@echo off
REM acc-switch 安装脚本 (Windows)
REM 使用方式：install.bat [github_url]

echo === acc-switch 安装 ===

REM 检查 Python
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo ❌ 未找到 Python，请先安装 Python 3.6+
    echo 下载地址: https://www.python.org/downloads/
    echo 安装时请勾选 "Add Python to PATH"
    pause
    exit /b 1
)

echo ✅ Python:
python --version

REM 设置参数
set REPO_URL=%1
if "%REPO_URL%"=="" set REPO_URL=https://github.com/your-username/acc-switch.git
set INSTALL_DIR=%USERPROFILE%\.claude\skills\acc-switch

echo 仓库: %REPO_URL%
echo 目标: %INSTALL_DIR%
echo.

REM 克隆仓库
if exist "%INSTALL_DIR%" (
    echo ⚠️ 目录已存在，更新中...
    cd /d "%INSTALL_DIR%"
    git pull
) else (
    echo 📥 克隆仓库...
    git clone "%REPO_URL%" "%INSTALL_DIR%"
)

REM 测试
echo 🧪 测试...
cd /d "%INSTALL_DIR%"
python src\db_helper.py --help >nul 2>nul

echo.
echo ✅ 安装完成！
echo.
echo 使用方法：
echo   在 Claude Code / Codex / Gemini 等工具中直接说：
echo   'doctor 一下' 或 '列出所有 provider'
echo.
echo 手动测试：
echo   cd %INSTALL_DIR%
echo   python src\db_helper.py doctor
pause
