"""
第 2 章练习: pandas 基础

规则同上一章: 补全 # TODO,然后运行本文件看 PASS/FAIL。
"""

import os
import sys

import pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from _check_utils import check_eq, summary  # noqa: E402


def load_customers():
    """
    读取 data/customers.csv,返回 DataFrame。
    提示: pd.read_csv(路径)
    """
    # TODO
    df = None
    return df


def count_rows(df):
    """返回 df 的行数。对应 SQL: SELECT COUNT(*) FROM customers"""
    # TODO
    return None


def count_columns(df):
    """返回 df 的列数。"""
    # TODO
    return None


def get_column_names(df):
    """返回所有列名组成的 list。"""
    # TODO
    return None


def first_n_rows(df, n):
    """返回前 n 行。对应 SQL: SELECT * FROM customers LIMIT n"""
    # TODO
    return None


def distinct_city_count(df):
    """返回 city 列有多少个不重复的值(不算 NaN)。对应 SQL: SELECT COUNT(DISTINCT city) FROM customers"""
    # TODO
    return None


if __name__ == "__main__":
    df = load_customers()
    check_eq("load_customers 类型正确", type(df).__name__ if df is not None else None, "DataFrame")
    check_eq("count_rows", count_rows(df) if df is not None else None, 20)
    check_eq("count_columns", count_columns(df) if df is not None else None, 4)
    check_eq(
        "get_column_names",
        get_column_names(df) if df is not None else None,
        ["customer_id", "customer_name", "city", "signup_date"],
    )
    head3 = first_n_rows(df, 3) if df is not None else None
    check_eq("first_n_rows 行数", len(head3) if head3 is not None else None, 3)
    check_eq("distinct_city_count", distinct_city_count(df) if df is not None else None, 5)

    summary()
