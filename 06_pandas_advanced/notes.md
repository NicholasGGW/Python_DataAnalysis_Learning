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

## 4. 新增列 / 删除列 / 改类型

```python
orders["amount"] = orders["quantity"] * 10        # 新增一列(基于已有列计算)
orders = orders.drop(columns=["amount"])           # 删除列
orders["order_date"] = pd.to_datetime(orders["order_date"])  # 改成日期类型
orders["quantity"] = orders["quantity"].astype(float)        # 改成小数类型
```

## 5. apply: 对每一行/每个值套用自定义逻辑

当内置方法不够用时,可以用 `apply` 跑自己写的函数。能不用就不用(向量化更快),
但它很灵活,像 SQL 里复杂的 `CASE WHEN` 兜底:

```python
def level(q):
    if q >= 4:
        return "high"
    elif q >= 2:
        return "medium"
    return "low"

orders["qty_level"] = orders["quantity"].apply(level)
```

## 6. 累计值(类似 SUM(...) OVER (ORDER BY ...))

```python
orders_sorted = orders.sort_values("order_date")
orders_sorted["running_total"] = orders_sorted["quantity"].cumsum()  # 逐行累加
```

对应 SQL 的滑动累计:`SUM(quantity) OVER (ORDER BY order_date)`。

## 7. 字符串列的常用处理(.str)

字符串列有一整套 `.str` 方法,类似 SQL 的 `UPPER / LIKE / SUBSTRING`:

```python
customers["customer_name"].str.upper()             # 转大写,类似 UPPER()
customers["customer_name"].str.contains("1")       # 是否包含,类似 LIKE '%1%'
customers["customer_name"].str.replace("Customer", "客户")  # 替换
```

## 8. 数据导出(把结果存回文件)

分析完想把结果保存下来,和 `read_csv` 相对:

```python
result.to_csv("data/result.csv", index=False)   # index=False 不把行号写进文件
```

去 `exercises.py` 练手,这是最后一章了。
