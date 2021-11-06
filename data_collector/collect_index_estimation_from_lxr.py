import datetime
from datetime import date

import requests
import json
import time
import os
import sys

sys.path.append("..")
import database.db_operator as db_operator
import config.lxr_token as lxr_token
import log.custom_logger as custom_logger

class CollectIndexEstimationFromLXR:
    # 从理杏仁收集指数估值信息
    # dyr ：股息率
    # pe_ttm：动态市盈率
    # pb ：市净率
    # ps_ttm ：动态市销率
    # # 运行频率：每个交易日收盘后

    def __init__(self):

        # 要从理杏仁采集估值的指数
        self.index_code_name_dict = {"000300":"沪深300", "1000002":"沪深A股"}


    def collect_index_estimation_in_a_period_time(self, index_code, start_date, end_date):
        # 调取理杏仁接口，获取一段时间范围内，指数估值数据, 并储存
        # param:  index_code, 指数代码，如 000300
        # param:  start_date, 开始时间，如 2020-11-12
        # param:  end_date, 结束时间，默认为空，如 2020-11-13
        # 输出： 将获取到指数估值数据存入数据库

        # 随机获取一个token
        token = lxr_token.LXRToken().get_token()
        # 理杏仁要求 在请求的headers里面设置Content-Type为application/json。
        headers = {'Content-Type': 'application/json'}
        # 理杏仁 获取A股指数基本面数据 接口，文档如下
        # https://www.lixinger.com/open/api/doc?api-key=a%2Findex%2Ffundamental
        url = 'https://open.lixinger.com/api/a/index/fundamental'

        # 接口参数，
        # dyr：股息率
        # pe_ttm ： 滚动市盈率
        # pb ： 市净率
        # ps_ttm ： 滚动市销率

        # 估值方式
        # mcw ： 市值加权 ， 以PE-TTM为例，所有样品公司市值之和 / 所有样品公司归属于母公司净利润之和
        # ew ： 等权， 以PE-TTM为例，算出所有公司的PE-TTM，然后通过(n / ∑(1 / PE.i))计算出来
        # ewpvo ： 等权， 当计算PE-TTM的时候，意味着剔除所有不赚钱的企业。
        #                当计算PB的时候，意味着剔除所有净资产为负数的企业（多见于ST或者快退市的企业，港股和美股有部分长期大比率分红而导致净资产为负数的企业）。
        #                当计算PS-TTM的时候，意味着剔除所有营业额为0的企业（可见于极少部分即将退市的企业，以及少部分港股的投资公司）。
        #                当计算股息率的时候，意味着剔除所有不分红的企业。
        # avg ： 平均值， 以PE-TTM为例，算出所有样品公司的滚动市盈率，剔除负数，然后使用四分位距（interquartile range, IQR）去除极端值，然后加和求平均值
        # median ： 中位数， 以PE-TTM为例，算出所有样品公司的市盈率，然后排序，然后取最中间的那个数；如果是偶数，那么取中间的两个，加和求半。

        parms = {"token": token,
                 "startDate": start_date,
                 "endDate": end_date,
                 "stockCodes":
                     [
                         index_code
                     ],
                 "metricsList": [
                    "pe_ttm.mcw",
                    "pe_ttm.ew",
                    "pe_ttm.ewpvo",
                    "pe_ttm.avg",
                    "pe_ttm.median",
                    "pb.mcw",
                    "pb.ew",
                    "pb.ewpvo",
                    "pb.avg",
                    "pb.median",
                    "ps_ttm.mcw",
                    "ps_ttm.ew",
                    "ps_ttm.ewpvo",
                    "ps_ttm.avg",
                    "ps_ttm.median",
                    "dyr.mcw",
                    "dyr.ew",
                    "dyr.ewpvo",
                    "dyr.avg",
                    "dyr.median"
                 ]}

        values = json.dumps(parms)
        # 调用理杏仁接口
        req = requests.post(url, data=values, headers=headers)
        content = req.json()

        if 'message' in content and content['message'] == "illegal token.":
            # 日志记录失败
            msg = '无法使用理杏仁token ' + token + ' ' + '来采集指数估值 ' + \
                  index_code+ '' +self.index_code_name_dict.get(index_code) + ' ' + start_date + ' ' + end_date
            custom_logger.CustomLogger().log_writter(msg, 'error')
            return self.collect_index_estimation_in_a_period_time(index_code, start_date, end_date)

    def collect_index_estimation_in_a_special_date(self, date):
        # 调取理杏仁接口，获取某一个具体日期，指数估值数据, 并储存
        # param:  index_code, 指数代码，如 000300
        # param:  date, 日期，如 2020-11-12
        # 输出： 将获取到指数估值数据存入数据库

        # 随机获取一个token
        token = lxr_token.LXRToken().get_token()
        # 理杏仁要求 在请求的headers里面设置Content-Type为application/json。
        headers = {'Content-Type': 'application/json'}
        # 理杏仁 获取A股指数基本面数据 接口，文档如下
        # https://www.lixinger.com/open/api/doc?api-key=a%2Findex%2Ffundamental
        url = 'https://open.lixinger.com/api/a/index/fundamental'

        # 接口参数，
        # dyr：股息率
        # pe_ttm ： 滚动市盈率
        # pb ： 市净率
        # ps_ttm ： 滚动市销率

        # 估值方式
        # mcw ： 市值加权 ， 以PE-TTM为例，所有样品公司市值之和 / 所有样品公司归属于母公司净利润之和
        # ew ： 等权， 以PE-TTM为例，算出所有公司的PE-TTM，然后通过(n / ∑(1 / PE.i))计算出来
        # ewpvo ： 等权， 当计算PE-TTM的时候，意味着剔除所有不赚钱的企业。
        #                当计算PB的时候，意味着剔除所有净资产为负数的企业（多见于ST或者快退市的企业，港股和美股有部分长期大比率分红而导致净资产为负数的企业）。
        #                当计算PS-TTM的时候，意味着剔除所有营业额为0的企业（可见于极少部分即将退市的企业，以及少部分港股的投资公司）。
        #                当计算股息率的时候，意味着剔除所有不分红的企业。
        # avg ： 平均值， 以PE-TTM为例，算出所有样品公司的滚动市盈率，剔除负数，然后使用四分位距（interquartile range, IQR）去除极端值，然后加和求平均值
        # median ： 中位数， 以PE-TTM为例，算出所有样品公司的市盈率，然后排序，然后取最中间的那个数；如果是偶数，那么取中间的两个，加和求半。

        # 取出指数代码
        index_code_list = list(self.index_code_name_dict.keys())

        parms = {"token": token,
                 "date": date,
                 "stockCodes":
                     index_code_list,
                 "metricsList": [
                     "pe_ttm.mcw",
                     "pe_ttm.ew",
                     "pe_ttm.ewpvo",
                     "pe_ttm.avg",
                     "pe_ttm.median",
                     "pb.mcw",
                     "pb.ew",
                     "pb.ewpvo",
                     "pb.avg",
                     "pb.median",
                     "ps_ttm.mcw",
                     "ps_ttm.ew",
                     "ps_ttm.ewpvo",
                     "ps_ttm.avg",
                     "ps_ttm.median",
                     "dyr.mcw",
                     "dyr.ew",
                     "dyr.ewpvo",
                     "dyr.avg",
                     "dyr.median"
                 ]}

        values = json.dumps(parms)
        # 调用理杏仁接口
        req = requests.post(url, data=values, headers=headers)
        content = req.json()
        print(content)

        if 'message' in content and content['message'] == "illegal token.":
            # 日志记录失败
            msg = '无法使用理杏仁token ' + token + ' ' + '来采集指数估值 ' + \
                  str(self.index_code_name_dict) + ' ' + date
            custom_logger.CustomLogger().log_writter(msg, 'error')
            return self.collect_index_estimation_in_a_special_date(date)


        '''
                try:
            # 数据存入数据库
            self.save_content_into_db(content, self.index_code_name_dict, "period")
        except Exception as e:
            # 日志记录失败
            msg = '数据存入数据库失败。 ' + '理杏仁接口返回为 '+str(content) + '。 抛错为 '+ str(e)
            custom_logger.CustomLogger().log_writter(msg, 'error')
        '''

if __name__ == '__main__':
    go = CollectIndexEstimationFromLXR()
    #go.collect_index_estimation_in_a_period_time("000300","2021-11-01","2021-11-05")
    go.collect_index_estimation_in_a_special_date("2021-11-05")