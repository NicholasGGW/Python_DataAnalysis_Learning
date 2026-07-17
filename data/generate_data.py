"""
生成练习用的三张"表"(CSV 文件): customers / products / orders。

运行方式:
    python data/generate_data.py

生成后会在 data/ 目录下看到:
    customers.csv
    products.csv
    orders.csv
"""

import os
import numpy as np
import pandas as pd

np.random.seed(42)

OUT_DIR = os.path.dirname(os.path.abspath(__file__))

# ---------- customers 客户表 ----------
customer_ids = range(1, 21)  # 20 个客户
cities = ["Beijing", "Shanghai", "Guangzhou", "Shenzhen", "Hangzhou"]

customers = pd.DataFrame({
    "customer_id": customer_ids,
    "customer_name": [f"Customer_{i}" for i in customer_ids],
    "city": np.random.choice(cities, size=len(customer_ids)),
    "signup_date": pd.date_range("2023-01-01", periods=len(customer_ids), freq="17D"),
})
# 故意留几个空值,后面练习处理 NULL 用
customers.loc[[3, 10], "city"] = np.nan

# ---------- products 商品表 ----------
products = pd.DataFrame({
    "product_id": range(1, 11),
    "product_name": [f"Product_{i}" for i in range(1, 11)],
    "category": np.random.choice(["Electronics", "Books", "Home", "Toys"], size=10),
    "price": np.round(np.random.uniform(9.9, 999.9, size=10), 2),
})

# ---------- orders 订单表 ----------
n_orders = 60
orders = pd.DataFrame({
    "order_id": range(1001, 1001 + n_orders),
    "customer_id": np.random.choice(customer_ids, size=n_orders),
    "product_id": np.random.choice(products["product_id"], size=n_orders),
    "order_date": pd.to_datetime(
        np.random.choice(pd.date_range("2023-06-01", "2023-12-31"), size=n_orders)
    ),
    "quantity": np.random.randint(1, 6, size=n_orders),
    "status": np.random.choice(
        ["completed", "cancelled", "pending"], size=n_orders, p=[0.7, 0.15, 0.15]
    ),
})
# 故意造几个"孤儿订单"(customer_id 在 customers 表里不存在),练习 join 时用
orders.loc[[0, 1], "customer_id"] = 999

if __name__ == "__main__":
    customers.to_csv(os.path.join(OUT_DIR, "customers.csv"), index=False)
    products.to_csv(os.path.join(OUT_DIR, "products.csv"), index=False)
    orders.to_csv(os.path.join(OUT_DIR, "orders.csv"), index=False)
    print("数据生成完毕:")
    print(f"  customers: {len(customers)} 行")
    print(f"  products:  {len(products)} 行")
    print(f"  orders:    {len(orders)} 行")
    print(f"文件保存在: {OUT_DIR}")
