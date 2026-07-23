"""第 6 章参考答案。"""

import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from _check_utils import check_eq, summary  # noqa: E402


def load_all():
    customers = pd.read_csv("data/customers.csv")
    orders = pd.read_csv("data/orders.csv")
    return customers, orders


def add_qty_level(orders):
    conditions = [orders["quantity"] >= 4, orders["quantity"] >= 2]
    choices = ["high", "medium"]
    orders["qty_level"] = np.select(conditions, choices, default="low")
    return orders


def add_is_completed_flag(orders):
    orders["is_completed"] = np.where(orders["status"] == "completed", 1, 0)
    return orders


def rows_with_missing_city(customers):
    return customers[customers["city"].isna()]


def fill_missing_city(customers):
    return customers["city"].fillna("Unknown")


def rank_quantity_within_status(orders):
    orders["rn"] = (
        orders.sort_values("quantity", ascending=False)
        .groupby("status")
        .cumcount() + 1
    )
    return orders


def diff_from_status_avg(orders):
    orders["group_avg"] = orders.groupby("status")["quantity"].transform("mean")
    orders["diff_from_avg"] = orders["quantity"] - orders["group_avg"]
    return orders


if __name__ == "__main__":
    customers, orders = load_all()

    q = add_qty_level(orders.copy())
    check_eq("add_qty_level (high判断, low判断)",
              (bool((q.loc[q["quantity"] >= 4, "qty_level"] == "high").all()),
               bool((q.loc[q["quantity"] < 2, "qty_level"] == "low").all())),
              (True, True))

    ic = add_is_completed_flag(orders.copy())
    check_eq("add_is_completed_flag 求和",
              int(ic["is_completed"].sum()), int((orders["status"] == "completed").sum()))

    rmc = rows_with_missing_city(customers)
    check_eq("rows_with_missing_city 行数", len(rmc), int(customers["city"].isna().sum()))

    fmc = fill_missing_city(customers)
    check_eq("fill_missing_city 没有空值了", bool(fmc.isna().sum() == 0), True)

    rk = rank_quantity_within_status(orders.copy())
    rn1_rows = rk[rk["rn"] == 1]
    group_max = rk.groupby("status")["quantity"].max()
    check_eq("rank_quantity_within_status 每组rn=1的行数量都是最大值",
              bool((rn1_rows.set_index("status")["quantity"] == group_max.loc[rn1_rows["status"]].values).all()),
              True)

    da = diff_from_status_avg(orders.copy())
    ref_avg = orders.groupby("status")["quantity"].transform("mean")
    check_eq("diff_from_status_avg 数值正确",
              bool(np.allclose(da["diff_from_avg"], orders["quantity"] - ref_avg)), True)

    summary()
