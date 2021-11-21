/* --------- user：investor1 ------ */
/* --------- db：parser_component ------ */
/*创建一个表，IP_availability，用于记录ip的可用性 */

/*
USE parser_component;
CREATE TABLE IF NOT EXISTS `IP_availability`(
	`ip_address` VARCHAR(21) NOT NULL COMMENT '主键，ip的地址+端口号，最长可达21位，作为主键可确保数据库中的ip地址不会重复',
	`is_anonymous` BOOLEAN NOT NULL COMMENT '是否为高匿名，是为1，否为0',
	`is_available` BOOLEAN NOT NULL COMMENT '是否仍然可用，是为1，否为0',
	`type` VARCHAR(21) COMMENT 'IP类型，HTTP,HTTPS, (HTTP,HTTPS)',
	`submission_date` DATE NOT NULL COMMENT '提交的日期',
	PRIMARY KEY ( `ip_address` )
) ENGINE=InnoDB DEFAULT CHARSET=utf8 
COMMENT '记录IP的可用性';
*/


USE parser_component;
DROP TABLE IF EXISTS `IP_availability`;
CREATE TABLE IF NOT EXISTS `IP_availability`(
	`ip_address` VARCHAR(21) NOT NULL COMMENT '主键，ip的地址+端口号，最长可达21位，作为主键可确保数据库中的ip地址不会重复',
	`is_anonymous` BOOLEAN NOT NULL COMMENT '是否为高匿名，是为1，否为0',
	`is_available` BOOLEAN NOT NULL COMMENT '是否仍然可用，是为1，否为0',
	`type` VARCHAR(21) COMMENT 'IP类型，HTTP,HTTPS, (HTTP,HTTPS)',
	`submission_date` TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '提交时间',
	PRIMARY KEY ( `ip_address` )
) ENGINE=InnoDB DEFAULT CHARSET=utf8
COMMENT '记录IP的可用性';




/* --------- user：investor1 ------ */
/* --------- db：parser_component ------ */
/*创建一个表，fake_user_agent，用于存储生成的假UA（用户代理）*/

USE parser_component;
CREATE TABLE IF NOT EXISTS `fake_user_agent`(
	`id` MEDIUMINT NOT NULL AUTO_INCREMENT,
	`ua` VARCHAR(1000) NOT NULL COMMENT '用户代理',
	`submission_date` DATE NOT NULL COMMENT '提交的日期',
	PRIMARY KEY ( `id` )
) ENGINE=InnoDB DEFAULT CHARSET=utf8 
COMMENT '生成的假UA（用户代理）';


/* --------- user：investor1 ------ */
/* --------- db：financial_data ------ */
/*创建一个表，index_constituent_stocks_weights，用于存储 指数构成及权重*/

USE financial_data;
CREATE TABLE IF NOT EXISTS `index_constituent_stocks_weight`(
	`id` MEDIUMINT NOT NULL AUTO_INCREMENT,
	`index_code` VARCHAR(12) NOT NULL COMMENT '指数代码',
	`index_name` VARCHAR(50) NOT NULL COMMENT '指数名称',
	`global_stock_code` VARCHAR(20) DEFAULT NULL COMMENT '股票全球代码',
	`stock_code` VARCHAR(20) NOT NULL COMMENT '股票代码',
	`stock_name` VARCHAR(20) NOT NULL COMMENT '股票名称',
	`stock_exchange_location` VARCHAR(20) DEFAULT NULL COMMENT '股票上市地',
	`weight` DECIMAL(21,18) NOT NULL COMMENT '股票权重',
	`source` VARCHAR(10) DEFAULT NULL COMMENT '数据来源',
	`index_company` VARCHAR(20) DEFAULT NULL COMMENT '指数开发公司',
	`submission_date` DATE DEFAULT NULL COMMENT '提交的日期',
	`submission_time` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '提交时间',
	PRIMARY KEY ( `id` )
	)ENGINE=InnoDB DEFAULT CHARSET=utf8
COMMENT '指数构成及权重';	



