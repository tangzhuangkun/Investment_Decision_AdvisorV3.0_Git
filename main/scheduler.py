# 每天
# collect_proxy_IP.py 收集代理IP

import schedule
import time
#import sys
sys.path.append('..')
from log import custom_logger
import log.custom_logger as custom_logger
import target_pool.read_target_fund as read_target_fund
import data_collector.collect_index_weight as collect_index_weight
import parser.check_saved_IP_availability as check_saved_IP_availability


# print(f"current_file_path: {current_file_path}")


class Scheduler:
	def __init__(self):
		pass


	def schedule_plan(self):
		# 调度器，根据时间安排工作
		# 每天：
		# 盘中：	14:40 collect_proxy_IP.py， check_saved_IP_availability.py，
		# 		14:45 fund_strategy_PE_estimation.py
		schedule.every().day.at("22:26").do(check_saved_IP_availability.CheckSavedIPAvailability().main)



		# 盘后：collect_stock_historical_estimation_info.py


		# 每月：generate_save_user_agent.py
		
		# 每月底初（1-10）：收集所跟踪关注指数的成分及权重
		self.collect_tracking_index_weight()





	def collect_tracking_index_weight(self):
		# 收集所跟踪关注指数的成分及权重
		# 输入：无
		# 输出：存入数据

		# 获取当月日期
		monthly_date = time.strftime("%d", time.localtime())
		# 如果介于每月底初（1-10）
		if int(monthly_date) in range(1, 11):
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