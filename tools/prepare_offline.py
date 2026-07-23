"""
一键准备"离线包": 把网页运行 Python 所需的 Pyodide(含 numpy / pandas)
和 Windows 便携版 Python 解释器下载到项目里,之后整个项目拷到没网的机器上也能跑。

用法(在一台**有网**的机器上跑一次即可):
    python tools/prepare_offline.py            # 正式下载
    python tools/prepare_offline.py --dry-run  # 只打印将要下载的东西,不真正下载
    python tools/prepare_offline.py --pyodide-base https://cdn.jsdelivr.net/pyodide/v0.26.4/full/

下载源默认优先用**中国大陆访问较快的镜像**(npmmirror / 华为云 / jsdelivr 的 gcore、fastly 节点),
某个源慢或连不上会自动换下一个。

下载完成后会得到:
    web/vendor/pyodide/      —— 浏览器端离线运行 Python 用(pyodide + numpy + pandas)
    runtime/win-python/      —— Windows 上启动本地服务器用的便携 Python(免安装)

这两个目录默认不提交进 git(见 .gitignore),离线时把整个项目文件夹拷过去即可。
"""

import argparse
import json
import os
import platform
import shutil
import sys
import urllib.request
import zipfile

PYODIDE_VERSION = "0.26.4"
PYTHON_VERSION = "3.12.4"

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
PYODIDE_DIR = os.path.join(ROOT, "web", "vendor", "pyodide")
WINPY_DIR = os.path.join(ROOT, "runtime", "win-python")

# Pyodide 的 full/ 目录镜像(按顺序尝试,靠前的在国内一般更快)
PYODIDE_MIRRORS = [
    f"https://gcore.jsdelivr.net/pyodide/v{PYODIDE_VERSION}/full/",
    f"https://fastly.jsdelivr.net/pyodide/v{PYODIDE_VERSION}/full/",
    f"https://testingcf.jsdelivr.net/pyodide/v{PYODIDE_VERSION}/full/",
    f"https://cdn.jsdelivr.net/pyodide/v{PYODIDE_VERSION}/full/",
]

# Windows 便携版(embeddable)Python 的镜像(npmmirror / 华为云都镜像了 python.org/ftp)
PY_EMBED_NAME = f"python-{PYTHON_VERSION}-embed-amd64.zip"
PYTHON_MIRRORS = [
    f"https://registry.npmmirror.com/-/binary/python/{PYTHON_VERSION}/",
    f"https://mirrors.huaweicloud.com/python/{PYTHON_VERSION}/",
    f"https://www.python.org/ftp/python/{PYTHON_VERSION}/",
]

# Pyodide 加载器必需的核心文件
CORE_FILES = [
    "pyodide.js",
    "pyodide.asm.js",
    "pyodide.asm.wasm",
    "python_stdlib.zip",
    "pyodide-lock.json",
]
# 我们只需要这几个库(以及它们的依赖会从 lock 文件里自动解析出来)
WANT_PACKAGES = ["numpy", "pandas"]


def log(*a):
    print(*a, flush=True)


def human(n):
    for unit in ("B", "KB", "MB", "GB"):
        if n < 1024 or unit == "GB":
            return f"{n:.1f}{unit}"
        n /= 1024


