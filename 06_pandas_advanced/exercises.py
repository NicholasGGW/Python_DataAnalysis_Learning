"""
第 6 章练习: CASE WHEN / NULL 处理 / 开窗函数思路

补全 # TODO 后运行: python 06_pandas_advanced/exercises.py
"""

import os
import sys

import numpy as np
import pandas as pd

# 下面这行是固定的准备代码(把项目根目录加进来好载入校验工具),照抄即可,不是本章知识点
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from _check_utils import check_eq, summary  # noqa: E402


def load_all():
    customers = pd.read_csv("data/customers.csv")
    orders = pd.read_csv("data/orders.csv")
    return customers, orders


def add_qty_level(orders):
    """
    新增一列 qty_level: quantity>=4 -> 'high', quantity>=2 -> 'medium', 否则 'low'。
    用 np.select 实现。返回加了新列的 orders。
    """
    # TODO
    return None


def add_is_completed_flag(orders):
    """新增一列 is_completed: status=='completed' 时是 1,否则是 0。用 np.where 实现。"""
    # TODO
    return None


def rows_with_missing_city(customers):
    """返回 city 是空值(NULL)的所有行。SQL: WHERE city IS NULL"""
    # TODO
    return None


def fill_missing_city(customers):
    """把 city 列的空值替换成字符串 'Unknown',返回替换后的 Series。SQL: COALESCE(city, 'Unknown')"""
    # TODO
    return None


def rank_quantity_within_status(orders):
    """
    新增一列 rn: 在每个 status 分组内,按 quantity 从大到小排名(从 1 开始,类似 ROW_NUMBER)。
    返回加了新列的 orders。
    提示: sort_values + groupby + cumcount
    """
    # TODO
    return None


def diff_from_status_avg(orders):
    """
    新增一列 diff_from_avg = quantity - 该行所在 status 分组的平均 quantity。
    返回加了新列的 orders。
    提示: groupby(...).transform("mean")
    """
    # TODO
    return None


if __name__ == "__main__":
    customers, orders = load_all()

    q = add_qty_level(orders.copy()) if orders is not None else None
    if q is not None:
        check_eq("add_qty_level (high判断, low判断)",
                  (bool((q.loc[q["quantity"] >= 4, "qty_level"] == "high").all()),
                   bool((q.loc[q["quantity"] < 2, "qty_level"] == "low").all())),
                  (True, True))
    else:
        check_eq("add_qty_level (high判断, low判断)", None, (True, True))

    ic = add_is_completed_flag(orders.copy()) if orders is not None else None
    if ic is not None:
        check_eq("add_is_completed_flag 求和",
                  int(ic["is_completed"].sum()), int((orders["status"] == "completed").sum()))
    else:
        check_eq("add_is_completed_flag", None, "0/1")

    rmc = rows_with_missing_city(customers)
    check_eq("rows_with_missing_city 行数", len(rmc) if rmc is not None else None,
              int(customers["city"].isna().sum()))

    fmc = fill_missing_city(customers)
    check_eq("fill_missing_city 没有空值了",
              bool(fmc.isna().sum() == 0) if fmc is not None else None, True)

    rk = rank_quantity_within_status(orders.copy()) if orders is not None else None
    if rk is not None:
        rn1_rows = rk[rk["rn"] == 1]
        group_max = rk.groupby("status")["quantity"].max()
        check_eq("rank_quantity_within_status 每组rn=1的行数量都是最大值",
                  bool((rn1_rows.set_index("status")["quantity"] == group_max.loc[rn1_rows["status"]].values).all()),
                  True)
    else:
        check_eq("rank_quantity_within_status", None, "有 rn 列")

    da = diff_from_status_avg(orders.copy()) if orders is not None else None
    if da is not None:
        ref_avg = orders.groupby("status")["quantity"].transform("mean")
        check_eq("diff_from_status_avg 数值正确",
                  bool(np.allclose(da["diff_from_avg"], orders["quantity"] - ref_avg)), True)
    else:
        check_eq("diff_from_status_avg", None, "有 diff_from_avg 列")

    summary()
