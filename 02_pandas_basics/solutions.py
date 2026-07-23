"""第 2 章参考答案。"""

import os
import sys

import pandas as pd

# 下面这行是固定的准备代码(把项目根目录加进来好载入校验工具),照抄即可,不是本章知识点
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from _check_utils import check_eq, summary  # noqa: E402


def load_customers():
    return pd.read_csv("data/customers.csv")


def count_rows(df):
    return len(df)


def count_columns(df):
    return df.shape[1]


def get_column_names(df):
    return list(df.columns)


def first_n_rows(df, n):
    return df.head(n)


def distinct_city_count(df):
    return df["city"].nunique()


if __name__ == "__main__":
    df = load_customers()
    check_eq("load_customers 类型正确", type(df).__name__, "DataFrame")
    check_eq("count_rows", count_rows(df), 20)
    check_eq("count_columns", count_columns(df), 4)
    check_eq(
        "get_column_names",
        get_column_names(df),
        ["customer_id", "customer_name", "city", "signup_date"],
    )
    head3 = first_n_rows(df, 3)
    check_eq("first_n_rows 行数", len(head3), 3)
    check_eq("distinct_city_count", distinct_city_count(df), 5)

    summary()
