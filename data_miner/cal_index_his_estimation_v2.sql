-- 未完成，2021-09-28

-- 拼接中证的最新前十权重股
(select id, index_code, index_name, stock_code, stock_name, weight, source, submission_date
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
select a.id, a.index_code, index_name, stock_code, stock_name, weight, source, a.submission_date
from
-- 每个指数，构成成份，采集日期
(select id, index_code, index_name, stock_code, stock_name, weight, source, submission_date
from index_constituent_stocks_weight
where source = '聚宽'
group by id, index_code, index_name, stock_code, stock_name, weight, source, submission_date
order by index_code, submission_date, weight desc) a
inner join
-- 每个指数及对应的最新采集日期
(select index_code, max(submission_date) as submission_date
from index_constituent_stocks_weight
where source = '聚宽'
group by index_code ) b
on a.index_code = b.index_code
and a.submission_date = b.submission_date
group by a.id, a.index_code, index_name, stock_code, stock_name, weight, source, submission_date
order by index_code, weight desc;


-- 拼接中证的最新前十权重股
(select id, index_code, index_name, stock_code, stock_name, weight, source, submission_date
from index_constituent_stocks_weight
where source = '中证'
and submission_date = (select max(submission_date) from index_constituent_stocks_weight)) as top

-- 创建视图
create view jq as
-- 获取最新的数据库中，聚宽的最新指数构成信息
(select a.index_code, index_name, stock_code, stock_name, weight, source, a.submission_date
from
-- 每个指数，构成成份，采集日期
(select index_code, index_name, stock_code, stock_name, weight, source, submission_date
from index_constituent_stocks_weight
where source = '聚宽'
group by index_code, index_name, stock_code, stock_name, weight, source, submission_date
order by index_code, submission_date, weight desc) a
inner join
-- 每个指数及对应的最新采集日期
(select index_code, max(submission_date) as submission_date
from index_constituent_stocks_weight
where source = '聚宽'
group by index_code ) b
on a.index_code = b.index_code
and a.submission_date = b.submission_date
group by a.index_code, index_name, stock_code, stock_name, weight, source, submission_date
order by index_code, weight desc);

-- 取出视图中weight倒序，10名之后的
select a.index_code, index_name, stock_code, stock_name, weight, source, a.submission_date from jq a
where
( select count(1) from jq b
				where a.index_code = b.index_code
				and a.weight<b.weight
				order by b.weight desc) >= 10
group by a.index_code, index_name, stock_code, stock_name, weight, source, a.submission_date
order by a.index_code, a.weight;


select index_code, index_name, stock_code, stock_name, weight, source, submission_date from (
-- 拼接中证的最新前十权重股
(select index_code, index_name, stock_code, stock_name, weight, source, submission_date
from index_constituent_stocks_weight
where source = '中证'
and submission_date = (select max(submission_date) from index_constituent_stocks_weight))
union all
-- 取出视图中weight倒序，10名之后的
(select a.index_code, index_name, stock_code, stock_name, weight, source, a.submission_date from jq a
where
( select count(1) from jq b
				where a.index_code = b.index_code
				and a.weight<b.weight
				order by b.weight desc) > 10
group by a.index_code, index_name, stock_code, stock_name, weight, source, a.submission_date
order by a.index_code, a.weight)) x
order by index_code, weight desc,stock_code;

-- 将视图删除
drop view jq;