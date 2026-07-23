"""第 3 章参考答案。"""

import os
import sys

import pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from _check_utils import check_eq, summary  # noqa: E402


def load_orders():
    return pd.read_csv("data/orders.csv")


def select_columns(orders):
    return orders[["order_id", "quantity"]]


def filter_completed(orders):
    return orders[orders["status"] == "completed"]


def filter_completed_and_qty_gt(orders, n):
    return orders[(orders["status"] == "completed") & (orders["quantity"] > n)]


def filter_status_in(orders, statuses):
    return orders[orders["status"].isin(statuses)]


def order_by_quantity_desc(orders):
    return orders.sort_values("quantity", ascending=False)


def distinct_status_sorted(orders):
    return sorted(orders["status"].unique().tolist())


def top_n_by_quantity(orders, n):
    return orders.sort_values("quantity", ascending=False).head(n)


if __name__ == "__main__":
    orders = load_orders()
    check_eq("load_orders 类型", type(orders).__name__, "DataFrame")

    ref = pd.read_csv("data/orders.csv")

    cols = select_columns(orders)
    check_eq("select_columns 列名", list(cols.columns), ["order_id", "quantity"])

    fc = filter_completed(orders)
    check_eq("filter_completed 行数", len(fc), len(ref[ref["status"] == "completed"]))

    fcq = filter_completed_and_qty_gt(orders, 2)
    check_eq("filter_completed_and_qty_gt 行数", len(fcq),
              len(ref[(ref["status"] == "completed") & (ref["quantity"] > 2)]))

    fsi = filter_status_in(orders, ["completed", "pending"])
    check_eq("filter_status_in 行数", len(fsi), len(ref[ref["status"].isin(["completed", "pending"])]))

    ob = order_by_quantity_desc(orders)
    check_eq("order_by_quantity_desc 首行数量最大", ob["quantity"].iloc[0], ref["quantity"].max())

    ds = distinct_status_sorted(orders)
    check_eq("distinct_status_sorted", ds, sorted(ref["status"].unique().tolist()))

    top3 = top_n_by_quantity(orders, 3)
    check_eq("top_n_by_quantity (行数, 第一行的quantity)",
              (len(top3), top3["quantity"].iloc[0]), (3, ref["quantity"].max()))

    summary()
