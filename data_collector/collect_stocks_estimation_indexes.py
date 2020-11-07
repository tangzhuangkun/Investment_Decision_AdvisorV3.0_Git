

from bs4 import BeautifulSoup
import urllib.request
import sys
sys.path.append("..")
import log.custom_logger as custom_logger
import database.db_operator as db_operator
import parser.disguise as disguise

class CollectStocksEstimationIndexes:
    # 收集股票的估值指标，滚动市盈率，扣非滚动市盈率，市净率，股息率

    def __init__(self):
        pass

    # https://androidinvest.com/stock/history/sh600519/

    def generate_web_address(self,stock_code):
        # 根据数据库中
        pass

    def get_raw_web_content(self, stock_code):
        # 从乌龟量化获取数据

        # 从数据库中获取一个代理IP和假的文件头
        proxy_ip_address, fake_ua = disguise.Disguise().get_one_IP_UA()

        # 伪装，隐藏IP和文件头
        # 使用ProxyHandler处理器，Proxy代理
        # 注意此处必须使用'http'，不可使用'https',与parse_csindex_detail_json.py 有区别
        proxy_support = urllib.request.ProxyHandler({'http': 'http://' + proxy_ip_address})
        # 通过urllib2.build_opener()方法使用这些代理Handler对象，创建自定义opener
        opener = urllib.request.build_opener(proxy_support)
        # 给用户代理添加User-Agent属性
        opener.addheaders = [('User-Agent', fake_ua)]
        try:
            # opener.open()方法发送请才使用自定义的代理
            response = opener.open(address)
            # 解析返回内容
            response_content = response.read()
            # 将返回内容解析成json结构
            json_content = json.loads(response_content)
            return (json_content)
        except Exception as e:
            print(e)
            return 'there is nothing'



        req_obj = requests.get('https://androidinvest.com/stock/history/sh600519/')
        soup = BeautifulSoup(req_obj.text, 'lxml')

