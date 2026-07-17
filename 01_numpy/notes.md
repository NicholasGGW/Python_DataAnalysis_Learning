# 第 1 章: numpy 基础

numpy 和 SQL 关系不大,但它是 pandas 的底层,所以先花一点点时间了解它。
你可以把 numpy 数组(`ndarray`)简单理解成"一列数字",支持批量运算,速度比 Python 原生 list 快很多。

## 1. 创建数组

```python
import numpy as np

a = np.array([1, 2, 3, 4, 5])
b = np.arange(1, 6)          # 等价于 [1,2,3,4,5]
c = np.zeros(5)               # [0. 0. 0. 0. 0.]
d = np.ones((2, 3))           # 2行3列的全 1 矩阵
```

## 2. 向量化运算(不用写 for 循环)

SQL 里你写 `SELECT price * 0.9 AS new_price FROM products`,
本质是对一列数据做统一变换。numpy/pandas 也是这个思路:

```python
prices = np.array([100, 200, 300])
discounted = prices * 0.9   # 直接对整个数组做运算,不需要循环
```

## 3. 布尔筛选(类似 WHERE)

```python
prices = np.array([9.9, 199.0, 599.0, 15.0])

mask = prices > 100          # 得到 [False, True, True, False]
print(prices[mask])          # [199. 599.] —— 相当于 WHERE price > 100
```

这是最重要的一个概念:**用一个布尔数组当"筛子"去过滤原数组**,
后面 pandas 的 `WHERE` 写法完全是这个思路的延伸。

## 4. 常用聚合函数(类似 SQL 聚合函数)

| numpy | SQL |
|---|---|
| `arr.sum()` | `SUM(col)` |
| `arr.mean()` | `AVG(col)` |
| `arr.max()` / `arr.min()` | `MAX(col)` / `MIN(col)` |
| `arr.std()` | `STDDEV(col)` |
| `len(arr)` | `COUNT(col)` |

## 5. 数组形状 / 索引切片

```python
arr = np.arange(10)
arr[0]        # 第一个元素
arr[-1]       # 最后一个元素
arr[2:5]      # 切片,类似 LIMIT + OFFSET 的感觉(取一段)
arr.reshape(2, 5)  # 变形成 2 行 5 列
```

看完以上内容,去 `exercises.py` 把 TODO 填完,然后直接运行这个文件看校验结果。
