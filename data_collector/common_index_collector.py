import requests

import decimal
import time
import sys
sys.path.append("..")
import parsers.disguise as disguise

class CommonIndexCollector:
    # 一些通用的，用于收集指数某些属性的方法

    def __init__(self):
        pass

    def get_index_latest_increasement_decreasement_rate(self, index_code):
        # 获取指数最新的涨跌率
        # index_code: 指数代码, 必须如 399965.XSHE，代码后面带上市地
        # return: 最新的涨跌幅, 如 0.39% 即返回为 0.39
        location_index_code = ''
        if index_code[-5:] == '.XSHE':
            location_index_code = 'sz'+index_code[:6]
        elif index_code[-5:] == '.XSHG':
            location_index_code = 'sh' + index_code[:6]

        # 伪装，隐藏UA和IP
        ip_address, ua = disguise.Disguise().get_one_IP_UA()
        header = {"user-agent": ua['ua'], 'Connection': 'close'}
        proxy = {'http': 'https://' + ip_address['ip_address']}

        # 接口地址
        # 接口返回: 指数名称，当前点数，当前价格，涨跌率，成交量（手），成交额（万元）；
        # 接口返回如： var hq_str_s_sz399997="中证白酒,17305.78,66.408,0.39,1882235,1917906";
        # 只取 涨跌率
        url = 'https://hq.sinajs.cn/list=s_'+location_index_code
        content = requests.get(url, headers=header, proxies=proxy)
        content_split = content.text.split(',')
        #return float(content_split[3])
        return decimal.Decimal(content_split[3])

if __name__ == '__main__':
    time_start = time.time()
    go = CommonIndexCollector()
    result = go.get_index_latest_increasement_decreasement_rate('399997.XSHE')
    print(result)
    time_end = time.time()
    print('time:')
    print(time_end - time_start)