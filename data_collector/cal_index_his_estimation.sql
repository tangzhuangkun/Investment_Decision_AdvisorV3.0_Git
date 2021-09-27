# todo 插入后的结果，取出某一天，需要与excel计算结果对比

# 利用mysql，基于指数现在的成分股进行计算历史估值信息
# 将计算结果插入另外一个的表中
insert into aggregated_data.index_components_historical_estimations (index_code, index_name, historical_date, pe_ttm, pe_ttm_effective_weight,
pe_ttm_nonrecurring, pe_ttm_nonrecurring_effective_weight, pb, pb_effective_weight, pb_wo_gw, pb_wo_gw_effective_weight, ps_ttm, ps_ttm_effective_weight,
pcf_ttm, pcf_ttm_effective_weight, dividend_yield, dividend_yield_effective_weight)

select a.index_code, a.index_name, c.date as historical_date,
# 计算指数pe_ttm
sum(
case
		when pe_ttm < 0 then  0
	else
		weight*pe_ttm/100
	end
) as pe_ttm,
# 计算指数pe_ttm的有效权重，舍弃pe_ttm<=0的成份股权重
sum(
	case
		when pe_ttm < 0 then  0
	else
		weight
	end ) as pe_ttm_effective_weight,
# 计算指数pe_ttm_nonrecurring
sum(
case
		when pe_ttm_nonrecurring < 0 then  0
	else
		weight*pe_ttm_nonrecurring/100
	end
) as pe_ttm_nonrecurring,
# 计算指数pe_ttm_nonrecurring的有效权重，舍弃pe_ttm_nonrecurring<=0的成份股权重
sum(
	case
		when pe_ttm_nonrecurring < 0 then  0
	else
		weight
	end ) as pe_ttm_nonrecurring_effective_weight,
# 计算指数pb
sum(
case
		when pb < 0 then  0
	else
		weight*pb/100
	end
) as pb,
# 计算指数pb的有效权重，舍弃pb<=0的成份股权重
sum(
	case
		when pb < 0 then  0
	else
		weight
	end ) as pb_effective_weight,
# 计算指数pb_wo_gw
sum(
case
		when pb_wo_gw < 0 then  0
	else
		weight*pb_wo_gw/100
	end
) as pb_wo_gw,
# 计算指数pb_wo_gw的有效权重，舍弃pb_wo_gw<=0的成份股权重
sum(
	case
		when pb_wo_gw < 0 then  0
	else
		weight
	end ) as pb_wo_gw_effective_weight,
# 计算指数ps_ttm
sum(
case
		when ps_ttm < 0 then  0
	else
		weight*ps_ttm/100
	end
) as ps_ttm,
# 计算指数ps_ttm的有效权重，舍弃ps_ttm<=0的成份股权重
sum(
	case
		when ps_ttm < 0 then  0
	else
		weight
	end ) as ps_ttm_effective_weight,
# 计算指数pcf_ttm
sum(
case
		when pcf_ttm < 0 then  0
	else
		weight*pcf_ttm/100
	end
) as pcf_ttm,
# 计算指数pcf_ttm的有效权重，舍弃pcf_ttm<=0的成份股权重
sum(
	case
		when pcf_ttm < 0 then  0
	else
		weight
	end ) as pcf_ttm_effective_weight,
# 计算指数dividend_yield
sum(
case
		when dividend_yield< 0 then  0
	else
		weight*dividend_yield/100
	end
) as dividend_yield,
# 计算指数dividend_yield的有效权重，舍弃dividend_yield<=0的成份股权重
sum(
	case
		when dividend_yield< 0 then  0
	else
		weight
	end ) as dividend_yield_effective_weight
from
# 获取指数及其成分股，权重，日期
(select index_code, index_name, stock_code, stock_name, submission_date, weight
from index_constituent_stocks_weight) a
inner join
# 与a表拼接，得到各指数最新日期的成分股，权重
(select index_code, index_name, max(submission_date) as submission_date
from index_constituent_stocks_weight
group by index_code, index_name ) b
on a.index_code = b.index_code
and a.index_name = b.index_name
and a.submission_date = b.submission_date
inner join
# 获取每个股票的历史指标信息
(select stock_code, stock_name, date, pe_ttm, pe_ttm_nonrecurring, pb, pb_wo_gw, ps_ttm, pcf_ttm, dividend_yield
from stocks_main_estimation_indexes_historical_data) c
on a.stock_code = c.stock_code
group by c.date,a.index_code, a.index_name
order by c.date desc;
