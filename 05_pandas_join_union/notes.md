# 第 5 章: JOIN / UNION —— 表和表之间的合并

`pd.merge()` 就是 pandas 里的 JOIN,参数 `how` 决定 JOIN 的类型,和 SQL 的
`INNER JOIN` / `LEFT JOIN` / `RIGHT JOIN` / `OUTER JOIN` 一一对应。

## 1. INNER JOIN(默认,只保留两边都匹配上的)

```sql
SELECT o.*, c.customer_name
FROM orders o
INNER JOIN customers c ON o.customer_id = c.customer_id;
```
```python
orders.merge(customers, on="customer_id", how="inner")
```

## 2. LEFT JOIN(保留左表全部,右表没匹配上就是 NaN)

```sql
SELECT o.*, c.customer_name
FROM orders o
LEFT JOIN customers c ON o.customer_id = c.customer_id;
```
```python
orders.merge(customers, on="customer_id", how="left")
```

我们的练习数据里,`orders` 表故意造了两条 `customer_id = 999` 的"孤儿订单",
这两条在 `customers` 表里是找不到的。做 `left join` 之后,这两行的
`customer_name` 会是 `NaN`;做 `inner join` 之后,这两行会直接消失。
这和 SQL 里 LEFT JOIN vs INNER JOIN 的区别完全一样。

## 3. RIGHT JOIN / OUTER JOIN

```python
orders.merge(customers, on="customer_id", how="right")   # RIGHT JOIN
orders.merge(customers, on="customer_id", how="outer")   # FULL OUTER JOIN
```

## 4. 关联字段名不一样时

SQL:
```sql
SELECT * FROM orders o JOIN products p ON o.product_id = p.product_id;
```

如果两张表用来关联的字段名不同,比如左边叫 `pid`、右边叫 `product_id`:
```python
orders.merge(products, left_on="pid", right_on="product_id")
```

## 5. 多表连续 JOIN

SQL 里经常一次 JOIN 好几张表,pandas 就是链式调用 `merge` 好几次:

```sql
SELECT o.order_id, c.customer_name, p.product_name, o.quantity
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
JOIN products p ON o.product_id = p.product_id;
```
```python
result = (
    orders
    .merge(customers, on="customer_id", how="inner")
    .merge(products, on="product_id", how="inner")
)
result[["order_id", "customer_name", "product_name", "quantity"]]
```

## 6. UNION(纵向拼接两张结构相同的表)

```sql
SELECT customer_id FROM orders WHERE status = 'completed'
UNION
SELECT customer_id FROM orders WHERE status = 'pending';
```
```python
pd.concat([
    orders.loc[orders["status"] == "completed", ["customer_id"]],
    orders.loc[orders["status"] == "pending", ["customer_id"]],
]).drop_duplicates()          # UNION 会自动去重,所以要 drop_duplicates
# 如果想要 UNION ALL(不去重),去掉 drop_duplicates() 即可
```

去 `exercises.py` 练手。
