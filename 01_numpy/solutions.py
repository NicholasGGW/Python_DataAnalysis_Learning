"""
第 1 章参考答案。建议自己先在 exercises.py 里写完再来对照。
运行方式: python 01_numpy/solutions.py (会跑一遍同样的校验,应该全部 PASS)
"""

import os
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from _check_utils import check_eq, summary  # noqa: E402


def ex1_create_range():
    return np.arange(1, 11)


def ex2_sum_mean_max(arr):
    return (arr.sum(), arr.mean(), arr.max())


def ex3_filter_over_100(prices):
    return prices[prices > 100]


def ex4_apply_discount(prices, discount_rate=0.9):
    return prices * discount_rate


def ex5_reshape():
    return np.arange(0, 12).reshape(3, 4)


if __name__ == "__main__":
    r1 = ex1_create_range()
    check_eq("ex1_create_range", list(r1), list(range(1, 11)))

    sample = np.array([10, 20, 30, 40])
    check_eq("ex2_sum_mean_max", ex2_sum_mean_max(sample), (100, 25.0, 40))

    prices = np.array([9.9, 199.0, 599.0, 15.0, 120.5])
    r3 = ex3_filter_over_100(prices)
    check_eq("ex3_filter_over_100", sorted(r3.tolist()), sorted([199.0, 599.0, 120.5]))

    r4 = ex4_apply_discount(np.array([100.0, 200.0]))
    check_eq("ex4_apply_discount", r4.tolist(), [90.0, 180.0])

    r5 = ex5_reshape()
    check_eq("ex5_reshape_shape", r5.shape, (3, 4))
    check_eq("ex5_reshape_values", r5.tolist(), [[0, 1, 2, 3], [4, 5, 6, 7], [8, 9, 10, 11]])

    summary()