/* --------- user：investor1 ------ */
/* --------- db：financial_data ------ */
/*创建一个表，stocks_main_estimation_indexes_historical_data，用于存储 股票估值指标历史数据*/

USE financial_data;
CREATE TABLE IF NOT EXISTS `stocks_main_estimation_indexes_historical_data`(
	`id` INT NOT NULL AUTO_INCREMENT,
	`stock_code` VARCHAR(20) NOT NULL COMMENT '股票代码',
	`stock_name` VARCHAR(20) NOT NULL COMMENT '股票名称',
	`date` DATE NOT NULL COMMENT '日期',
	`pe_ttm` DECIMAL(24,16) NOT NULL COMMENT '滚动市盈率',
	`pe_ttm_nonrecurring` DECIMAL(24,16) NOT NULL COMMENT '扣非滚动市盈率',
	`pb` DECIMAL(24,16) NOT NULL COMMENT '市净率',
	`pb_wo_gw` DECIMAL(24,16) DEFAULT NULL COMMENT '扣商誉市净率',
	`ps_ttm` DECIMAL(24,16)DEFAULT NULL COMMENT '滚动市销率',
	`pcf_ttm` DECIMAL(24,16) DEFAULT NULL COMMENT '滚动市现率',
	`ev_ebit` DECIMAL(24,16) DEFAULT NULL COMMENT 'EV/EBIT企业价值倍数 ',
	`stock_yield` DECIMAL(24,18) DEFAULT NULL COMMENT '股票收益率',
	`dividend_yield` DECIMAL(24,18) DEFAULT NULL COMMENT '股息率',
	`share_price` DECIMAL(20,4) DEFAULT NULL COMMENT '股价',
	`turnover` BIGINT DEFAULT NULL COMMENT '成交量',
	`fc_rights` DECIMAL(12,6) DEFAULT NULL COMMENT '前复权',
	`bc_rights` DECIMAL(12,6)DEFAULT NULL COMMENT '后复权',
	`lxr_fc_rights` DECIMAL(12,6)DEFAULT NULL COMMENT '理杏仁前复权',
	`shareholders` BIGINT DEFAULT NULL COMMENT '股东人数',
	`market_capitalization` DECIMAL(24,6) DEFAULT NULL COMMENT '市值',
	`circulation_market_capitalization` DECIMAL(24,6) DEFAULT NULL COMMENT '流通市值',
	`free_circulation_market_capitalization` DECIMAL(24,6) DEFAULT NULL COMMENT '自由流通市值',
	`free_circulation_market_capitalization_per_capita` DECIMAL(24,6) DEFAULT NULL COMMENT '人均自由流通市值',
	`financing_balance` DECIMAL(24,6) DEFAULT 0 COMMENT '融资余额',
	`securities_balances` DECIMAL(24,6) DEFAULT 0 COMMENT '融券余额',
	`stock_connect_holding_amount` DECIMAL(24,6) DEFAULT NULL COMMENT '陆股通持仓金额',
	`submission_time` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '提交时间',
	PRIMARY KEY ( `id` )
	)ENGINE=InnoDB DEFAULT CHARSET=utf8
COMMENT '股票估值指标历史数据';





/*

-- 创建数据库 target_pool,用作标的池，存储标的物，对应交易策略
CREATE DATABASE IF NOT EXISTS target_pool;
-- 授权给用户 investor1 所有权限
GRANT ALL PRIVILEGES ON target_pool.* TO 'investor1'@'%' WITH GRANT OPTION;
# 刷新权限 权限更新后刷新才会起作用
FLUSH PRIVILEGES;
*/


/* --------- user：investor1 ------ */
/* --------- db：target_pool ------ */
/*创建一个表，fund_target，用于存储基金标的,对应策略*/

