# 第 3 章: SELECT / WHERE / ORDER BY / DISTINCT / LIMIT

这一章是最重要的一章,把你最常用的 SQL 语句一个个对照着写。
下面全部以 `orders` 表(`data/orders.csv`)为例。

## 1. SELECT 列

```sql
SELECT order_id, quantity FROM orders;
```
```python
orders[["order_id", "quantity"]]
```

## 2. WHERE 单条件

```sql
SELECT * FROM orders WHERE status = 'completed';
```
```python
orders[orders["status"] == "completed"]
# 等价写法(更接近 SQL 的语感):
orders.query("status == 'completed'")
```

## 3. WHERE 多条件(AND / OR)

**重要:pandas 里的多条件必须用 `&`、`|`,不能用 Python 的 `and`/`or`,
并且每个条件要用括号括起来。**

```sql
SELECT * FROM orders WHERE status = 'completed' AND quantity > 2;
SELECT * FROM orders WHERE status = 'completed' OR status = 'pending';
```
```python
orders[(orders["status"] == "completed") & (orders["quantity"] > 2)]
orders[(orders["status"] == "completed") | (orders["status"] == "pending")]
```

## 4. IN / NOT IN

```sql
SELECT * FROM orders WHERE status IN ('completed', 'pending');
SELECT * FROM orders WHERE status NOT IN ('cancelled');
```
```python
orders[orders["status"].isin(["completed", "pending"])]
orders[~orders["status"].isin(["cancelled"])]   # ~ 表示取反,相当于 NOT
```

## 5. LIKE 模糊匹配

```sql
SELECT * FROM customers WHERE customer_name LIKE 'Customer_1%';
```
```python
customers[customers["customer_name"].str.startswith("Customer_1")]
# 更通用的写法,支持正则:
customers[customers["customer_name"].str.contains("1", regex=False)]
```

## 6. ORDER BY

```sql
SELECT * FROM orders ORDER BY quantity DESC;
SELECT * FROM orders ORDER BY status ASC, quantity DESC;
```
```python
orders.sort_values("quantity", ascending=False)
orders.sort_values(["status", "quantity"], ascending=[True, False])
```

## 7. DISTINCT

```sql
SELECT DISTINCT status FROM orders;
```
```python
orders["status"].unique()          # 返回 numpy 数组
orders[["status"]].drop_duplicates()  # 返回 DataFrame 形式
```

## 8. LIMIT

```sql
SELECT * FROM orders ORDER BY quantity DESC LIMIT 5;
```
```python
orders.sort_values("quantity", ascending=False).head(5)
```

## 9. 别名(AS)

```sql
SELECT quantity AS qty FROM orders;
```
```python
orders.rename(columns={"quantity": "qty"})
```

好,概念讲完了,去 `exercises.py` 练手。
