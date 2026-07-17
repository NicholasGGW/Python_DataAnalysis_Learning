"""
所有章节的 exercises.py 共用的校验工具。

规则:
- 每道题对应一次 check_eq 调用,所以最后的统计就是"通过题数 / 总题数"。
- 不管通过与否,每道题都会打印出预期值和实际值,方便对照排错。

输出格式:
    [exercise1]
    预期: ...
    实际: ...
    结果: Pass!  (或 Failed.)
"""

import os

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")

_total = 0
_passed = 0


def check_eq(name, actual, expected):
    """校验一道题: actual 是否等于 expected。每道题只调用一次。"""
    global _total, _passed
    ok = actual == expected
    # DataFrame/Series/ndarray 的 == 返回的不是单个 bool,这里做兼容
    try:
        ok = bool(ok)
    except (ValueError, TypeError):
        ok = bool(ok.all()) if hasattr(ok, "all") else False

    _total += 1
    if ok:
        _passed += 1

    print(f"[{name}]")
    print(f"预期: {expected!r}")
    print(f"实际: {actual!r}")
    print(f"结果: {'Pass!' if ok else 'Failed.'}")
    print()
    return ok


def summary():
    print("=" * 40)
    print(f"通过 {_passed} / {_total} 题")
    if _passed == _total and _total > 0:
        print("全部通过,可以进入下一章了。")
    else:
        print("还有题没通过,回去看 notes.md 或者对照 solutions.py 修改。")
