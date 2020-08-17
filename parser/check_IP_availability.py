import sys
sys.path.append('..')
import log.custom_logger as custom_logger
import ipaddress


class CheckIPAvailability:
	# 检查单个IP的活性
	
	def __init__(self):
		pass

	def check_single_ip_availability(self,ip):
		# ip: ip地址，不带端口
		# 异常判断ip地址,利用异常捕捉判断
		# 输出：返回 True 或者 False
		try:  
			ipaddress.ip_address(ip)
			return True
		except Exception as e:
			# 日志记录	
			msg = ip + ' is unavailable  ' + str(e)
			custom_logger.CustomLogger().log_writter(msg,lev='info')
			return False

if __name__ == "__main__":
	go = CheckIPAvailability()
	result = go.check_single_ip_availability('61.134.217.7')
	print(result)