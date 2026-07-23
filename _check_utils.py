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

# 把工作目录切到本文件所在的项目根目录,这样练习里用相对路径
# pd.read_csv("data/xxx.csv") 无论从哪个目录运行都能读到数据(对学员透明,不用管)。
os.chdir(os.path.dirname(os.path.abspath(__file__)))

_total = 0
_passed = 0

_SERIA_ALL_PASS = [
    "干得漂亮,勇士!全部通过,下一章的冒险也拜托你了!",
    "太厉害了!这波操作赛利亚给满分!",
    "全部通过!勇士,你离传说中的数据分析师又近了一步!",
    "完美通关!赛利亚为你骄傲!",
    "本章满星!星星全点亮了,可以去挑战下一章啦!",
    "无懈可击!这一章被你彻底拿下了!",
    "全对!基本功这么扎实,后面的章节也难不倒你!",
    "漂亮的收官!休息一下,下一章见~",
]
_SERIA_SOME_PASS = [
    "已经通过 {p} 题了,剩下的也一定没问题的,加油勇士!",
    "离全部通过只差一点点了!看看上面 Failed 的预期和实际,你能行的!",
    "不错不错,又前进了一步!剩下的题回去翻翻 notes.md 吧!",
    "对了 {p} 题,稳扎稳打!把 Failed 的那几题对照一下预期和实际。",
    "有进步!没通过的题别急,报错和预期就是线索。",
    "{p} 题拿下!剩下的照着笔记里的例子改改就好。",
]
_SERIA_ALL_FAIL = [
    "别灰心,勇士!先看看 notes.md 里的秘籍,再来挑战一次!",
    "万事开头难,赛利亚相信你!从第一题开始,一道一道来!",
    "一个都还没对没关系,先照着笔记的例子敲一遍试试!",
    "先深呼吸~ 把第一题搞定,后面就顺了。",
    "报错不可怕,它在告诉你哪里要改。慢慢来!",
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
    if _total > 0:
        got = min(_passed, _total)
        print("进度 " + "⭐" * got + "☆" * (_total - got) + f"  ({_passed}/{_total})")
    if _passed == _total and _total > 0:
        print(f"[赛利亚] {random.choice(_SERIA_ALL_PASS)}")
    elif _passed > 0:
        print(f"[赛利亚] {random.choice(_SERIA_SOME_PASS).format(p=_passed)}")
    else:
        print(f"[赛利亚] {random.choice(_SERIA_ALL_FAIL)}")
