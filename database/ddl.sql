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
	`global_stock_code` VARCHAR(20) NOT NULL COMMENT '股票全球代码',
	`stock_code` VARCHAR(20) NOT NULL COMMENT '股票代码',
	`stock_name` VARCHAR(20) NOT NULL COMMENT '股票名称',
	`stock_exchange_location` VARCHAR(20) NOT NULL COMMENT '股票上市地',
	`weight` DECIMAL(7,4) NOT NULL COMMENT '股票权重',
	`source` VARCHAR(10) NOT NULL COMMENT '数据来源',
	`submission_date` DATE NOT NULL COMMENT '提交的日期',
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




