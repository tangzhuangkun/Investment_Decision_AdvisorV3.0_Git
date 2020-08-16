import logging
import time
import sys
import os
import inspect


class CustomLogger:
	# 自定义的日志工具
	# 只有warning，error，critical才会写入日志文件
	# 会在log文件夹中，按日期生成日志文件
	
	def __init__(self):
		# 当天的日期
		self.today= time.strftime("%Y-%m-%d", time.localtime())
		
	def my_logger(self,working_dir, msg, lev='error'):
		# working_dir: 调用该日志功能的函数路径
		# msg: 需要写入日志文件的信息
		# lev: 日志的级别，默认 error,需要小写
		# 日志级别：debug<info<warning<error<critical 
		# 只有warning，error，critical才会写入日志文件
		# 输出：会在log文件夹中，按日期生成日志文件
		
		
		# 创建logger，如果参数为空则返回root logger
		logger = logging.getLogger("Investment&DecisionAdvisorV3.0")
		# 设置logger日志等级,设置日志器将会处理的日志消息的最低严重级别
		# DEBUG<INFO<WARNING<ERROR<CRITICAL
		logger.setLevel(logging.WARNING)  
		
		# 如果logger.handlers列表为空，且日志级别不为debug和不为info，则添加，否则，直接去写日志
		if not logger.handlers and lev != 'debug' and lev != 'info':
			# 创建handler
			fh = logging.FileHandler("../log/"+self.today+".log",encoding="utf-8")
			ch = logging.StreamHandler()
			
			# 设置输出日志格式
			formatter = logging.Formatter(
				fmt="%(asctime)s %(name)s %(message)s",
				datefmt="%Y-%m-%d  %H:%M:%S %a"
				)
				
			# 为handler指定输出格式
			fh.setFormatter(formatter)
			ch.setFormatter(formatter)
			
			# 为logger添加的日志处理器
			logger.addHandler(fh)
			logger.addHandler(ch)
			
		# 输出不同级别的log,严重级别依次递增
		if lev=='debug':
			logger.debug("DEBUG  "+working_dir+"  "+msg)
		elif lev=='info':
			logger.info("INFO  "+working_dir+"  "+msg)
		elif lev=='warning':
			logger.warning("WARNING  "+working_dir+"  "+msg)
		elif lev=='error':
			logger.error("ERROR  "+working_dir+"  "+msg)
		elif lev=='critical':
			logger.critical("CRITICAL  "+working_dir+"  "+msg)
		else:
			print('WRONG LEVEL')
	
	
	
	def log_writter(self, msg, lev='error'):
		# 该函数便于外部调用
		# msg: 需要写入日志文件的信息
		# lev: 日志的级别，默认 error,需要小写
		# 日志级别：debug<info<warning<error<critical 
		# 只有warning，error，critical才会写入日志文件
		# 输出：会在log文件夹中，按日期生成日志文件
		
		
		current_working_dir = os.path.realpath(sys.argv[0])
		func_name = inspect.stack()[1][3]
		self.my_logger('\''+current_working_dir+'/'+func_name+'()\'',msg,lev)
		

if __name__ == "__main__":
	
	'''
	# 调用时：参考
	# 日志记录
	msg = ip+' 失活'+ '  '+ str(e)
	current_working_dir = os.getcwd()
	class_name = self.__class__.__name__
	func_name = sys._getframe().f_code.co_name
	custom_logger.CustomLogger().my_logger('\''+current_working_dir+'/'+class_name+'()/'+func_name+'()\'', msg)
	
	
	'''
	pass
	

	go = CustomLogger()
	#go.my_logger('/Users/tangzekun/Desktop/KunCloud/Coding_Projects/Investment_Decision_AdvisorV3.0_Git/main',"MSG",'warning')
	go.log_writter("MSG",'warning')

