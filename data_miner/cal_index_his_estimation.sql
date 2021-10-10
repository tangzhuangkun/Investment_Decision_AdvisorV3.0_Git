/* 未完成，2021-10-08 */

/* 创建视图*/
create view jq as
/* 获取最新的数据库中，聚宽的最新指数构成信息 */
(select a.index_code, index_name, stock_code, stock_name, weight, source, a.submission_date
from
/* 每个指数，构成成份，采集日期 */
(select index_code, index_name, stock_code, stock_name, weight, source, submission_date
from index_constituent_stocks_weight
where source = '聚宽'
group by index_code, index_name, stock_code, stock_name, weight, source, submission_date
order by index_code, submission_date, weight desc) a
inner join
/* 每个指数及对应的最新采集日期 */
(select index_code, max(submission_date) as submission_date
from index_constituent_stocks_weight
where source = '聚宽'
group by index_code ) b
on a.index_code = b.index_code
and a.submission_date = b.submission_date
group by a.index_code, index_name, stock_code, stock_name, weight, source, submission_date
order by index_code, weight desc);

/* 创建视图 */
/* 拼接中证的最新前10权重股+每月聚宽中的10位之后的权重股 */
create view mix_top10_with_bottom as
(select index_code, index_name, stock_code, stock_name, weight, source, submission_date from (
/* 拼接中证的最新前十权重股 */
(select index_code, index_name, stock_code, stock_name, weight, source, submission_date
from index_constituent_stocks_weight
where source = '中证'
and submission_date = (select max(submission_date) from index_constituent_stocks_weight))
union all
/* 取出视图中weight倒序，10名之后的 */
(select a.index_code, index_name, stock_code, stock_name, weight, source, a.submission_date from jq a
where
( select count(1) from jq b
				where a.index_code = b.index_code
				and a.weight<b.weight
				order by b.weight desc) >= 10
group by a.index_code, index_name, stock_code, stock_name, weight, source, a.submission_date
order by a.index_code, a.weight)) x
order by index_code, weight desc,stock_code);


/* 创建视图 */
/* 拼接中证的最新前10权重股+每月聚宽中的10位之后的权重股,去除重复股票 */
create view mix_top10_with_bottom_no_repeat as
/* 如果视图（中证的最新前10权重股+每月聚宽中的10位之后的权重股）中股票有重复，以最新日期的为准，忽略旧日期的，去除重复股票 */
(select mt10wb.index_code, index_name, mt10wb.stock_code, stock_name, weight, source, mt10wb.submission_date
from mix_top10_with_bottom mt10wb
inner join
/* 取出视图（中证的最新前10权重股+每月聚宽中的10位之后的权重股）中每个指数及成分股的最新日期 */
(select index_code, stock_code, max(submission_date) as submission_date
from mix_top10_with_bottom
group by index_code,stock_code
order by index_code,stock_code
) mm
on mt10wb.index_code = mm.index_code
and mt10wb.stock_code = mm.stock_code
and mt10wb.submission_date = mm.submission_date
group by mt10wb.index_code, index_name, mt10wb.stock_code, stock_name, weight, source, mt10wb.submission_date
order by mt10wb.index_code, weight desc,mt10wb.stock_code);

/* 利用mysql，基于指数最新的成分股进行计算历史估值信息 */
/* 将计算结果插入另外一个的表中 */
insert into aggregated_data.index_components_historical_estimations (index_code, index_name, historical_date, pe_ttm, pe_ttm_effective_weight,
pe_ttm_nonrecurring, pe_ttm_nonrecurring_effective_weight, pb, pb_effective_weight, pb_wo_gw, pb_wo_gw_effective_weight, ps_ttm, ps_ttm_effective_weight,
pcf_ttm, pcf_ttm_effective_weight, dividend_yield, dividend_yield_effective_weight)

/* 需要验证准确性 */
select a.index_code, a.index_name, c.date as historical_date,
/* 计算指数pe_ttm */
round(sum(
case
		when pe_ttm < 0 then  0
	else
		weight*pe_ttm/100
	end
),5) as pe_ttm,
/* 计算指数pe_ttm的有效权重，舍弃pe_ttm<=0的成份股权重 */
round(sum(
	case
		when pe_ttm < 0 then  0
	else
		weight
	end ),5) as pe_ttm_effective_weight,
/* 计算指数pe_ttm_nonrecurring */
round(sum(
case
		when pe_ttm_nonrecurring < 0 then  0
	else
		weight*pe_ttm_nonrecurring/100
	end
),5) as pe_ttm_nonrecurring,
/* 计算指数pe_ttm_nonrecurring的有效权重，舍弃pe_ttm_nonrecurring<=0的成份股权重 */
round(sum(
	case
		when pe_ttm_nonrecurring < 0 then  0
	else
		weight
	end ),5) as pe_ttm_nonrecurring_effective_weight,
/* 计算指数pb */
round(sum(
case
		when pb < 0 then  0
	else
		weight*pb/100
	end
),5) as pb,
/* 计算指数pb的有效权重，舍弃pb<=0的成份股权重 */
round(sum(
	case
		when pb < 0 then  0
	else
		weight
	end ),5) as pb_effective_weight,
/* 计算指数pb_wo_gw */
round(sum(
case
		when pb_wo_gw < 0 then  0
	else
		weight*pb_wo_gw/100
	end
),5) as pb_wo_gw,
/* 计算指数pb_wo_gw的有效权重，舍弃pb_wo_gw<=0的成份股权重 */
round(sum(
	case
		when pb_wo_gw < 0 then  0
	else
		weight
	end ),5) as pb_wo_gw_effective_weight,
/* 计算指数ps_ttm */
round(sum(
case
		when ps_ttm < 0 then  0
	else
		weight*ps_ttm/100
	end
),5) as ps_ttm,
/* 计算指数ps_ttm的有效权重，舍弃ps_ttm<=0的成份股权重 */
round(sum(
	case
		when ps_ttm < 0 then  0
	else
		weight
	end ),5) as ps_ttm_effective_weight,
/* 计算指数pcf_ttm */
round(sum(
case
		when pcf_ttm < 0 then  0
	else
		weight*pcf_ttm/100
	end
),5) as pcf_ttm,
/* 计算指数pcf_ttm的有效权重，舍弃pcf_ttm<=0的成份股权重 */
round(sum(
	case
		when pcf_ttm < 0 then  0
	else
		weight
	end ),5) as pcf_ttm_effective_weight,
/* 计算指数dividend_yield */
round(sum(
case
		when dividend_yield< 0 then  0
	else
		weight*dividend_yield/100
	end
),5) as dividend_yield,
/* 计算指数dividend_yield的有效权重，舍弃dividend_yield<=0的成份股权重 */
round(sum(
	case
		when dividend_yield< 0 then  0
	else
		weight
	end ),5) as dividend_yield_effective_weight
from
/* 获取指数及其成分股，权重，日期 */
mix_top10_with_bottom_no_repeat a
inner join
/* 获取每个股票的历史指标信息 */
(select stock_code, stock_name, date, pe_ttm, pe_ttm_nonrecurring, pb, pb_wo_gw, ps_ttm, pcf_ttm, dividend_yield
from stocks_main_estimation_indexes_historical_data) c
on a.stock_code = c.stock_code
group by c.date,a.index_code, a.index_name
order by c.date desc;


/* 将视图删除 */
drop view jq;
drop view mix_top10_with_bottom;
drop view mix_top10_with_bottom_no_repeat;