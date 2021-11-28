import datetime

import requests
import time
import json

import sys

sys.path.append("..")
import parsers.disguise as disguise
import log.custom_logger as custom_logger
import database.db_operator as db_operator

class CollectCsi300IndexInfo:
    # 从东方财富网的接口获取沪深300指数的信息

    def __init__(self):
        pass


    def call_interface_to_get_CSI_300_info(self):
        # 调用接口，获取沪深300的指数内容

        # 东方财富网接口地址
        interface_address = 'https://datacenter-web.eastmoney.com/api/data/v1/get?callback=jQuery1123033240996308962667_1637913358385&sortColumns=WEIGHT&sortTypes=-1&pageSize=300&pageNumber=1&reportName=RPT_INDEX_TS_COMPONENT&columns=SECUCODE%2CSECURITY_CODE%2CTYPE%2CSECURITY_NAME_ABBR%2CCLOSE_PRICE%2CINDUSTRY%2CREGION%2CWEIGHT%2CEPS%2CBPS%2CROE%2CTOTAL_SHARES%2CFREE_SHARES%2CFREE_CAP&quoteColumns=f2%2Cf3&source=WEB&client=WEB&filter=(TYPE%3D%221%22)'

        # 伪装，隐藏UA和IP
        ip_address, ua = disguise.Disguise().get_one_IP_UA()
        header = {"user-agent": ua['ua'], 'Connection': 'close'}
        proxy = {'http': 'https://' + ip_address['ip_address']}

        # 增加连接重试次数,默认10次
        requests.adapters.DEFAULT_RETRIES = 10
        # 关闭多余的连接：requests使用了urllib3库，默认的http connection是keep-alive的，
        # requests设置False关闭
        s = requests.session()
        s.keep_alive = False

        # 忽略警告
        requests.packages.urllib3.disable_warnings()

        try:
            # 得到页面的信息
            raw_page = requests.get(interface_address, headers=header, proxies=proxy, verify=False, stream=False,
                                    timeout=10).text
            # 去除不必要信息，转换成符合json格式数据
            data_json = json.loads(raw_page[43:-2])
            # 去除data部分的内容
            data_list = data_json["result"]['data']
            return data_list

        except Exception as e:
            #日志记录
            msg = '调用东方财富网接口，获取沪深300的指数内容失败 ' + '  ' + str(e)
            msg += '  重新再调用东方财富网接口尝试获取沪深300的指数内容'
            custom_logger.CustomLogger().log_writter(msg, 'error')
            return []


    def parse_and_save(self,data_list):
        # 解析数据内容，并存入数据库

        # data_list，符合json格式的数据列表

        # 遍历
        for i in range(len(data_list)):
            # 股票全球代码
            stock_code_global = data_list[i]['SECUCODE']
            # 股票代码
            stock_code = data_list[i]['SECURITY_CODE']
            # 股票名称
            stock_name = data_list[i]['SECURITY_NAME_ABBR']
            # 股票权重
            stock_weight = data_list[i]['WEIGHT']
            # 股票上市地,转为小写
            stock_exchange_location = str.lower(data_list[i]['SECUCODE'][-2:])
            # 最新价格
            current_price = data_list[i]['CLOSE_PRICE']
            # 每股收益
            eps = data_list[i]['EPS']
            # 每股净资产
            bps = data_list[i]['BPS']
            # 净资产收益率
            roe = data_list[i]['ROE']
            # 总股本（亿股）
            total_shares = data_list[i]['TOTAL_SHARES']
            # 流通股本（亿股）
            free_shares = data_list[i]['FREE_SHARES']
            # 流通市值（亿元）
            free_cap = data_list[i]['FREE_CAP']
            # 所属行业
            industry = data_list[i]['INDUSTRY']
            # 地区
            region = data_list[i]['REGION']
            # 日期
            p_day =  datetime.date.today() - datetime.timedelta(days=1)

            try:
                # 插入的SQL
                inserting_sql = "INSERT INTO CSI_300_index_stocks (index_code_global,index_code,index_name," \
                                "stock_code_global,stock_code,stock_name,stock_weight,stock_exchange_location," \
                                "current_price,eps,bps,roe,total_shares,free_shares,free_cap,industry,region," \
                                "source,index_company,p_day)" \
                                "VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s'," \
                                "'%s','%s','%s','%s','%s')" % ('000300.XSHG','000300','沪深300',stock_code_global,
                                stock_code,stock_name,stock_weight,stock_exchange_location,current_price,eps,bps,roe,
                                total_shares,free_shares,free_cap,industry,region,'东方财富网','中证',p_day)
                db_operator.DBOperator().operate("insert", "financial_data", inserting_sql)

            except Exception as e:
                # 日志记录
                msg = '从东方财富网收集沪深300指数信息， 插入 ' + str(p_day) + ' 的数据 失败' + '  ' + str(e)
                custom_logger.CustomLogger().log_writter(msg, 'error')


    def main(self):
        data_list = self.call_interface_to_get_CSI_300_info()
        self.parse_and_save(data_list)



if __name__ == '__main__':

    time_start = time.time()
    go = CollectCsi300IndexInfo()
    go.main()
    time_end = time.time()
    print('Time Cost: ' + str(time_end - time_start))


