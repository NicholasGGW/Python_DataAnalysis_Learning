# 第 1 章: numpy 基础

numpy 和 SQL 关系不大,但它是 pandas 的底层,所以先花一点时间了解它。
你可以把 numpy 数组(`ndarray`)简单理解成"一列数字",支持批量运算,速度比 Python 原生 list 快很多。

## 1. 创建数组

```python
import numpy as np

a = np.array([1, 2, 3, 4, 5])
b = np.arange(1, 6)          # 等价于 [1,2,3,4,5],左闭右开
c = np.zeros(5)               # [0. 0. 0. 0. 0.]
d = np.ones((2, 3))           # 2行3列的全 1 矩阵
e = np.linspace(0, 1, 5)      # 0 到 1 之间等间隔取 5 个数
```

## 2. 向量化运算(不用写 for 循环)

SQL 里你写 `SELECT price * 0.9 AS new_price FROM products`,
本质是对一列数据做统一变换。numpy/pandas 也是这个思路:

```python
prices = np.array([100, 200, 300])
discounted = prices * 0.9   # 直接对整个数组做运算,不需要循环
total = prices + np.array([1, 2, 3])   # 两个数组逐元素相加
```

## 3. 布尔筛选(类似 WHERE)

```python
prices = np.array([9.9, 199.0, 599.0, 15.0])

mask = prices > 100          # 得到 [False, True, True, False]
print(prices[mask])          # [199. 599.] —— 相当于 WHERE price > 100
```

这是最重要的一个概念:**用一个布尔数组当"筛子"去过滤原数组**,
后面 pandas 的 WHERE 写法完全是这个思路的延伸。

多条件组合(注意用 `&`、`|`,并且每个条件加括号):

```python
prices[(prices > 100) & (prices < 500)]   # WHERE price > 100 AND price < 500
```

## 4. 布尔数组求和 = COUNT WHERE

一个很常用的小技巧:`True` 在求和时算 1、`False` 算 0,所以:

```python
(prices > 100).sum()     # 大于 100 的有几个
```

对应 SQL:

```sql
SELECT COUNT(*) FROM products WHERE price > 100;
```

## 5. 常用聚合函数(类似 SQL 聚合函数)

| numpy | SQL |
|---|---|
| `arr.sum()` | `SUM(col)` |
| `arr.mean()` | `AVG(col)` |
| `arr.max()` / `arr.min()` | `MAX(col)` / `MIN(col)` |
| `np.median(arr)` | `PERCENTILE(col, 0.5)` |
| `arr.std()` | `STDDEV(col)` |
| `len(arr)` | `COUNT(col)` |

## 6. np.where —— 单条件的 CASE WHEN

```python
labels = np.where(prices > 100, "high", "low")
# prices > 100 的位置是 "high",其余是 "low"
```

对应 SQL:

```sql
SELECT CASE WHEN price > 100 THEN 'high' ELSE 'low' END FROM products;
```

## 7. np.unique —— DISTINCT + ORDER BY

```python
np.unique(np.array([3, 1, 2, 1, 3]))    # [1 2 3],去重并且自动排好序
```

对应 SQL: `SELECT DISTINCT x FROM t ORDER BY x`

## 8. argmax / argmin —— 最大值在哪个位置

```python
prices.argmax()    # 返回最大值所在的下标(不是最大值本身)
prices.argmin()    # 最小值的下标
```

SQL 里没有直接对应,但类似"找到销量最高的那一行"这种需求,
pandas 里的 `idxmax` 就是同一个思路。

## 9. 二维数组和 axis(方向)

二维数组就是一个"矩阵"(几行几列)。聚合时用 `axis` 参数控制方向,
这个概念在 pandas 里也会反复出现:

```python
m = np.array([[1, 2, 3],
              [4, 5, 6]])

m.sum()          # 21,所有元素求和
m.mean(axis=0)   # [2.5, 3.5, 4.5],沿着"行的方向"压缩 → 每一列的平均值
m.mean(axis=1)   # [2.0, 5.0],沿着"列的方向"压缩 → 每一行的平均值
```

记忆方法: `axis=0` 消灭行(结果按列算),`axis=1` 消灭列(结果按行算)。

## 10. 数组形状 / 索引切片

```python
arr = np.arange(10)
arr[0]        # 第一个元素
arr[-1]       # 最后一个元素
arr[2:5]      # 切片,取下标 2、3、4 这一段
arr.reshape(2, 5)  # 变形成 2 行 5 列
```

## 11. 排序

```python
np.sort(arr)              # 从小到大排序(返回新数组)
np.sort(arr)[::-1]        # 从大到小([::-1] 表示倒序)
```

## 12. 数据类型(dtype)

数组里所有元素是同一种类型,`dtype` 能看/改类型:

```python
a = np.array([1, 2, 3])
a.dtype                  # dtype('int64'),整数
a.astype(float)          # 转成小数: [1. 2. 3.]
```

## 13. 处理缺失值 NaN

numpy 用 `np.nan` 表示"缺失/空"。注意:含 NaN 的普通聚合会被"传染"成 NaN,
要用 `nan*` 系列函数跳过缺失值:

```python
x = np.array([1.0, 2.0, np.nan, 4.0])
x.mean()          # nan —— 被缺失值传染了
np.nanmean(x)     # 2.333... —— 自动跳过 NaN
np.isnan(x)       # [False False  True False] 哪些是缺失
```

这和 SQL 里聚合函数默认忽略 `NULL` 的行为类似(`AVG(col)` 会跳过 NULL)。

## 14. 两数组按条件择一(np.where 的另一种用法)

`np.where(条件, a, b)` 还能"逐元素在两个数组之间挑":

```python
a = np.array([1, 2, 3, 4])
b = np.array([10, 20, 30, 40])
np.where(a >= 3, a, b)   # a>=3 的位置取 a,否则取 b -> [10 20 3 4]
```

看完以上内容,去 `exercises.py` 把 10 道题的 TODO 填完,然后直接运行看校验结果。
