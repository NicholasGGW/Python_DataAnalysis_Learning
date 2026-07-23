@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion
cd /d "%~dp0"
title 准备离线包(在有网的机器上跑一次)

echo ================================================
echo   准备离线包 —— 把 Pyodide 和便携 Python 下载进项目
echo   请在一台【有网】的机器上运行(国内镜像,速度较快)。
echo   跑完后把整个项目文件夹拷到离线机器,双击 启动网页学习.bat 即可。
echo ================================================
echo.

set "PY="
REM 1) 优先用项目里已经有的便携 Python
if exist "%~dp0runtime\win-python\python.exe" set "PY=%~dp0runtime\win-python\python.exe"
REM 2) 其次用系统 Python
if not defined PY ( where python >nul 2>nul && set "PY=python" )
if not defined PY ( where py >nul 2>nul && set "PY=py" )

REM 3) 都没有的话,先从国内镜像(npmmirror)引导一个便携 Python 出来
if not defined PY (
    echo 未检测到 Python,先从 npmmirror 镜像下载一个便携版 Python(约 10MB)...
    set "PYZIP=%TEMP%\py-embed.zip"
    set "PYDIR=%~dp0runtime\win-python"
    powershell -NoProfile -Command "try { [Net.ServicePointManager]::SecurityProtocol=[Net.SecurityProtocolType]::Tls12; Invoke-WebRequest -Uri 'https://registry.npmmirror.com/-/binary/python/3.12.4/python-3.12.4-embed-amd64.zip' -OutFile '!PYZIP!' } catch { exit 1 }"
    if not exist "!PYZIP!" (
        echo 下载便携 Python 失败,请检查网络后重试,或先手动装个 Python 再跑本文件。
        pause & exit /b 1
    )
    powershell -NoProfile -Command "Expand-Archive -Force -Path '!PYZIP!' -DestinationPath '!PYDIR!'"
    del "!PYZIP!" >nul 2>nul
    REM 打开 embeddable python 的 site,让它能正常跑脚本
    powershell -NoProfile -Command "Get-ChildItem '!PYDIR!\*._pth' | ForEach-Object { (Get-Content $_.FullName) -replace '#import site','import site' | Set-Content $_.FullName }"
    set "PY=!PYDIR!\python.exe"
    echo 便携 Python 就绪: !PY!
)

echo.
echo 正在下载 Pyodide(含 numpy / pandas)和便携 Python...
echo.
"!PY!" "%~dp0tools\prepare_offline.py"
set "RC=!errorlevel!"

echo.
if "!RC!"=="0" (
    echo ================================================
    echo   离线包准备完成!现在可以断网,双击 启动网页学习.bat 试试。
    echo   把整个项目文件夹拷到别的离线机器也能直接用。
    echo ================================================
) else (
    echo 准备过程出错(错误码 !RC!)。常见原因: 网络不稳定,重试一次通常就好;
    echo 或用参数指定源,例如在命令行运行:
    echo   "!PY!" tools\prepare_offline.py --pyodide-base https://fastly.jsdelivr.net/pyodide/v0.26.4/full/
)
echo.
pause
