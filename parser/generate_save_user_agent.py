import fake_useragent
import sys
sys.path.append("..")
import log.custom_logger as custom_logger
import database.db_operator as db_operator
import time


class GenerateSaveUserAgent:
	# 先删除数据中已过时的数据
	# 随机生成大量UA，并存入数据库
	# 运行频率：每月
	
	def __init__(self):
		pass
		
	def generate_and_save_user_agent(self):
		# 随机生成大量UA，并存入数据库
		
		# 获取当前时间
		today= time.strftime("%Y-%m-%d", time.localtime())
		
		# 禁用服务器缓存
		ua = fake_useragent.UserAgent(use_cache_server=False)
		
		for i in range(2000):
			# 随机生成UA
			ua = fake_useragent.UserAgent().random
			# 插入数据库
			sql = "INSERT INTO fake_user_agent(ua,submission_date)VALUES ('%s','%s')" %(ua,today)
			db_operator.DBOperator().operate('insert','parser_component', sql)
		
		# 日志记录
		msg = 'Inserted 2000 fake UAs into database'	
		custom_logger.CustomLogger().log_writter(msg,'info')
	
	
	def deleted_outdated_user_agent(self):
		# 删除数据库中过时的UA
		
		# 如果有数据，则删除
		sql = "DELETE FROM IF EXISTS fake_user_agent"
		db_operator.DBOperator().operate('delete','parser_component', sql)
		
		# 日志记录
		msg = 'DELETE all fake UAs from database'	
		custom_logger.CustomLogger().log_writter(msg,'info')
	
	
	def deleted_outdated_and_then_generate_and_save_user_agent(self):
		# 先删除数据中已过时的数据
		# 随机生成大量UA，并存入数据库
		
		self.deleted_outdated_user_agent()
		self.generate_and_save_user_agent()

if __name__ == "__main__":
	go = GenerateSaveUserAgent()
	go.deleted_outdated_and_then_generate_and_save_user_agent()

