# 每天
# collect_proxy_IP.py 收集代理IP

import sys
sys.path.append('..')
import log.custom_logger as custom_logger

import os


# print(f"current_file_path: {current_file_path}")


class Main:
	def __init__(self):
		pass
	
	def timer(self):
		pass
		
	def test(self):
		current_working_dir = os.getcwd()
		try:
			4/0
		except:
			class_name = self.__class__.__name__
			func_name = sys._getframe().f_code.co_name
			custom_logger.CustomLogger().my_logger('\''+current_working_dir+'/'+class_name+'()/'+func_name+'()\'','MSSSG')



if __name__ == "__main__":
	go = Main()
	go.test()