"""
第 3 章练习: SELECT / WHERE / ORDER BY / DISTINCT / LIMIT

补全 # TODO 后运行: python 03_pandas_select_where/exercises.py
"""

import os
import sys

import pandas as pd

# 下面这行是固定的准备代码(把项目根目录加进来好载入校验工具),照抄即可,不是本章知识点
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from _check_utils import check_eq, summary  # noqa: E402


def load_orders():
    # TODO: 读取 data/orders.csv
    return None


def select_columns(orders):
    """只保留 order_id、quantity 两列。SQL: SELECT order_id, quantity FROM orders"""
    # TODO
    return None


def filter_completed(orders):
    """只保留 status == 'completed' 的行。SQL: WHERE status = 'completed'"""
    # TODO
    return None


def filter_completed_and_qty_gt(orders, n):
    """status 是 completed 并且 quantity > n。SQL: WHERE status = 'completed' AND quantity > n"""
    # TODO
    return None


def filter_status_in(orders, statuses):
    """status 属于给定的 statuses 列表。SQL: WHERE status IN (...)"""
    # TODO
    return None


def order_by_quantity_desc(orders):
    """按 quantity 从大到小排序。SQL: ORDER BY quantity DESC"""
    # TODO
    return None


def distinct_status_sorted(orders):
    """返回 status 列所有不重复的值,并且按字母顺序排好序,类型是 list。"""
    # TODO
    return None


def top_n_by_quantity(orders, n):
    """按 quantity 从大到小排序后,取前 n 行。SQL: ORDER BY quantity DESC LIMIT n"""
    # TODO
    return None


if __name__ == "__main__":
    orders = load_orders()
    check_eq("load_orders 类型", type(orders).__name__ if orders is not None else None, "DataFrame")

    ref = pd.read_csv("data/orders.csv")  # 独立读取一份用来算期望值,不依赖你的实现

    cols = select_columns(orders) if orders is not None else None
    check_eq("select_columns 列名", list(cols.columns) if cols is not None else None,
              ["order_id", "quantity"])

    fc = filter_completed(orders) if orders is not None else None
    check_eq("filter_completed 行数", len(fc) if fc is not None else None,
              len(ref[ref["status"] == "completed"]))

    fcq = filter_completed_and_qty_gt(orders, 2) if orders is not None else None
    check_eq("filter_completed_and_qty_gt 行数", len(fcq) if fcq is not None else None,
              len(ref[(ref["status"] == "completed") & (ref["quantity"] > 2)]))

    fsi = filter_status_in(orders, ["completed", "pending"]) if orders is not None else None
    check_eq("filter_status_in 行数", len(fsi) if fsi is not None else None,
              len(ref[ref["status"].isin(["completed", "pending"])]))

    ob = order_by_quantity_desc(orders) if orders is not None else None
    check_eq("order_by_quantity_desc 首行数量最大", ob["quantity"].iloc[0] if ob is not None else None,
              ref["quantity"].max())

    ds = distinct_status_sorted(orders) if orders is not None else None
    check_eq("distinct_status_sorted", ds, sorted(ref["status"].unique().tolist()))

    top3 = top_n_by_quantity(orders, 3) if orders is not None else None
    check_eq("top_n_by_quantity (行数, 第一行的quantity)",
              (len(top3), top3["quantity"].iloc[0]) if top3 is not None else None,
              (3, ref["quantity"].max()))

    summary()
