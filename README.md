# Python 数据分析入门项目(SQL 人士专用)

给已经会 SQL、想学 Python 数据分析(numpy + pandas)的人准备的一套小项目。
每一章都会把 pandas 的写法和你熟悉的 SQL 语句对照着讲,不会讲得很深,
只覆盖日常数据分析最常用的部分。

## 怎么用这个项目

两种学习方式:**命令行**(适合装好 Python 的人)和 **网页学习模式**
(推荐,尤其是 Python 小白,Windows 用户双击一个 bat 就能一键启动)。

👉 **详细的上手步骤都在 [使用方法.md](使用方法.md) 里,请先看那个文件。**

简单来说:

- 命令行: `pip install -r requirements.txt` → `python data/generate_data.py`
  → 每章读 `notes.md`、补全 `exercises.py` 里的 `# TODO`、运行看校验、卡住看 `solutions.py`
- 网页: Windows 双击 `启动网页学习.bat`;其他系统在根目录跑 `python -m http.server 8000`
  再打开 <http://localhost:8000/web/>

## 学习顺序

| 章节 | 内容 | 对应的 SQL 知识点 |
|---|---|---|
| `01_numpy` | numpy 数组基础、向量化运算、布尔筛选 | 没有直接对应,但布尔筛选类似 WHERE 的思路 |
| `02_pandas_basics` | DataFrame 是什么、读数据、看结构 | `DESCRIBE`、`SELECT * FROM t LIMIT n` |
| `03_pandas_select_where` | 选列、筛选行、排序、去重、限制条数 | `SELECT`、`WHERE`、`ORDER BY`、`DISTINCT`、`LIMIT` |
| `04_pandas_groupby_having` | 分组聚合、分组后筛选 | `GROUP BY`、聚合函数、`HAVING` |
| `05_pandas_join_union` | 表合并、纵向拼接 | `JOIN`(inner/left/right/outer)、`UNION` |
| `06_pandas_advanced` | 条件取值、空值处理、开窗函数思路 | `CASE WHEN`、`IS NULL`/`COALESCE`、`ROW_NUMBER() OVER(...)` |

## 用到的"表"(练习数据)

三张表,模拟一个简单的电商场景,字段名故意起得和 SQL 表一样:

- `customers`(客户表): `customer_id`, `customer_name`, `city`, `signup_date`
- `products`(商品表): `product_id`, `product_name`, `category`, `price`
- `orders`(订单表): `order_id`, `customer_id`, `product_id`, `order_date`, `quantity`, `status`

三张表之间的关系和 SQL 里一样:`orders.customer_id` 关联 `customers.customer_id`,
`orders.product_id` 关联 `products.product_id`。