def fetch_bytes(url, timeout=60):
    req = urllib.request.Request(url, headers={"User-Agent": "prepare-offline/1.0"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def download_to(url, dest, timeout=120):
    """下载 url 到 dest,返回字节数。"""
    req = urllib.request.Request(url, headers={"User-Agent": "prepare-offline/1.0"})
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    with urllib.request.urlopen(req, timeout=timeout) as r, open(dest, "wb") as f:
        shutil.copyfileobj(r, f)
    return os.path.getsize(dest)


def try_mirrors(mirrors, filename):
    """按顺序在多个镜像里找 filename,返回 (可用的 base_url) 或抛异常。"""
    last = None
    for base in mirrors:
        url = base + filename
        try:
            req = urllib.request.Request(url, method="HEAD",
                                         headers={"User-Agent": "prepare-offline/1.0"})
            with urllib.request.urlopen(req, timeout=20):
                return base
        except Exception as e:  # noqa: BLE001
            last = e
            log(f"  镜像不可用,换下一个: {base}  ({e})")
    raise RuntimeError(f"所有镜像都拿不到 {filename}: {last}")


def resolve_wheels(lock_bytes):
    """从 pyodide-lock.json 里,解析出 numpy/pandas 及其全部依赖的 wheel 文件名。"""
    lock = json.loads(lock_bytes)
    packages = lock["packages"]
    # lock 里的 key 是小写包名
    want, seen, files = list(WANT_PACKAGES), set(), []
    while want:
        name = want.pop().lower()
        if name in seen or name not in packages:
            continue
        seen.add(name)
        info = packages[name]
        files.append(info["file_name"])
        for dep in info.get("depends", []):
            want.append(dep.lower())
    return sorted(set(files))


def prepare_pyodide(dry_run, override_base):
    log("== 准备 Pyodide(浏览器端离线运行 Python)==")
    if override_base:
        base = override_base if override_base.endswith("/") else override_base + "/"
        log(f"使用指定源: {base}")
    else:
        base = None

    if dry_run:
        log(f"将下载核心文件到 {PYODIDE_DIR}:")
        for f in CORE_FILES:
            log(f"  - {f}")
        log(f"并根据 pyodide-lock.json 解析 {WANT_PACKAGES} 及其依赖的 wheel 一并下载。")
        log(f"候选镜像: {(override_base and [base]) or PYODIDE_MIRRORS}")
        return

    if base is None:
        log("挑选可用镜像中...")
        base = try_mirrors(PYODIDE_MIRRORS, "pyodide-lock.json")
    log(f"使用源: {base}")

    os.makedirs(PYODIDE_DIR, exist_ok=True)
    total = 0
    # 先拿 lock 文件解析出需要哪些 wheel
    lock_bytes = fetch_bytes(base + "pyodide-lock.json")
    wheels = resolve_wheels(lock_bytes)
    log(f"需要的库文件({len(wheels)} 个): {', '.join(wheels)}")

    for name in CORE_FILES + wheels:
        dest = os.path.join(PYODIDE_DIR, name)
        if os.path.exists(dest) and os.path.getsize(dest) > 0:
            log(f"  已存在,跳过: {name}")
            total += os.path.getsize(dest)
            continue
        log(f"  下载: {name} ...")
        total += download_to(base + name, dest)
    log(f"Pyodide 就绪,占用 {human(total)} -> {PYODIDE_DIR}")


def prepare_win_python(dry_run):
    log("== 准备 Windows 便携版 Python(启动本地服务器用,免安装)==")
    marker = os.path.join(WINPY_DIR, "python.exe")
    if os.path.exists(marker):
        log(f"  已存在,跳过: {WINPY_DIR}")
        return
    if dry_run:
        log(f"将从下列镜像下载 {PY_EMBED_NAME} 并解压到 {WINPY_DIR}:")
        for b in PYTHON_MIRRORS:
            log(f"  - {b}{PY_EMBED_NAME}")
        return

    base = try_mirrors(PYTHON_MIRRORS, PY_EMBED_NAME)
    log(f"使用源: {base}")
    os.makedirs(WINPY_DIR, exist_ok=True)
    zip_path = os.path.join(WINPY_DIR, PY_EMBED_NAME)
    size = download_to(base + PY_EMBED_NAME, zip_path)
    log(f"  下载完成 {human(size)},解压中...")
    with zipfile.ZipFile(zip_path) as z:
        z.extractall(WINPY_DIR)
    os.remove(zip_path)
    # 打开 embeddable python 的 site,允许 http.server 正常工作
    for name in os.listdir(WINPY_DIR):
        if name.endswith("._pth"):
            p = os.path.join(WINPY_DIR, name)
            txt = open(p, encoding="utf-8").read()
            if "#import site" in txt:
                open(p, "w", encoding="utf-8").write(txt.replace("#import site", "import site"))
    log(f"便携 Python 就绪 -> {WINPY_DIR}")


def main():
    ap = argparse.ArgumentParser(description="下载 Pyodide + 便携 Python,做成离线包")
    ap.add_argument("--dry-run", action="store_true", help="只打印计划,不真正下载")
    ap.add_argument("--pyodide-base", default=None, help="自定义 Pyodide full/ 目录 URL")
    ap.add_argument("--skip-python", action="store_true", help="不下载 Windows 便携 Python")
    args = ap.parse_args()

    log(f"项目根目录: {ROOT}")
    log(f"当前系统: {platform.system()} {platform.machine()}")
    log("")
    prepare_pyodide(args.dry_run, args.pyodide_base)
    log("")
    if not args.skip_python:
        prepare_win_python(args.dry_run)
    log("")
    if args.dry_run:
        log("(这是 --dry-run,没有真正下载。去掉 --dry-run 即可正式下载。)")
    else:
        log("全部完成!现在把整个项目文件夹拷到离线机器,双击 启动网页学习.bat 即可离线运行。")


if __name__ == "__main__":
    main()
