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
			custom_logger.CustomLogger().my_logger('Current working file  '+current_working_dir,'ERROR', 'warning')



if __name__ == "__main__":
	go = Main()
	go.test()