/*
DATABASE target_pool;
CREATE TABLE IF NOT EXISTS `fund_target`(
	`fund_code` VARCHAR(12) NOT NULL COMMENT '基金代码',
	`fund_name` VARCHAR(50) NOT NULL COMMENT '基金名称',
	`fund_type`  VARCHAR(12) NOT NULL COMMENT '基金类型，指数，混合，股票，债券型，联接，，，',
	`tracking_index`  VARCHAR(50) COMMENT '跟踪指数名称',
	`tracking_index_code`  VARCHAR(12) COMMENT '跟踪指数代码',
	`hold_or_not`  tinyint(1) COMMENT '当前是否持有,1为持有，0不持有',
	`valuation_method` VARCHAR(100) COMMENT '估值方法',
	`B&H_strategy`  VARCHAR(100) COMMENT '买入持有策略',
	`sell_out_strategy` VARCHAR(100) COMMENT '卖出策略',
	`monitoring_frequency` VARCHAR(20) COMMENT '监控频率',
	`submission_date` DATE NOT NULL COMMENT '提交的日期',
	PRIMARY KEY ( `fund_code` )
) ENGINE=InnoDB DEFAULT CHARSET=utf8 
COMMENT '基金标的池';
*/



/* --------- user：investor1 ------ */
/* --------- db：financial_data ------ */
/*创建一个表，trading_days，用于存储 交易日期*/

USE financial_data;
DROP TABLE IF EXISTS `trading_days`;
CREATE TABLE IF NOT EXISTS `trading_days`(
	`id` MEDIUMINT NOT NULL AUTO_INCREMENT,
	`trading_date` DATE NOT NULL COMMENT '交易日期',
	`area` VARCHAR(50) NOT NULL COMMENT '地区',
	`source` VARCHAR(10) NOT NULL COMMENT '数据来源',
	`submission_time` TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '提交时间',
	UNIQUE INDEX (trading_date),
	PRIMARY KEY ( `id`)
	)ENGINE=InnoDB DEFAULT CHARSET=utf8
COMMENT '交易日期';



/* --------- user：investor1 ------ */
/* --------- db：financial_data ------ */
/*创建一个表，chn_gov_bonds_rates_di，用于存储 中国国债到期收益率，日增表*/

USE financial_data;
CREATE TABLE IF NOT EXISTS `chn_gov_bonds_rates_di`(
	`id` INT NOT NULL AUTO_INCREMENT,
	`1m` VARCHAR(20) NOT NULL COMMENT '1月期限到期利率',
	`2m` VARCHAR(20) DEFAULT NULL COMMENT '2月期限到期利率',
	`3m` VARCHAR(20) DEFAULT NULL COMMENT '3月期限到期利率',
	`6m` VARCHAR(20) DEFAULT NULL COMMENT '6月期限到期利率',
	`9m` VARCHAR(20) DEFAULT NULL COMMENT '9月期限到期利率',
	`1y` VARCHAR(20) DEFAULT NULL COMMENT '1年期限到期利率',
	`2y` VARCHAR(20) DEFAULT NULL COMMENT '2年期限到期利率',
	`3y` VARCHAR(20) DEFAULT NULL COMMENT '3年期限到期利率',
	`5y` VARCHAR(20) DEFAULT NULL COMMENT '5年期限到期利率',
	`7y` VARCHAR(20) DEFAULT NULL COMMENT '7年期限到期利率',
	`10y` VARCHAR(20) DEFAULT NULL COMMENT '10年期限到期利率',
	`trading_day` DATE NOT NULL COMMENT '交易日期',
	`source` VARCHAR(10) NOT NULL COMMENT '数据来源',
	`submission_date` DATE DEFAULT NULL COMMENT '提交的日期',
	`submission_time` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '提交时间',
	UNIQUE INDEX(trading_day),
	PRIMARY KEY ( `id` )
	)ENGINE=InnoDB DEFAULT CHARSET=utf8
COMMENT '中国国债到期收益率';


/* --------- user：investor1 ------ */
/* --------- db：financial_data ------ */
/*创建一个表，index_estimation_from_lxr，用于存储 理杏仁的指数估值信息*/

