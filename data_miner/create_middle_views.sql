/* 创建中间视图层，便于后续运算 */

/* 将视图删除 */
drop view if exists jq;
drop view if exists mix_top10_with_bottom;
truncate table mix_top10_with_bottom_no_repeat;

/* 创建视图*/
create view jq as
/* 获取最新的数据库中，聚宽的最新指数构成信息 */
(select a.index_code, index_name, global_stock_code, stock_code, stock_name, weight, source, index_company, a.submission_date
from
/* 每个指数，构成成份，采集日期 */
(select index_code, index_name, global_stock_code,stock_code, stock_name, weight, source, index_company, submission_date
from index_constituent_stocks_weight
where source = '聚宽'
group by index_code, index_name, global_stock_code, stock_code, stock_name, weight, source, index_company,submission_date
order by index_code, submission_date, weight desc) a
inner join
/* 每个指数及对应的最新采集日期 */
(select index_code, max(submission_date) as submission_date
from index_constituent_stocks_weight
where source = '聚宽'
group by index_code ) b
on a.index_code = b.index_code
and a.submission_date = b.submission_date
group by a.index_code, index_name, global_stock_code, stock_code, stock_name, weight, source, index_company, submission_date
order by index_code, weight desc);

/* 创建视图 */
/* 拼接中证的最新前10权重股+每月聚宽中的10位之后的权重股+国证指数 */
create view mix_top10_with_bottom as
(select index_code, index_name, global_stock_code,stock_code, stock_name, weight, source, index_company, submission_date from (
/* 拼接中证的最新前十权重股 */
(select index_code, index_name, global_stock_code,stock_code, stock_name, weight, source, index_company, submission_date
from index_constituent_stocks_weight
where source = '中证官网' and index_company= '中证'
and submission_date = (select max(submission_date) from index_constituent_stocks_weight))
union all
/* 取出视图中中证公司weight倒序，10名之后的 */
(select a.index_code, index_name, global_stock_code, stock_code, stock_name, weight, source, index_company, a.submission_date from jq a
where
index_company= '中证'
and ( select count(1) from jq b
				where a.index_code = b.index_code
				and a.weight<b.weight
				order by b.weight desc) >= 10
group by a.index_code, index_name, global_stock_code, stock_code, stock_name, weight, source, index_company, a.submission_date
order by a.index_code, a.weight)
union all
/* 拼接国证公司的指数信息 */
select c.index_code, index_name, global_stock_code, stock_code, stock_name, weight, source, index_company, c.submission_date from jq c
where c.index_company = '国证'
    ) x
order by index_code, weight desc,stock_code);


/* 插入表格中 */
/* 拼接中证的最新前10权重股+每月聚宽中的10位之后的权重股,去除重复股票+国证指数 */
insert into mix_top10_with_bottom_no_repeat (index_code, index_name, global_stock_code, stock_code, stock_name, weight, source, index_company, submission_date)
/* 如果视图（中证的最新前10权重股+每月聚宽中的10位之后的权重股）中股票有重复，以最新日期的为准，忽略旧日期的，去除重复股票 */
select mt10wb.index_code, index_name, mt10wb.global_stock_code, mt10wb.stock_code, stock_name, weight, source, index_company, mt10wb.submission_date
from mix_top10_with_bottom mt10wb
inner join
/* 取出视图（中证的最新前10权重股+每月聚宽中的10位之后的权重股）中每个指数及成分股的最新日期 */
(select index_code, global_stock_code, stock_code, max(submission_date) as submission_date
from mix_top10_with_bottom
group by index_code, global_stock_code, stock_code
order by index_code,stock_code
) mm
on mt10wb.index_code = mm.index_code
and mt10wb.stock_code = mm.stock_code
and mt10wb.submission_date = mm.submission_date
group by mt10wb.index_code, index_name, mt10wb.global_stock_code, mt10wb.stock_code, stock_name, weight, source, index_company, mt10wb.submission_date
order by mt10wb.index_code, weight desc,mt10wb.stock_code;