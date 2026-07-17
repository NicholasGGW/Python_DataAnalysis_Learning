"""第 4 章参考答案。"""

import os
import sys

import pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from _check_utils import DATA_DIR, check_eq, summary  # noqa: E402


def load_orders():
    return pd.read_csv(os.path.join(DATA_DIR, "orders.csv"))


def count_by_status(orders):
    return orders.groupby("status").size().reset_index(name="cnt")


def total_qty_by_customer(orders):
    return orders.groupby("customer_id")["quantity"].sum().reset_index(name="total_qty")


def multi_agg_by_status(orders):
    return orders.groupby("status").agg(
        cnt=("order_id", "count"),
        total_qty=("quantity", "sum"),
        avg_qty=("quantity", "mean"),
    ).reset_index()


def status_with_more_than(orders, n):
    grouped = orders.groupby("status").size().reset_index(name="cnt")
    return grouped[grouped["cnt"] > n]


if __name__ == "__main__":
    orders = load_orders()

    cbs = count_by_status(orders)
    ref_cbs = orders.groupby("status").size().reset_index(name="cnt")
    check_eq(
        "count_by_status",
        cbs.sort_values("status").reset_index(drop=True).to_dict(),
        ref_cbs.sort_values("status").reset_index(drop=True).to_dict(),
    )

    tqc = total_qty_by_customer(orders)
    ref_tqc = orders.groupby("customer_id")["quantity"].sum().reset_index(name="total_qty")
    check_eq(
        "total_qty_by_customer",
        tqc.sort_values("customer_id").reset_index(drop=True).to_dict(),
        ref_tqc.sort_values("customer_id").reset_index(drop=True).to_dict(),
    )

    mabs = multi_agg_by_status(orders)
    check_eq("multi_agg_by_status 列名", list(mabs.columns), ["status", "cnt", "total_qty", "avg_qty"])

    swm = status_with_more_than(orders, 5)
    ref_swm = ref_cbs[ref_cbs["cnt"] > 5]
    check_eq("status_with_more_than 行数", len(swm), len(ref_swm))

    summary()
