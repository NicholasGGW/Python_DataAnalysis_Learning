@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion
cd /d "%~dp0"
title Python 数据分析学习 - 网页启动器

echo ================================================
echo   Python 数据分析学习 - 网页学习模式启动器
echo ================================================
echo.

REM ---------- 1. 检测 Python ----------
set "PY="

REM 1a. 最优先: 项目自带的便携 Python(离线包,免安装)
if exist "%~dp0runtime\win-python\python.exe" (
    set "PY=%~dp0runtime\win-python\python.exe"
    echo [1/3] 使用项目自带的便携 Python(离线包)
    goto :run
)

REM 1b. 其次: 系统已装的 Python
where python >nul 2>nul && set "PY=python"
if not defined PY (
    where py >nul 2>nul && set "PY=py"
)

if defined PY (
    echo [1/3] 已检测到系统 Python: !PY!
    goto :run
)

echo [1/3] 未检测到 Python。
echo 提示: 想做到"离线开箱即用",可以先在有网的机器上双击 "准备离线包.bat",
echo       它会把便携版 Python 和 Pyodide 下载进项目,之后拷到离线机器直接双击本文件即可。
echo.
echo 现在先尝试自动安装 Python...
echo.

REM ---------- 2. 优先用 winget 安装(Win10 较新版本自带) ----------
where winget >nul 2>nul
if !errorlevel! == 0 (
    echo 正在通过 winget 安装 Python 3.12,请在弹出的窗口里点"是"确认...
    winget install -e --id Python.Python.3.12 --accept-package-agreements --accept-source-agreements
) else (
    echo winget 不可用,改为从官网下载安装包...
    set "PYINSTALLER=%TEMP%\python-installer.exe"
    echo 正在下载 Python 安装包(约 25MB)...
    powershell -NoProfile -Command "try { [Net.ServicePointManager]::SecurityProtocol=[Net.SecurityProtocolType]::Tls12; Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.12.4/python-3.12.4-amd64.exe' -OutFile '!PYINSTALLER!' } catch { exit 1 }"
    if not exist "!PYINSTALLER!" (
        echo.
        echo 下载失败。请手动到 https://www.python.org/downloads/ 下载安装,
        echo 安装时记得勾选 "Add Python to PATH",装完后重新双击本文件。
        echo.
        pause
        exit /b 1
    )
    echo 正在静默安装 Python(勾选加入 PATH)...
    "!PYINSTALLER!" /passive InstallAllUsers=0 PrependPath=1 Include_test=0
)

echo.
echo Python 安装步骤已执行。正在重新检测...

REM ---------- 3. 重新检测(新装的 Python 可能还没进当前窗口的 PATH) ----------
set "PY="
where python >nul 2>nul && set "PY=python"
if not defined PY ( where py >nul 2>nul && set "PY=py" )

REM 再兜底找一下 Python 的默认安装目录
if not defined PY (
    for /d %%D in ("%LocalAppData%\Programs\Python\Python3*") do (
        if exist "%%D\python.exe" set "PY=%%D\python.exe"
    )
)

if not defined PY (
    echo.
    echo Python 已安装,但当前窗口还没识别到它。
    echo 这是正常现象 —— 请关闭本窗口,然后重新双击 "启动网页学习.bat" 即可。
    echo.
    pause
    exit /b 0
)

:run
echo [2/3] 正在启动本地服务器: !PY! -m http.server 8000
start "Python 学习服务器(关闭此窗口即停止)" cmd /k "!PY! -m http.server 8000"

echo [3/3] 3 秒后自动打开浏览器...
timeout /t 3 /nobreak >nul
start "" "http://localhost:8000/web/"

echo.
echo ================================================
echo   已启动!浏览器地址: http://localhost:8000/web/
echo   学习结束后,关闭那个"Python 学习服务器"黑窗口即可停止。
if exist "%~dp0web\vendor\pyodide\pyodide.js" (
    echo   检测到本地 Pyodide 离线包,网页端将离线运行,无需联网。
) else (
    echo   提示: 网页端 Python 目前仍需联网下载 Pyodide;想完全离线请先跑 "准备离线包.bat"。
)
echo ================================================
echo.
pause
