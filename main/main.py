# 每天
# collect_proxy_IP.py 收集代理IP

import sys
sys.path.append('..')
import log.custom_logger as custom_logger



# print(f"current_file_path: {current_file_path}")


class Main:
	def __init__(self):
		pass
	
	def timer(self):
		pass
		# 每天： collect_proxy_IP.py， check_saved_IP_availability.py
		
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
	go = Main()
	go.test()