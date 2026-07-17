"""
第 1 章练习: numpy 基础

规则:
1. 把每个函数里 `# TODO` 的地方补全,不要改函数名和参数。
2. 补完后直接运行这个文件: python 01_numpy/exercises.py
3. 看输出的 PASS / FAIL,FAIL 的题回去看 notes.md 再改。
"""

import os
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from _check_utils import check_eq, summary  # noqa: E402


def ex1_create_range():
    """用 np.arange 创建一个 1 到 10(含)的数组。"""
    # TODO: 把下面这行改成正确答案
    arr = None
    return arr


def ex2_sum_mean_max(arr):
    """
    输入一个 numpy 数组 arr,返回一个元组 (总和, 平均值, 最大值)。
    对应 SQL: SELECT SUM(x), AVG(x), MAX(x) FROM t
    """
    # TODO: 分别用 arr.sum() / arr.mean() / arr.max() 实现
    total = None
    mean = None
    maximum = None
    return (total, mean, maximum)


def ex3_filter_over_100(prices):
    """
    输入一个价格数组 prices,只返回大于 100 的那些价格。
    对应 SQL: SELECT price FROM products WHERE price > 100
    提示: 用布尔索引,例如 prices[mask]
    """
    # TODO
    result = None
    return result


def ex4_apply_discount(prices, discount_rate=0.9):
    """
    输入价格数组,返回打折后的价格数组(不要用 for 循环,直接向量化运算)。
    对应 SQL: SELECT price * 0.9 AS new_price FROM products
    """
    # TODO
    result = None
    return result


def ex5_reshape():
    """
    创建一个 0 到 11(不含)的数组,然后 reshape 成 3 行 4 列。
    """
    # TODO
    arr = None
    return arr


if __name__ == "__main__":
    r1 = ex1_create_range()
    check_eq("ex1_create_range", list(r1) if r1 is not None else None, list(range(1, 11)))

    sample = np.array([10, 20, 30, 40])
    check_eq("ex2_sum_mean_max", ex2_sum_mean_max(sample), (100, 25.0, 40))

    prices = np.array([9.9, 199.0, 599.0, 15.0, 120.5])
    r3 = ex3_filter_over_100(prices)
    check_eq("ex3_filter_over_100", sorted(r3.tolist()) if r3 is not None else None,
              sorted([199.0, 599.0, 120.5]))

    r4 = ex4_apply_discount(np.array([100.0, 200.0]))
    check_eq("ex4_apply_discount", r4.tolist() if r4 is not None else None, [90.0, 180.0])

    r5 = ex5_reshape()
    check_eq("ex5_reshape_shape", r5.shape if r5 is not None else None, (3, 4))
    check_eq("ex5_reshape_values", r5.tolist() if r5 is not None else None,
              [[0, 1, 2, 3], [4, 5, 6, 7], [8, 9, 10, 11]])

    summary()
