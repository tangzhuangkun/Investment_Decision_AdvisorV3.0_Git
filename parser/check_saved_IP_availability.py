
import check_IP_availability
import sys
sys.path.append('..')
import database.db_operator as db_operator
import log.custom_logger as custom_logger


class CheckSavedIPAvailability:
	# 检查数据库中保存的所有IP的可用性
	# 不可用的删除掉
	# 运行频率：每天
	
	def __init__(self):
		pass
		
	def get_all_db_IPs(self,db_name):
		# 获取所有的存量IP
		# db_name: 需要查询数据库的名称， 来自 db_config.py 的 DATABASES
		# 输出：IP_dict_list，如[{'ip_address': '95.216.228.204:3128'},,,,]
		
		# sql query查询所有已存的ip地址		
		sql = "SELECT ip_address from T_IP_availability"
		# 从数据库取出
		IP_dict_list = db_operator.DBOperator().select_all(db_name,sql)
		
		return IP_dict_list
		
	def delete_unavailable_ip(self,db_name,ip):
		# 如果ip地址已经失活，从数据库中删除
		# db_name: 需要查询数据库的名称， 来自 db_config.py 的 DATABASE
		# ip: IP地址
		
		#删除该无效的ip地址		
		sql="DELETE from T_IP_availability where ip_address='%s'" % (ip)
		db_operator.DBOperator().operate('delete', db_name, sql)
		
		# 日志记录	
		msg = sql
		custom_logger.CustomLogger().log_writter(msg,'info')
		
	
	def check_ip_availability_and_delete_unable_from_DB(self,db_name,IP_dict_list):
		# db_name: 需要查询数据库的名称， 来自 db_config.py 的 DATABASE
		# IP_dict_list, 输入的是一个list，里面装有dict，形式如：[{'ip_address': '1.24.185.60:9999'}, ,,,]
		# 检查查询到的所有ip的可用性，如果不可用，则从数据库中删除
			
		for ip_dict in IP_dict_list:
			#挨个检查IP活性, 舍去端口号
			is_available = check_IP_availability.CheckIPAvailability().check_single_ip_availability(ip_dict['ip_address'].split(":")[0])
			if not is_available:
				self.delete_unavailable_ip(db_name, ip_dict['ip_address'])	
		


if __name__ == "__main__":
	go = CheckSavedIPAvailability()
	IP_dict_list =  go.get_all_db_IPs('IP_proxy')
	# go.delete_unavailable_ip('IP_proxy', '61.175.192.2:3542')
	go.check_ip_availability_and_delete_unable_from_DB('IP_proxy', IP_dict_list)
		