# 第 6 章: CASE WHEN / NULL 处理 / 开窗函数思路

## 1. CASE WHEN

```sql
SELECT quantity,
       CASE WHEN quantity >= 4 THEN 'high'
            WHEN quantity >= 2 THEN 'medium'
            ELSE 'low' END AS qty_level
FROM orders;
```

pandas 里最常用 `np.select`(多条件)或 `np.where`(单条件):

```python
import numpy as np

conditions = [orders["quantity"] >= 4, orders["quantity"] >= 2]
choices = ["high", "medium"]
orders["qty_level"] = np.select(conditions, choices, default="low")
```

单条件的简单情况用 `np.where` 更快:

```sql
SELECT CASE WHEN status = 'completed' THEN 1 ELSE 0 END AS is_completed FROM orders;
```
```python
orders["is_completed"] = np.where(orders["status"] == "completed", 1, 0)
```

## 2. NULL 处理

| SQL | pandas |
|---|---|
| `col IS NULL` | `df["col"].isna()` |
| `col IS NOT NULL` | `df["col"].notna()` |
| `COALESCE(col, 'default')` | `df["col"].fillna("default")` |
| 删除有空值的行 | `df.dropna(subset=["col"])` |

```sql
SELECT * FROM customers WHERE city IS NULL;
SELECT customer_id, COALESCE(city, 'Unknown') AS city FROM customers;
```
```python
customers[customers["city"].isna()]
customers["city"].fillna("Unknown")
```

## 3. 开窗函数思路(ROW_NUMBER / RANK / 累计值)

pandas 没有 `OVER(PARTITION BY ...)` 这个语法,但可以用 `groupby` + `transform`
或者 `groupby` + `rank`/`cumsum` 达到同样效果。

### ROW_NUMBER() OVER (PARTITION BY status ORDER BY quantity DESC)

```sql
SELECT *,
       ROW_NUMBER() OVER (PARTITION BY status ORDER BY quantity DESC) AS rn
FROM orders;
```
```python
orders["rn"] = (
    orders.sort_values("quantity", ascending=False)
    .groupby("status")
    .cumcount() + 1
)
```

### 每组的平均值"广播"回每一行(常用于算"高于本组平均"这类指标)

```sql
SELECT *,
       quantity - AVG(quantity) OVER (PARTITION BY status) AS diff_from_avg
FROM orders;
```
```python
orders["group_avg"] = orders.groupby("status")["quantity"].transform("mean")
orders["diff_from_avg"] = orders["quantity"] - orders["group_avg"]
```

`transform` 是这里的关键:它和 `groupby().agg()` 不同,`agg` 是"多行变一行"(分组汇总),
而 `transform` 是"算出汇总值后,再把这个值贴回原来的每一行",行数不变。

### RANK() OVER (ORDER BY quantity DESC)

```python
orders["rank"] = orders["quantity"].rank(ascending=False, method="min")
```

去 `exercises.py` 练手,这是最后一章了。
