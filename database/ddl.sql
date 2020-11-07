

-- 创建数据库 parser_component,用于存储与爬虫相关的组件
CREATE DATABASE IF NOT EXISTS parser_component;
-- 授权给用户 investor1 所有权限
GRANT ALL PRIVILEGES ON parser_component.* TO 'investor1'@'%' WITH GRANT OPTION;
# 刷新权限 权限更新后刷新才会起作用
FLUSH PRIVILEGES;




/* --------- user：investor1 ------ */
/* --------- db：parser_component ------ */
/*创建一个表，IP_availability，用于记录ip的可用性 */

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








-- 创建数据库 financial_data,用于存储金融数据
CREATE DATABASE IF NOT EXISTS financial_data;
-- 授权给用户 investor1 所有权限
GRANT ALL PRIVILEGES ON financial_data.* TO 'investor1'@'%' WITH GRANT OPTION;
# 刷新权限 权限更新后刷新才会起作用
FLUSH PRIVILEGES;




/* --------- user：investor1 ------ */
/* --------- db：financial_data ------ */
/*创建一个表，index_constituent_stocks_weights，用于存储 指数构成及权重*/

USE financial_data;
CREATE TABLE IF NOT EXISTS `index_constituent_stocks_weight`(
	`id` MEDIUMINT NOT NULL AUTO_INCREMENT,
	`index_code` VARCHAR(12) NOT NULL COMMENT '指数代码',
	`index_name` VARCHAR(50) NOT NULL COMMENT '指数名称',
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
	`date` DATE COMMENT '日期',
	`pe_ttm`DECIMAL(8,3) COMMENT '滚动市盈率',
	`nonrecurring_pe_ttm`DECIMAL(8,3) COMMENT '扣非滚动市盈率',
	`pb`DECIMAL(7,3) COMMENT '市净率',
	`dyr`DECIMAL(7,3) COMMENT '股息率',
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