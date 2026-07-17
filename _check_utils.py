"""
所有章节的 exercises.py 共用的小校验工具。
不用管这个文件里的实现细节,你只需要知道:
每道题写完后,运行该章节的 exercises.py,就会看到 PASS / FAIL 的结果。
"""

import os

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")

_total = 0
_passed = 0


def check(name, condition):
    """打印一道题的校验结果。condition 为 True 表示通过。"""
    global _total, _passed
    _total += 1
    if condition:
        _passed += 1
        print(f"[PASS] {name}")
    else:
        print(f"[FAIL] {name}")
    return condition


def check_eq(name, actual, expected):
    """校验 actual 是否等于 expected(自动打印出两者方便你排错)。"""
    ok = actual == expected
    # 有些结果(比如 DataFrame/Series)比较结果不是单个 bool,这里做个兼容
    try:
        ok = bool(ok)
    except ValueError:
        ok = bool(ok.all()) if hasattr(ok, "all") else bool(ok)
    if not ok:
        print(f"      期望: {expected!r}")
        print(f"      实际: {actual!r}")
    return check(name, ok)


def summary():
    print("-" * 40)
    print(f"通过 {_passed} / {_total} 题")
    if _passed == _total and _total > 0:
        print("全部通过,可以进入下一章了。")
    else:
        print("还有题没通过,回去看 notes.md 或者对照 solutions.py 修改。")
