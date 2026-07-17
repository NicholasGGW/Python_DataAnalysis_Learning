"""
第 1 章参考答案。建议自己先在 exercises.py 里写完再来对照。
运行方式: python 01_numpy/solutions.py (会跑一遍同样的校验,应该全部 Pass)
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


def ex6_count_over(prices, threshold):
    return int((prices > threshold).sum())


def ex7_label_high_low(prices, threshold):
    return np.where(prices > threshold, "high", "low")


def ex8_distinct_sorted(arr):
    return np.unique(arr)


def ex9_column_means(matrix):
    return matrix.mean(axis=0)


def ex10_index_of_max(prices):
    return int(prices.argmax())


if __name__ == "__main__":
    check_eq("ex1_create_range", list(ex1_create_range()), list(range(1, 11)))

    check_eq("ex2_sum_mean_max", ex2_sum_mean_max(np.array([10, 20, 30, 40])), (100, 25.0, 40))

    prices = np.array([9.9, 199.0, 599.0, 15.0, 120.5])
    check_eq("ex3_filter_over_100", sorted(ex3_filter_over_100(prices).tolist()),
             [120.5, 199.0, 599.0])

    check_eq("ex4_apply_discount", ex4_apply_discount(np.array([100.0, 200.0])).tolist(),
             [90.0, 180.0])

    check_eq("ex5_reshape", ex5_reshape().tolist(),
             [[0, 1, 2, 3], [4, 5, 6, 7], [8, 9, 10, 11]])

    check_eq("ex6_count_over", ex6_count_over(prices, 100), 3)

    check_eq("ex7_label_high_low",
             ex7_label_high_low(np.array([50.0, 150.0, 99.0, 300.0]), 100).tolist(),
             ["low", "high", "low", "high"])

    check_eq("ex8_distinct_sorted", ex8_distinct_sorted(np.array([3, 1, 2, 1, 3, 2])).tolist(),
             [1, 2, 3])

    check_eq("ex9_column_means",
             ex9_column_means(np.array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])).tolist(),
             [2.5, 3.5, 4.5])

    check_eq("ex10_index_of_max", ex10_index_of_max(prices), 2)

    summary()
