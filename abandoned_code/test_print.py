# https://hq.sinajs.cn/list=s_sz399997


import requests
import json

url = 'https://hq.sinajs.cn/list=s_sz399997'

r = requests.get(url)
print(r.text)