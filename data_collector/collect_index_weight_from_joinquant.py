import requests
import json
import time
import sys
sys.path.append("..")
import config.joinquant_account_info as joinquant_account_info
import log.custom_logger as custom_logger


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
	
	
	# 存入数据库
	def save_index_stocks_weight_to_db(self, index_code):
		pass
	

if __name__ == "__main__":
	go = CollectIndexWeightFromJoinquant()
	result = go.get_index_stocks_weight('399997.XSHE')
	print(result)
