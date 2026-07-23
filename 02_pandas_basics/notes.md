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

## 6. Series 和 DataFrame 的区别

pandas 里有两种核心结构,分清楚它们后面会少踩很多坑:

- **Series**: 一列数据(带一个"行标签"索引),取单列 `customers["city"]` 得到的就是 Series。
- **DataFrame**: 一张二维表(多列),取多列 `customers[["customer_id", "city"]]` 得到的还是 DataFrame。

一个记忆点: **一个方括号取一列(Series),两个方括号取多列(DataFrame)**。

## 7. 每列的常用小统计

针对某一列(Series)可以直接算:

```python
customers["city"].value_counts()   # 每个城市各有几个客户,类似 GROUP BY city COUNT(*)
customers["city"].unique()         # 有哪些不同的城市(数组)
customers["signup_date"].min()     # 最早的注册时间,类似 MIN(signup_date)
customers["signup_date"].max()     # 最晚的,类似 MAX(signup_date)
```

`value_counts()` 特别常用,一行就能看"某列各取值的分布",相当于:

```sql
SELECT city, COUNT(*) FROM customers GROUP BY city ORDER BY COUNT(*) DESC;
```

## 8. 改列名 / 看有没有空值

```python
customers.rename(columns={"city": "城市"})   # 改列名,类似 SELECT city AS 城市
customers.isna().sum()                       # 每列有多少个空值(NULL),排查数据质量必用
```

看完去 `exercises.py` 练手,数据用的是 `data/customers.csv`、`data/products.csv`、`data/orders.csv`,
运行 `python data/generate_data.py` 生成(如果还没生成过)。