USE financial_data;
DROP TABLE IF EXISTS `index_estimation_from_lxr_di`;
CREATE TABLE IF NOT EXISTS `index_estimation_from_lxr_di`(
	`id` MEDIUMINT NOT NULL AUTO_INCREMENT,
	`index_code` VARCHAR(20) NOT NULL COMMENT '指数代码',
	`index_name` VARCHAR(20) NOT NULL COMMENT '指数名称',
	`trading_date` DATE NOT NULL COMMENT '交易日期',
	`pe_ttm_mcw` DECIMAL(22,17) NOT NULL COMMENT '滚动市盈率市值加权，所有样品公司市值之和 / 所有样品公司归属于母公司净利润之和',
	`pe_ttm_ew` DECIMAL(22,17) NOT NULL COMMENT '滚动市盈率等权，算出所有公司的PE-TTM，然后通过(n / ∑(1 / PE.i))计算出来',
	`pe_ttm_ewpvo` DECIMAL(22,17) NOT NULL COMMENT '滚动市盈率正数等权，剔除所有不赚钱的企业',
	`pe_ttm_avg` DECIMAL(22,17) NOT NULL COMMENT '滚动市盈率平均值，算出所有样品公司的滚动市盈率，剔除负数，然后使用四分位距（interquartile range, IQR）去除极端值，然后加和求平均值',
	`pe_ttm_median` DECIMAL(22,17) NOT NULL COMMENT '滚动市盈率中位数，算出所有样品公司的市盈率，然后排序，然后取最中间的那个数；如果是偶数，那么取中间的两个，加和求半',
	`pb_mcw` DECIMAL(22,17) NOT NULL COMMENT '市净率市值加权，所有样品公司市值之和 / 净资产之和',
	`pb_ew` DECIMAL(22,17) NOT NULL COMMENT '市净率等权，算出所有公司的PB，然后通过(n / ∑(1 / PB.i))计算出来',
	`pb_ewpvo` DECIMAL(22,17) NOT NULL COMMENT '市净率正数等权，剔除所有净资产为负数的企业',
	`pb_avg` DECIMAL(22,17) NOT NULL COMMENT '市净率平均值',
	`pb_median` DECIMAL(22,17) NOT NULL COMMENT '市净率中位数，算出所有样品公司的市净率，然后排序，然后取最中间的那个数；如果是偶数，那么取中间的两个，加和求半',
	`ps_ttm_mcw` DECIMAL(22,17) NOT NULL COMMENT '市销率市值加权，所有样品公司市值之和 / 营业额之和',
	`ps_ttm_ew` DECIMAL(22,17) NOT NULL COMMENT '市销率等权，算出所有公司的PS-TTM，然后通过(n / ∑(1 / PS.i))计算出来',
	`ps_ttm_ewpvo` DECIMAL(22,17) NOT NULL COMMENT '市销率正数等权，剔除所有营业额为0的企业',
	`ps_ttm_avg` DECIMAL(22,17) NOT NULL COMMENT '市销率平均值',
	`ps_ttm_median` DECIMAL(22,17) NOT NULL COMMENT '市销率中位数，算出所有样品公司的市销率，然后排序，然后取最中间的那个数；如果是偶数，那么取中间的两个，加和求半',
	`dyr_mcw` DECIMAL(23,20) NOT NULL COMMENT '股息率市值加权，所有样品公司市值之和 / 分红之和',
	`dyr_ew` DECIMAL(23,20) NOT NULL COMMENT '股息率等权，算出所有公司的DYR，然后通过(n / ∑(1 / DYR.i))计算出来',
	`dyr_ewpvo` DECIMAL(23,20) NOT NULL COMMENT '股息率正数等权，剔除所有不分红的企业',
	`dyr_avg` DECIMAL(23,20) NOT NULL COMMENT '股息率平均值',
	`dyr_median` DECIMAL(23,20) NOT NULL COMMENT '股息率中位数，算出所有样品公司的股息率，然后排序，然后取最中间的那个数；如果是偶数，那么取中间的两个，加和求半',
	`source` VARCHAR(10) NOT NULL COMMENT '数据来源',
	`submission_date` DATE DEFAULT NULL COMMENT '提交的日期',
	`submission_time` TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '提交时间',
	UNIQUE INDEX (index_code, trading_date, source),
	PRIMARY KEY ( `id`)
	)ENGINE=InnoDB DEFAULT CHARSET=utf8
