/* --------- user：investor1 ------ */
/* --------- db：target_pool ------ */
/*创建一个表，fund_target，用于存储基金标的,对应策略*/


USE  target_pool;
CREATE TABLE IF NOT EXISTS `index_target`(
    `id` MEDIUMINT NOT NULL AUTO_INCREMENT,
	`index_code`  VARCHAR(12) COMMENT '跟踪指数代码',
	`index_name`  VARCHAR(50) COMMENT '跟踪指数名称',
    `exchange_location_1`  VARCHAR(10) COMMENT '指数上市地1，如 sh,sz',
    `exchange_location_2`  VARCHAR(10) COMMENT '指数上市地2，如 XSHE, XSHG',
	`hold_or_not`  tinyint(1) COMMENT '当前是否持有,1为持有，0不持有',
	`valuation_methods` VARCHAR(100) COMMENT '估值方法,可以同时存在多个估值方法, pb,pe,ps',
	`B&H_strategy`  VARCHAR(100) COMMENT '买入持有策略,可以同时存在多个',
	`sell_out_strategy` VARCHAR(100) COMMENT '卖出策略,可以同时存在多个',
	`monitoring_frequency` VARCHAR(20) COMMENT '监控频率，secondly, minutely, hourly, daily, weekly, monthly, seasonly, yearly, periodically',
	`p_day` DATE NOT NULL COMMENT '提交的日期',
	`submission_time` TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '提交时间',
	PRIMARY KEY ( `id` )
) ENGINE=InnoDB DEFAULT CHARSET=utf8
COMMENT '跟踪指数及跟踪策略标的池';
