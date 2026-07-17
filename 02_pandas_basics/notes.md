# 第 2 章: pandas 基础 —— DataFrame 就是一张表

## 1. DataFrame 是什么

`pandas.DataFrame` 你可以直接理解成 SQL 里的一张表:每一列有列名和类型,每一行是一条记录。

```python
import pandas as pd

# 相当于连接数据库、拿到一张表
customers = pd.read_csv("data/customers.csv")
```

## 2. 看表结构(类似 DESCRIBE / information_schema)

```python
customers.shape        # (行数, 列数),类似 SELECT COUNT(*) 再看列数
customers.dtypes       # 每列的数据类型,类似 DESCRIBE table
customers.columns      # 所有列名
customers.info()       # 更详细的结构信息(含空值统计)
```

## 3. 看数据(类似 SELECT * LIMIT n)

```python
customers.head()       # 相当于 SELECT * FROM customers LIMIT 5
customers.head(10)     # LIMIT 10
customers.tail(3)      # 取最后 3 行
customers.sample(5)    # 随机取 5 行,类似 ORDER BY RAND() LIMIT 5
```

## 4. 单列 / 多列取出来长什么样

```python
customers["city"]                     # 取一列,类型是 Series(可以理解成一列数据)
customers[["customer_id", "city"]]    # 取多列,类型还是 DataFrame
```

对应 SQL:

```sql
SELECT city FROM customers;
SELECT customer_id, city FROM customers;
```

## 5. 行数 / 简单统计(类似 COUNT / DESCRIBE 统计)

```python
len(customers)                # 行数,类似 SELECT COUNT(*) FROM customers
customers["city"].nunique()   # 去重后有多少种,类似 SELECT COUNT(DISTINCT city)
customers.describe()          # 数值列的统计概览(均值、最大最小值等)
```

看完去 `exercises.py` 练手,数据用的是 `data/customers.csv`、`data/products.csv`、`data/orders.csv`,
运行 `python data/generate_data.py` 生成(如果还没生成过)。
