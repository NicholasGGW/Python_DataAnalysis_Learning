"""第 5 章参考答案。"""

import os
import sys

import pandas as pd

# 下面这行是固定的准备代码(把项目根目录加进来好载入校验工具),照抄即可,不是本章知识点
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from _check_utils import check_eq, summary  # noqa: E402


def load_all():
    customers = pd.read_csv("data/customers.csv")
    products = pd.read_csv("data/products.csv")
    orders = pd.read_csv("data/orders.csv")
    return customers, products, orders


def inner_join_orders_customers(orders, customers):
    return orders.merge(customers, on="customer_id", how="inner")


def left_join_orders_customers(orders, customers):
    return orders.merge(customers, on="customer_id", how="left")


def join_three_tables(orders, customers, products):
    result = (
        orders
        .merge(customers, on="customer_id", how="inner")
        .merge(products, on="product_id", how="inner")
    )
    return result[["order_id", "customer_name", "product_name", "quantity"]]


def union_customer_ids_by_status(orders, status_a, status_b):
    return pd.concat([
        orders.loc[orders["status"] == status_a, ["customer_id"]],
        orders.loc[orders["status"] == status_b, ["customer_id"]],
    ]).drop_duplicates()


if __name__ == "__main__":
    customers, products, orders = load_all()

    ij = inner_join_orders_customers(orders, customers)
    ref_ij = orders.merge(customers, on="customer_id", how="inner")
    check_eq("inner_join 行数(孤儿订单被排除)", len(ij), len(ref_ij))

    lj = left_join_orders_customers(orders, customers)
    check_eq("left_join (行数, 孤儿订单customer_name全是NaN)",
              (len(lj), bool(lj.loc[lj["customer_id"] == 999, "customer_name"].isna().all())),
              (len(orders), True))

    jt = join_three_tables(orders, customers, products)
    check_eq("join_three_tables 列名", list(jt.columns),
              ["order_id", "customer_name", "product_name", "quantity"])

    un = union_customer_ids_by_status(orders, "completed", "pending")
    ref_union = pd.concat([
        orders.loc[orders["status"] == "completed", ["customer_id"]],
        orders.loc[orders["status"] == "pending", ["customer_id"]],
    ]).drop_duplicates()
    check_eq("union_customer_ids_by_status 行数", len(un), len(ref_union))

    summary()
