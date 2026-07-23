"""
第 5 章练习: JOIN / UNION

补全 # TODO 后运行: python 05_pandas_join_union/exercises.py
"""

import os
import sys

import pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from _check_utils import check_eq, summary  # noqa: E402


def load_all():
    customers = pd.read_csv("data/customers.csv")
    products = pd.read_csv("data/products.csv")
    orders = pd.read_csv("data/orders.csv")
    return customers, products, orders


def inner_join_orders_customers(orders, customers):
    """
    orders 和 customers 按 customer_id 做 inner join。
    SQL: orders o INNER JOIN customers c ON o.customer_id = c.customer_id
    """
    # TODO
    return None


def left_join_orders_customers(orders, customers):
    """
    orders 和 customers 按 customer_id 做 left join(以 orders 为主表)。
    SQL: orders o LEFT JOIN customers c ON o.customer_id = c.customer_id
    """
    # TODO
    return None


def join_three_tables(orders, customers, products):
    """
    orders 依次 join customers、join products(都用 inner join),
    最终只保留 order_id, customer_name, product_name, quantity 四列。
    """
    # TODO
    return None


def union_customer_ids_by_status(orders, status_a, status_b):
    """
    把 status == status_a 的 customer_id 和 status == status_b 的 customer_id
    合并成一列(去重),返回一个 DataFrame,只有一列 customer_id。
    SQL: SELECT customer_id FROM orders WHERE status=status_a
         UNION
         SELECT customer_id FROM orders WHERE status=status_b
    """
    # TODO
    return None


if __name__ == "__main__":
    customers, products, orders = load_all()

    ij = inner_join_orders_customers(orders, customers)
    ref_ij = orders.merge(customers, on="customer_id", how="inner")
    check_eq("inner_join 行数(孤儿订单被排除)", len(ij) if ij is not None else None, len(ref_ij))

    lj = left_join_orders_customers(orders, customers)
    check_eq("left_join (行数, 孤儿订单customer_name全是NaN)",
              (len(lj), bool(lj.loc[lj["customer_id"] == 999, "customer_name"].isna().all()))
              if lj is not None else None,
              (len(orders), True))

    jt = join_three_tables(orders, customers, products)
    check_eq("join_three_tables 列名", list(jt.columns) if jt is not None else None,
              ["order_id", "customer_name", "product_name", "quantity"])

    un = union_customer_ids_by_status(orders, "completed", "pending")
    ref_union = pd.concat([
        orders.loc[orders["status"] == "completed", ["customer_id"]],
        orders.loc[orders["status"] == "pending", ["customer_id"]],
    ]).drop_duplicates()
    check_eq("union_customer_ids_by_status 行数", len(un) if un is not None else None, len(ref_union))

    summary()
