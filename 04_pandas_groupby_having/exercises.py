"""
第 4 章练习: GROUP BY / 聚合 / HAVING

补全 # TODO 后运行: python 04_pandas_groupby_having/exercises.py
"""

import os
import sys

import pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from _check_utils import DATA_DIR, check_eq, summary  # noqa: E402


def load_orders():
    return pd.read_csv(os.path.join(DATA_DIR, "orders.csv"))


def count_by_status(orders):
    """
    按 status 分组,统计每组行数,返回 DataFrame,列名是 ["status", "cnt"]。
    SQL: SELECT status, COUNT(*) AS cnt FROM orders GROUP BY status
    """
    # TODO
    return None


def total_qty_by_customer(orders):
    """
    按 customer_id 分组,求 quantity 总和,返回 DataFrame,列名是 ["customer_id", "total_qty"]。
    SQL: SELECT customer_id, SUM(quantity) AS total_qty FROM orders GROUP BY customer_id
    """
    # TODO
    return None


def multi_agg_by_status(orders):
    """
    按 status 分组,同时算出 cnt(行数)、total_qty(quantity 总和)、avg_qty(quantity 平均值)。
    返回 DataFrame,列名是 ["status", "cnt", "total_qty", "avg_qty"]。
    """
    # TODO
    return None


def status_with_more_than(orders, n):
    """
    先按 status 分组统计 cnt,再只保留 cnt > n 的分组(这一步就是 HAVING)。
    返回 DataFrame,列名是 ["status", "cnt"]。
    """
    # TODO
    return None


if __name__ == "__main__":
    orders = load_orders()

    cbs = count_by_status(orders)
    ref_cbs = orders.groupby("status").size().reset_index(name="cnt")
    check_eq("count_by_status 列名", list(cbs.columns) if cbs is not None else None, ["status", "cnt"])
    check_eq(
        "count_by_status 数值",
        cbs.sort_values("status").reset_index(drop=True).to_dict() if cbs is not None else None,
        ref_cbs.sort_values("status").reset_index(drop=True).to_dict(),
    )

    tqc = total_qty_by_customer(orders)
    ref_tqc = orders.groupby("customer_id")["quantity"].sum().reset_index(name="total_qty")
    check_eq("total_qty_by_customer 列名", list(tqc.columns) if tqc is not None else None,
              ["customer_id", "total_qty"])
    check_eq(
        "total_qty_by_customer 行数",
        len(tqc) if tqc is not None else None,
        len(ref_tqc),
    )

    mabs = multi_agg_by_status(orders)
    check_eq("multi_agg_by_status 列名", list(mabs.columns) if mabs is not None else None,
              ["status", "cnt", "total_qty", "avg_qty"])

    swm = status_with_more_than(orders, 5)
    ref_swm = ref_cbs[ref_cbs["cnt"] > 5]
    check_eq("status_with_more_than 行数", len(swm) if swm is not None else None, len(ref_swm))

    summary()