COMMENT '理杏仁的指数估值信息';






/* --------- user：investor1 ------ */
/* --------- db：aggregated_data ------ */
/*创建一个表，index_components_historical_estimations，用于存储 基于指数最新成分股及权重得到的历史每日估值*/

USE aggregated_data;
DROP TABLE IF EXISTS `index_components_historical_estimations`;
CREATE TABLE IF NOT EXISTS `index_components_historical_estimations`(
	`id` int(10) NOT NULL AUTO_INCREMENT,
	`index_code` VARCHAR(12) NOT NULL COMMENT '指数代码',
	`index_name` VARCHAR(50) NOT NULL COMMENT '指数名称',
	`historical_date` DATE NOT NULL COMMENT '历史日期',
	`pe_ttm` DECIMAL(10,5) DEFAULT NULL COMMENT '滚动市盈率',
    `pe_ttm_effective_weight` DECIMAL(10,5) DEFAULT NULL COMMENT '滚动市盈率有效权重',
	`pe_ttm_nonrecurring` DECIMAL(10,5) DEFAULT NULL COMMENT '扣非滚动市盈率',
	`pe_ttm_nonrecurring_effective_weight` DECIMAL(10,5) DEFAULT NULL COMMENT '扣非滚动市盈率有效权重',
	`pb` DECIMAL(10,5) DEFAULT NULL COMMENT '市净率',
	`pb_effective_weight` DECIMAL(10,5) DEFAULT NULL COMMENT '市净率有效权重',
	`pb_wo_gw` DECIMAL(10,5) DEFAULT NULL COMMENT '扣商誉市净率',
	`pb_wo_gw_effective_weight` DECIMAL(10,5) DEFAULT NULL COMMENT '扣商誉市净率有效权重',
	`ps_ttm` DECIMAL(10,5) DEFAULT NULL COMMENT '滚动市销率',
	`ps_ttm_effective_weight` DECIMAL(10,5) DEFAULT NULL COMMENT '滚动市销率有效权重',
	`pcf_ttm` DECIMAL(10,5) DEFAULT NULL COMMENT '滚动市现率',
	`pcf_ttm_effective_weight` DECIMAL(10,5) DEFAULT NULL COMMENT '滚动市现率有效权重',
    `dividend_yield` DECIMAL(10,5) DEFAULT NULL COMMENT '股息率',
    `dividend_yield_effective_weight` DECIMAL(10,5) DEFAULT NULL COMMENT '股息率有效权重',
	`submission_time` TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '提交时间',
	UNIQUE INDEX (index_code, historical_date),
	PRIMARY KEY ( `id` )
	)ENGINE=InnoDB DEFAULT CHARSET=utf8
COMMENT '基于指数最新成分股及权重得到的历史每日估值';


/* --------- user：investor1 ------ */
/* --------- db：aggregated_data ------ */
/*创建一个表，stock_bond_ratio_di，用于存储 每日股债比*/

USE aggregated_data;
DROP TABLE IF EXISTS `stock_bond_ratio_di`;
CREATE TABLE IF NOT EXISTS `stock_bond_ratio_di`(
	`id` int(10) NOT NULL AUTO_INCREMENT,
	`index_code` VARCHAR(12) NOT NULL COMMENT '指数代码',
	`index_name` VARCHAR(50) NOT NULL COMMENT '指数名称',
	`trading_date` DATE NOT NULL COMMENT '交易日期',
	`pe` DECIMAL(22,17) DEFAULT NULL COMMENT '市盈率',
	`stock_yield_rate` DECIMAL(9,6) DEFAULT NULL COMMENT '股票收益率，市盈率倒数',
	`10y_bond_rate` DECIMAL(9,6) DEFAULT NULL COMMENT '10年期国债收益率',
	`ratio` DECIMAL(13,10) DEFAULT NULL COMMENT '股债收益比',
	`submission_time` TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '提交时间',
	UNIQUE INDEX (index_code, trading_date),
	PRIMARY KEY ( `id` )
	)ENGINE=InnoDB DEFAULT CHARSET=utf8
COMMENT '每日股债比';




