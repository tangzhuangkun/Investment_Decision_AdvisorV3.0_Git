#! /usr/bin/env python3
#coding:utf-8
from apscheduler.schedulers.blocking import BlockingScheduler
import sys
sys.path.append('..')
import log.custom_logger as custom_logger
import target_pool.read_collect_target_fund as read_collect_target_fund
import parsers.check_saved_IP_availability as check_saved_IP_availability
import parsers.collect_proxy_IP as collect_proxy_IP
import parsers.generate_save_user_agent as generate_save_user_agent
import data_collector.collect_stock_historical_estimation_info as collect_stock_historical_estimation_info
import notification.notification_plan as notification_plan


class Scheduler:
	# 任务调度器，根据时间安排工作
	def __init__(self):
		pass


	def schedule_plan(self):
		# 调度器，根据时间安排工作
		scheduler = BlockingScheduler()

		#####################      每天运行    ###################################################



		#########  盘前  #########


		#########  盘中  #########

		try:
			# 每日14：39检查已存储的IP的可用性，删除不可用的
			scheduler.add_job(func=check_saved_IP_availability.CheckSavedIPAvailability().main, trigger='cron',
							  month='1-12', day_of_week='mon,tue,wed,thu,fri', hour=14, minute=39,
							  id='weekdayCheckSavedIPAvailability')
		except Exception as e:
			# 抛错
			custom_logger.CustomLogger().log_writter(e, 'error')

		try:
			# 每个交易日14：41收集代理IP
			scheduler.add_job(func=collect_proxy_IP.CollectProxyIP().main, trigger='cron',
							  month='1-12', day_of_week='mon,tue,wed,thu,fri', hour=14, minute=41,
							  id='weekdayCollectProxyIP')
		except Exception as e:
			# 抛错
			custom_logger.CustomLogger().log_writter(e, 'error')

		try:
			# 每个交易日14：49计算并通过邮件发送指数的动态估值信息
			scheduler.add_job(func=notification_plan.NotificationPlan().
							  estimation_notification,
							  trigger='cron',
							  month='1-12', day_of_week='mon,tue,wed,thu,fri', hour=14, minute=49,
							  id='weekdayEmailEstimation')
		except Exception as e:
			# 抛错
			custom_logger.CustomLogger().log_writter(e, 'error')




		#########  盘后  #########

		try:
			# 每个交易日22：01收集所需的股票的估值信息
			scheduler.add_job(func=collect_stock_historical_estimation_info.CollectStockHistoricalEstimationInfo().main, args=('2021-01-02',),
							  trigger='cron',
							  month='1-12', day_of_week='mon,tue,wed,thu,fri', hour=22, minute=1,
							  id='weekdayCollectStockHistoricalEstimationInfo')
		except Exception as e:
			# 抛错
			custom_logger.CustomLogger().log_writter(e, 'error')

		#####################      每周运行    ###################################################

		try:
			# 每个星期天晚上23:00重新生成一批假的user_agent
			scheduler.add_job(func=generate_save_user_agent.GenerateSaveUserAgent().main, trigger='cron',
							  month='1-12', day_of_week='sun', hour=23,
							  id='sundayGenerateFakeUserAgent')
		except Exception as e:
			# 抛错
			custom_logger.CustomLogger().log_writter(e, 'error')




		#####################      每月运行    ###################################################

		try:
			# 每月初（1-30号），每天15：30收集所跟踪关注指数的成分及权重
			scheduler.add_job(func=read_collect_target_fund.ReadCollectTargetFund().collect_tracking_index_weight,
							  trigger='cron', month='1-12', day='1-30',
							  hour=15, minute=30, id='monthly1To10CollectIndexStocksAndWeight')
		except Exception as e:
			# 抛错
			custom_logger.CustomLogger().log_writter(e, 'error')


		# 启动调度器
		try:
			scheduler.start()
		except (KeyboardInterrupt, SystemExit):
			pass




if __name__ == "__main__":
	go = Scheduler()
	go.schedule_plan()








