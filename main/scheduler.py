#! /usr/bin/env python3
#coding:utf-8
from apscheduler.schedulers.blocking import BlockingScheduler
import sys
sys.path.append('..')
import log.custom_logger as custom_logger
import parsers.check_saved_IP_availability as check_saved_IP_availability
import parsers.collect_proxy_IP as collect_proxy_IP
import parsers.generate_save_user_agent as generate_save_user_agent
import data_collector.collect_stock_historical_estimation_info as collect_stock_historical_estimation_info
import notification.notification_plan_during_trading as notification_plan_during_trading
import data_collector.collect_trading_days as collect_trading_days
import data_miner.calculate_index_historial_estimations as calculate_index_historial_estimations
import data_collector.collect_index_weight as collect_index_weight
import data_collector.collect_csindex_top_10_stocks_weight_daily as collect_csindex_top_10_stocks_weight_daily

class Scheduler:
	# 任务调度器，根据时间安排工作
	def __init__(self):
		pass


	def schedule_plan(self):
		# 调度器，根据时间安排工作
		scheduler = BlockingScheduler()

		#####################      每天运行    ###################################################



		#########  盘前(00:00-9:29)  #########


		#########  盘中(9:30-15:00)  #########

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
			# 每个交易日14：49计算并通过邮件/微信发送指数的动态估值信息
			scheduler.add_job(func=notification_plan_during_trading.NotificationPlanDuringTrading().
							  estimation_notification,
							  trigger='cron',
							  month='1-12', day_of_week='mon,tue,wed,thu,fri', hour=14, minute=49,
							  id='weekdayEmailEstimation')
		except Exception as e:
			# 抛错
			custom_logger.CustomLogger().log_writter(e, 'error')




		#########  盘后(15:00-23:59)  #########
		try:
			# 每个交易日18：01收集交易日信息
			scheduler.add_job(func=collect_trading_days.CollectTradingDays().save_all_trading_days_into_db,
							  trigger='cron',
							  month='1-12', day_of_week='mon,tue,wed,thu,fri', hour=18, minute=1,
							  id='weekdayCollectTradingDays')
		except Exception as e:
			# 抛错
			custom_logger.CustomLogger().log_writter(e, 'error')

		try:
			# 每个交易日18：04收集所需的股票的估值信息
			scheduler.add_job(func=collect_stock_historical_estimation_info.CollectStockHistoricalEstimationInfo().main, args=('2021-01-02',),
							  trigger='cron',
							  month='1-12', day_of_week='mon,tue,wed,thu,fri', hour=18, minute=4,
							  id='weekdayCollectStockHistoricalEstimationInfo')
		except Exception as e:
			# 抛错
			custom_logger.CustomLogger().log_writter(e, 'error')

		try:
			# 每个交易日20：05收集中证官网指数的最新构成信息
			scheduler.add_job(func=collect_csindex_top_10_stocks_weight_daily.CollectCSIndexTop10StocksWeightDaily().main,
							  trigger='cron',
							  month='1-12', day_of_week='mon,tue,wed,thu,fri', hour=20, minute=5,
							  id='weekdayCollectCSIndexTop10StocksWeight')
		except Exception as e:
			# 抛错
			custom_logger.CustomLogger().log_writter(e, 'error')

		try:
			# 每个交易日20：08计算指数估值
			scheduler.add_job(func=calculate_index_historial_estimations.CalculateIndexHistoricalEstimations().main,
							  trigger='cron',
							  month='1-12', day_of_week='mon,tue,wed,thu,fri', hour=20, minute=8,
							  id='weekdayCalculateIndexHistoricalEstimations')
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
			# 每月初（1-10号），每天20：01收集所跟踪关注指数的成分及权重
			scheduler.add_job(func=collect_index_weight.CollectIndexWeight().collect_tracking_index_weight,
							  trigger='cron', month='1-12', day='1-10',
							  hour=20, minute=1, id='monthly1To10CollectIndexStocksAndWeight')
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








