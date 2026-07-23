"""
第 1 章练习: numpy 基础(共 10 题)

规则:
1. 把每个函数里 `# TODO` 的地方补全,不要改函数名和参数。
2. 补完后直接运行这个文件: python 01_numpy/exercises.py
3. 每道题都会打印 预期/实际/结果,Failed 的题回去看 notes.md 再改。
"""

import os
import sys

import numpy as np

# 下面这行是固定的准备代码(把项目根目录加进来好载入校验工具),照抄即可,不是本章知识点
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from _check_utils import check_eq, summary  # noqa: E402


def ex1_create_range():
    """用 np.arange 创建一个 1 到 10(含)的数组。"""
    # TODO
    arr = None
    return arr


def ex2_sum_mean_max(arr):
    """
    输入一个 numpy 数组 arr,返回一个元组 (总和, 平均值, 最大值)。
    对应 SQL: SELECT SUM(x), AVG(x), MAX(x) FROM t
    """
    # TODO: 分别用 arr.sum() / arr.mean() / arr.max() 实现
    return None


def ex3_filter_over_100(prices):
    """
    输入一个价格数组 prices,只返回大于 100 的那些价格。
    对应 SQL: SELECT price FROM products WHERE price > 100
    提示: 布尔索引 prices[mask]
    """
    # TODO
    return None


def ex4_apply_discount(prices, discount_rate=0.9):
    """
    输入价格数组,返回打折后的价格数组(不要用 for 循环,直接向量化运算)。
    对应 SQL: SELECT price * 0.9 AS new_price FROM products
    """
    # TODO
    return None


def ex5_reshape():
    """创建一个 0 到 11(不含 12)的数组,然后 reshape 成 3 行 4 列。"""
    # TODO
    return None


def ex6_count_over(prices, threshold):
    """
    统计 prices 里大于 threshold 的元素个数,返回一个 int。
    对应 SQL: SELECT COUNT(*) FROM products WHERE price > threshold
    提示: 布尔数组直接 .sum()
    """
    # TODO
    return None


def ex7_label_high_low(prices, threshold):
    """
    用 np.where 给每个价格打标签: 大于 threshold 的是 'high',否则是 'low'。
    返回一个字符串数组。
    对应 SQL: SELECT CASE WHEN price > t THEN 'high' ELSE 'low' END FROM products
    """
    # TODO
    return None


def ex8_distinct_sorted(arr):
    """
    去重并从小到大排序,返回数组。
    对应 SQL: SELECT DISTINCT x FROM t ORDER BY x
    提示: np.unique 一步到位
    """
    # TODO
    return None


def ex9_column_means(matrix):
    """
    输入一个二维数组,返回每一列的平均值(一维数组)。
    提示: 用 axis 参数,想想 axis=0 还是 axis=1
    """
    # TODO
    return None


def ex10_index_of_max(prices):
    """
    返回最大值所在的下标(int),不是最大值本身。
    提示: argmax
    """
    # TODO
    return None


if __name__ == "__main__":
    r1 = ex1_create_range()
    check_eq("ex1_create_range", list(r1) if r1 is not None else None, list(range(1, 11)))

    check_eq("ex2_sum_mean_max", ex2_sum_mean_max(np.array([10, 20, 30, 40])), (100, 25.0, 40))

    prices = np.array([9.9, 199.0, 599.0, 15.0, 120.5])
    r3 = ex3_filter_over_100(prices)
    check_eq("ex3_filter_over_100", sorted(r3.tolist()) if r3 is not None else None,
             [120.5, 199.0, 599.0])

    r4 = ex4_apply_discount(np.array([100.0, 200.0]))
    check_eq("ex4_apply_discount", r4.tolist() if r4 is not None else None, [90.0, 180.0])

    r5 = ex5_reshape()
    check_eq("ex5_reshape", r5.tolist() if r5 is not None else None,
             [[0, 1, 2, 3], [4, 5, 6, 7], [8, 9, 10, 11]])

    r6 = ex6_count_over(prices, 100)
    check_eq("ex6_count_over", int(r6) if r6 is not None else None, 3)

    r7 = ex7_label_high_low(np.array([50.0, 150.0, 99.0, 300.0]), 100)
    check_eq("ex7_label_high_low", r7.tolist() if r7 is not None else None,
             ["low", "high", "low", "high"])

    r8 = ex8_distinct_sorted(np.array([3, 1, 2, 1, 3, 2]))
    check_eq("ex8_distinct_sorted", r8.tolist() if r8 is not None else None, [1, 2, 3])

    r9 = ex9_column_means(np.array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]]))
    check_eq("ex9_column_means", r9.tolist() if r9 is not None else None, [2.5, 3.5, 4.5])

    r10 = ex10_index_of_max(prices)
    check_eq("ex10_index_of_max", int(r10) if r10 is not None else None, 2)

    summary()
