import requests
import json
import time
import sys
sys.path.append("..")
import config.joinquant_account_info as joinquant_account_info
import log.custom_logger as custom_logger
import database.db_operator as db_operator


class CollectIndexWeightFromJoinquant:
	# 从聚宽获取指数的权重数据，并存入数据库
	# 运行频率：每月底

	def __init__(self):
		pass
	
	def get_index_stocks_weight(self,index_code):
		# 获取指数权重 
		# 输入：index_code，指数代码，例如：399997.XSHE
		# 输出：指数构成信息
		
		url, body, token = joinquant_account_info.JoinquantAccountInfo().get_token()
		# 获取当前时间
		today= time.strftime("%Y-%m-%d", time.localtime())
		body={
				"method": "get_index_weights",
				"token": token,
				"code": index_code,
				"date": today
			}
			
		try:
			# 获取聚宽返回的指数构成信息
			response = requests.post(url, data = json.dumps(body))
			# print(response.text)
			return response.text
			
		except Exception as e:
			# 日志记录	
			msg = 'Failed to get joinquant index weights' + '  '+ str(e)
			custom_logger.CustomLogger().log_writter(msg,'error')
	
	

	def save_index_stocks_weight_to_db(self, index_code,index_name):
		# 存入数据库
		# 输入：index_code，指数代码，例如：399997.XSHE
		# 		index_name，指数名称，例如：中证白酒指数
		# 输出：指数成分股存入数据库
		index_stocks_weight_str = self.get_index_stocks_weight(index_code)
		# 将聚宽传回的指数成分股及其权重信息，由string转化为list，便于处理
		index_holding_detail_list = index_stocks_weight_str.replace('\n', ',').split(',')
		# 获取今天日期
		today = time.strftime("%Y-%m-%d", time.localtime())

		stock_code = ''
		stock_name = ''
		weight = 0

		# 聚宽返回的指数成分股的格式，每4个为一个循环，从第5个开始为正式数据['code','display_name','date', 'weight', '000568.XSHE','泸州老窖','2020-01-28','4.3930','000596.XSHE','古井贡酒','2020-01-28','1.0820',,,,]
		for i in range(4, len(index_holding_detail_list)):
			if i % 4 == 0:
				# 获取股票代码
				stock_code = index_holding_detail_list[i]
			elif i % 4 == 1:
				# 获取股票名称
				stock_name = index_holding_detail_list[i]
			elif i % 4 == 3:
				# 获取股票权重F
				weight = index_holding_detail_list[i]

				# 插入的SQL
				inserting_sql = "INSERT INTO index_constituent_stocks_weight(index_code,index_name,stock_code,stock_name,weight,source,submission_date)VALUES ('%s','%s','%s','%s','%s','%s','%s')" % (
				index_code, index_name, stock_code, stock_name, weight, '聚宽', today)
				db_operator.DBOperator().operate("insert","financial_data",inserting_sql)


	def get_query_count(self):
		# 获取查询剩余条数
		url, body, token = joinquant_account_info.JoinquantAccountInfo().get_token()
		body = {
			"method": "get_query_count",
			"token": token,
		}
		try:
			# 获取聚宽返回的剩余条数
			response = requests.post(url, data=json.dumps(body))
			return response.text

		except Exception as e:
			# 日志记录
			msg = 'Failed to get joinquant query count' + '  ' + str(e)
			custom_logger.CustomLogger().log_writter(msg, 'error')

if __name__ == "__main__":
	go = CollectIndexWeightFromJoinquant()
	result = go.get_index_stocks_weight('399997.XSHE')
	go.save_index_stocks_weight_to_db("399997.XSHE","中证白酒")
	#result = go.get_query_count()
	print(result)
	#print(len(result))
