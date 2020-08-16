


/* --------- user：fund_investor1 ------ */
/* --------- db：IP_proxy ------ */
/*创建一个表，T_IP_availability，用于记录ip的可用性   
ip_address，主键，ip的地址+端口号，最长可达21位，作为主键可确保数据库中的ip地址不会重复；
is_anonymous，是否为高匿名，是为1，否为0；
is_available，是否仍然可用，是为1，否为0；
type, IP类型，HTTP,HTTPS, (HTTP,HTTPS);
submission_date，提交的日期；
*/


CREATE TABLE IF NOT EXISTS `T_IP_availability`(
	`ip_address` VARCHAR(21) NOT NULL COMMENT '主键，ip的地址+端口号，最长可达21位，作为主键可确保数据库中的ip地址不会重复',
	`is_anonymous` BOOLEAN NOT NULL COMMENT '是否为高匿名，是为1，否为0',
	`is_available` BOOLEAN NOT NULL COMMENT '是否仍然可用，是为1，否为0',
	`type` VARCHAR(21) COMMENT 'IP类型，HTTP,HTTPS, (HTTP,HTTPS)',
	`submission_date` DATE NOT NULL COMMENT '提交的日期',
	PRIMARY KEY ( `ip_address` )
) ENGINE=InnoDB DEFAULT CHARSET=utf8 
COMMENT '用于记录IP的可用性';