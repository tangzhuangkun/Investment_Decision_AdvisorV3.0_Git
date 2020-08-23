import fake_useragent



class GenerateSaveUserAgent:
	# 随机生成大量UA，并存入数据库
	# 运行频率：每月
	
	def __init__(self):
		pass
		
	def generate_and_save_user_agent(self):
		# 随机生成大量UA，并存入数据库
		
		# 禁用服务器缓存
		ua = fake_useragent.UserAgent(use_cache_server=False)
		# 不缓存数据
		# ua = fake_useragent.UserAgent(cache=False)
		# 忽略ssl验证
		# ua = fake_useragent.UserAgent(verify_ssl=False)
		
		for i in range(1000):
			# 随机生成UA
			ua = fake_useragent.UserAgent().random
			print(ua)
		
		


if __name__ == "__main__":
	go = GenerateSaveUserAgent()
	go.generate_and_save_user_agent()

