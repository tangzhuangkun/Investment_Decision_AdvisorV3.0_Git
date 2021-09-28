-- 未完成，2021-09-28

-- 拼接中证的最新前十权重股
(select index_code, index_name, stock_code, stock_name, weight, source, submission_date
from index_constituent_stocks_weight
where source = '中证'
and submission_date = (select max(submission_date) from index_constituent_stocks_weight))
union all
-- 拼接聚宽的最新的从11到最后一位的权重股
(select index_code, index_name, stock_code, stock_name, weight, source, submission_date
from index_constituent_stocks_weight
where source = '聚宽'
and submission_date = ()
limit 10,9999)

-- 获取最新的数据库中，聚宽的最新指数构成信息
select a.index_code, index_name, stock_code, stock_name, weight, source, a.submission_date
from
(select index_code, index_name, stock_code, stock_name, weight, source, submission_date
from index_constituent_stocks_weight
where source = '聚宽'
group by index_code, index_name, stock_code, stock_name, weight, source, submission_date
order by index_code, submission_date, weight desc) a
inner join
(select index_code, max(submission_date) as submission_date
from index_constituent_stocks_weight
where source = '聚宽'
group by index_code ) b
on a.index_code = b.index_code
and a.submission_date = b.submission_date
group by a.index_code, index_name, stock_code, stock_name, weight, source, submission_date
order by index_code, weight desc