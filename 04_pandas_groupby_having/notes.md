# 第 4 章: GROUP BY / 聚合函数 / HAVING

## 1. 基本分组聚合

```sql
SELECT status, COUNT(*) AS cnt
FROM orders
GROUP BY status;
```
```python
orders.groupby("status").size()
# 或者写成 DataFrame 形式,列名叫 cnt:
orders.groupby("status").size().reset_index(name="cnt")
```

## 2. 对某一列做聚合(SUM / AVG / MAX...)

```sql
SELECT status, SUM(quantity) AS total_qty, AVG(quantity) AS avg_qty
FROM orders
GROUP BY status;
```
```python
orders.groupby("status")["quantity"].agg(["sum", "mean"])
# 想要自定义列名:
orders.groupby("status")["quantity"].agg(total_qty="sum", avg_qty="mean")
```

`reset_index()` 常用来把分组用的列从"索引"变回普通列(更像 SQL 结果):

```python
orders.groupby("status")["quantity"].sum().reset_index(name="total_qty")
```

## 3. 按多列分组

```sql
SELECT customer_id, status, COUNT(*) AS cnt
FROM orders
GROUP BY customer_id, status;
```
```python
orders.groupby(["customer_id", "status"]).size().reset_index(name="cnt")
```

## 4. 一次算多个聚合指标

```sql
SELECT status,
       COUNT(*) AS cnt,
       SUM(quantity) AS total_qty,
       MAX(quantity) AS max_qty
FROM orders
GROUP BY status;
```
```python
orders.groupby("status").agg(
    cnt=("order_id", "count"),
    total_qty=("quantity", "sum"),
    max_qty=("quantity", "max"),
).reset_index()
```

## 5. HAVING(分组后再筛选)

SQL 里 `HAVING` 是在 `GROUP BY` 之后对聚合结果做筛选(不能用 `WHERE`,
因为 `WHERE` 是在分组之前生效的)。pandas 里的思路是:**先分组聚合出一个新表,
再对这个新表做和第 3 章一样的行筛选**。

```sql
SELECT status, COUNT(*) AS cnt
FROM orders
GROUP BY status
HAVING COUNT(*) > 10;
```
```python
grouped = orders.groupby("status").size().reset_index(name="cnt")
grouped[grouped["cnt"] > 10]     # 这一步就相当于 HAVING
```

## 6. 分组 + 排序: 每组的汇总再排个序

分组聚合出结果后,想按某个指标排序(常见的"销量排行榜"),接着 `sort_values` 即可:

```sql
SELECT customer_id, SUM(quantity) AS total_qty
FROM orders
GROUP BY customer_id
ORDER BY total_qty DESC;
```
```python
(orders.groupby("customer_id")["quantity"].sum()
       .reset_index(name="total_qty")
       .sort_values("total_qty", ascending=False))
```

## 7. COUNT(DISTINCT ...): 每组里有多少个不同的值

```sql
SELECT status, COUNT(DISTINCT customer_id) AS n_customers
FROM orders
GROUP BY status;
```
```python
orders.groupby("status")["customer_id"].nunique().reset_index(name="n_customers")
```

## 8. size() 和 count() 的区别(容易踩坑)

- `groupby(...).size()`: 每组**多少行**,类似 `COUNT(*)`,**包含空值行**。
- `groupby(...)["col"].count()`: 每组里 `col` **非空**的个数,类似 `COUNT(col)`,**不含 NULL**。

```python
orders.groupby("status").size()              # 每组行数(COUNT(*))
orders.groupby("status")["quantity"].count() # 每组 quantity 非空的个数(COUNT(quantity))
```

## 9. 小提示: 分组结果的"索引"

`groupby(...).agg(...)` 出来的结果,分组用的列会变成"索引"而不是普通列。
想让它变回普通列(更像 SQL 的结果表),记得在后面接 `.reset_index()`——
前面例子里几乎每个都用了它,原因就在这。

去 `exercises.py` 练手。
