import requests
import sys
sys.path.append('..')
import log.custom_logger as custom_logger
import os

class CheckIPAvailability:
	
	def __init__(self):
		pass
		
	def check_single_ip_availability(self,ip):	
		# 输入单个IP，检测IP活性,输出 是否仍存活
		
		# 请求响应头
		headers =  {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}		
		# 检测列表中IP活性
		try:
			proxy = {
				'http':ip
			}
			url1 = 'https://www.baidu.com/'
			# 遍历时，利用访问百度，设定timeout=1,即在1秒内，未收到响应就断开连接
			res = requests.get(url=url1,proxies=proxy,headers=headers,timeout=1)
			# 打印检测信息，elapsed.total_seconds()获取响应的时间
			# print(it +'--',res.elapsed.total_seconds())
			return True
		except BaseException as e:
			# print(e)
			# 日志记录
			msg = ip+' 失活'+ '  '+ str(e)
			custom_logger.CustomLogger().log_writter(msg)
			
			return False


if __name__ == "__main__":
	go = CheckIPAvailability()
	result = go.check_single_ip_availability('165.225.56.62:10605')	