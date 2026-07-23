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
import random

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")

_total = 0
_passed = 0

_SERIA_ALL_PASS = [
    "干得漂亮,勇士!全部通过,下一章的冒险也拜托你了!",
    "太厉害了!这波操作赛利亚给满分!",
    "全部通过!勇士,你离传说中的数据分析师又近了一步!",
    "完美通关!赛利亚为你骄傲!",
]
_SERIA_SOME_PASS = [
    "已经通过 {p} 题了,剩下的也一定没问题的,加油勇士!",
    "离全部通过只差一点点了!看看上面 Failed 的预期和实际,你能行的!",
    "不错不错,又前进了一步!剩下的题回去翻翻 notes.md 吧!",
]
_SERIA_ALL_FAIL = [
    "别灰心,勇士!先看看 notes.md 里的秘籍,再来挑战一次!",
    "万事开头难,赛利亚相信你!从第一题开始,一道一道来!",
]


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
    if _passed > 0:
        print("✨ " + "💰" * min(_passed, 10) + f"  金币 x{_passed} 掉落!✨")
    if _passed == _total and _total > 0:
        print(f"[赛利亚] {random.choice(_SERIA_ALL_PASS)}")
    elif _passed > 0:
        print(f"[赛利亚] {random.choice(_SERIA_SOME_PASS).format(p=_passed)}")
    else:
        print(f"[赛利亚] {random.choice(_SERIA_ALL_FAIL)}")
