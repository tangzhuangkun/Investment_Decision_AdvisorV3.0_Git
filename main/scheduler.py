from apscheduler.schedulers.blocking import BlockingScheduler
import sys
sys.path.append('..')
import log.custom_logger as custom_logger
import target_pool.read_target_fund as read_target_fund
import data_collector.collect_index_weight as collect_index_weight
import parsers.check_saved_IP_availability as check_saved_IP_availability
import parsers.collect_proxy_IP as collect_proxy_IP
import parsers.generate_save_user_agent as generate_save_user_agent


# print(f"current_file_path: {current_file_path}")


class Scheduler:
	def __init__(self):
		pass


	def schedule_plan(self):
		# 调度器，根据时间安排工作
		scheduler = BlockingScheduler()

		#####################      每天运行    ###################################################
		# 	缺	14:45 fund_strategy_PE_estimation.py


		#########  盘前  #########



		#########  盘中  #########
		# 每个交易日14：39检查已存储的IP的可用性，删除不可用的
		scheduler.add_job(func=check_saved_IP_availability.CheckSavedIPAvailability().main, trigger='cron',
						  month='1-12', day_of_week='mon,tue,wed,thu,fri', hour=23, minute=13,
						  id='weekdayCheckSavedIPAvailability')

		# 每个交易日14：41收集代理IP
		scheduler.add_job(func=collect_proxy_IP.CollectProxyIP().main, trigger='cron',
						  month='1-12', day_of_week='mon,tue,wed,thu,fri', hour=23, minute=21,
						  id='weekdayCollectProxyIP')


		#########  盘后  #########
		# 盘后：collect_stock_historical_estimation_info.py




		#####################      每周运行    ###################################################
		# 每个星期天晚上23:00重新生成一批假的user_agent
		scheduler.add_job(func=generate_save_user_agent.GenerateSaveUserAgent().main, trigger='cron',
						  month='1-12', day_of_week='sun', hour=23,
						  id='sundayGenerateFakeUserAgent')



		#####################      每月运行    ###################################################
		# 每月初（1-10号），每天15：30收集所跟踪关注指数的成分及权重
		scheduler.add_job(func=self.collect_tracking_index_weight, trigger='cron', month='1-12', day='1-10',
						  hour=23, minute=50, id='monthly1-10CollectIndexStocksAndWeight')

		# 启动调度器
		try:
			scheduler.start()
		except (KeyboardInterrupt, SystemExit):
			pass


	def collect_tracking_index_weight(self):
		# 收集所跟踪关注指数的成分及权重
		# 输入：无
		# 输出：存入数据

		'''
		# 获取当月日期
		monthly_date = time.strftime("%d", time.localtime())
		# 如果介于每月底初（1-10）
		if int(monthly_date) in range(1, 11):
			# 获取标的池中跟踪关注指数及他们的中文名称,字典形式。如，{'399396.XSHE': '国证食品', '000932.XSHG': '中证主要消费',,,,}
			tracking_indexes_names_dict = read_target_fund.ReadTargetFund().getIndexesAndTheirNames()
			# 收集指数的成分及权重
			for index in tracking_indexes_names_dict:
				collect_index_weight.CollectIndexWeight().main(index, tracking_indexes_names_dict.get(index))
		'''

		# 获取标的池中跟踪关注指数及他们的中文名称,字典形式。如，{'399396.XSHE': '国证食品', '000932.XSHG': '中证主要消费',,,,}
		tracking_indexes_names_dict = read_target_fund.ReadTargetFund().getIndexesAndTheirNames()
		# 收集指数的成分及权重
		for index in tracking_indexes_names_dict:
			collect_index_weight.CollectIndexWeight().main(index, tracking_indexes_names_dict.get(index))


		
	def test(self):
		
		try:
			4/0
			'''
		except:
			current_working_dir = os.getcwd()
			class_name = self.__class__.__name__
			func_name = sys._getframe().f_code.co_name
			custom_logger.CustomLogger().my_logger('\''+current_working_dir+'/'+class_name+'()/'+func_name+'()\'','MSSSG')
			'''
		
		except Exception as e:
			#custom_logger.CustomLogger().get_running_file_path()
			# custom_logger.CustomLogger().get_running_class_name()
			#custom_logger.CustomLogger().get_running_function_name()
			custom_logger.CustomLogger().log_writter(str(e))



if __name__ == "__main__":
	go = Scheduler()
	go.schedule_plan()








