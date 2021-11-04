import requests
import time
import json

import sys
sys.path.append("..")
import parsers.disguise as disguise
import log.custom_logger as custom_logger
import database.db_operator as db_operator

class CollectCHNGovBondsRates:
    # 从中国债券信息网收集 中国债券到期收益率

    def __init__(self):
        pass

    def millisecond_to_time(self, millis):
        """13位时间戳转换为日期格式字符串"""
        # millis, 13位时间戳
        return time.strftime('%Y-%m-%d', time.localtime(millis / 1000))

    def call_bonds_interface_to_collect_all_historical_data(self):
        # 调用中国债券信息网接口

        # header，伪装的UA
        # proxy，伪装的IP
        # startDay, 开始日期， 如 2021-11-01
        # endDay, 结束日期， 如 2021-11-04（startDay和endDay不可相同）

        bonds_interface_address = "https://yield.chinabond.com.cn/cbweb-mn/yc/queryYz?bjlx=no&&dcq=0.083333,1m;0.166667,2m;0.25,3m;0.5,6m;0.75,9m;1,1y;2,2y;3,3y;5,5y;7,7y;10,10y;&&startTime=2021-10-01&&endTime=2021-11-04&&qxlx=0,&&yqqxN=N&&yqqxK=K&&par=day&&ycDefIds=2c9081e50a2f9606010a3068cae70001,&&locale=zh_CN"

        # 解决报错 InsecureRequestWarning: Unverified HTTPS request is being made
        requests.packages.urllib3.disable_warnings()

        # 获取当前时间
        today = time.strftime("%Y-%m-%d", time.localtime())

        # 伪装，隐藏UA和IP
        ip_address, ua = disguise.Disguise().get_one_IP_UA()
        header = {"user-agent": ua['ua'], 'Connection': 'close'}
        proxy = {'http': 'http://' + ip_address['ip_address']}

        # 得到页面的信息
        raw_page = requests.post(bonds_interface_address, headers=header, proxies=proxy, verify=False, stream=False,
                                timeout=10).text
        # 转换成字典数据
        # [{"ycDefId":"2c9081e50a2f9606010a3068cae700015.0","ycDefName":"中债国债收益率曲线(到期)(5y)","ycYWName":null,"worktime":"","seriesData":[[1635868800000,2.7986],[1635955200000,2.7759]],"isPoint":false,"hyCurve":false,"point":false},{"ycDefId":"2c9081e50a2f9606010a3068cae7000110.0","ycDefName":"中债国债收益率曲线(到期)(10y)","ycYWName":null,"worktime":"","seriesData":[[1635868800000,2.9385],[1635955200000,2.9261]],"isPoint":false,"hyCurve":false,"point":false},{"ycDefId":"yzdcqx","ycDefName":"点差曲线","ycYWName":null,"worktime":null,"seriesData":[[1635868800000,0.1399],[1635955200000,0.1502]],"isPoint":false,"hyCurve":false,"point":false}]
        data_json_list = json.loads(raw_page)

        # 遍历 国债各时间到期信息
        for i in range(len(data_json_list)):
            # 每组信息如下
            # {"ycDefId":"2c9081e50a2f9606010a3068cae700010.083333","ycDefName":"中债国债收益率曲线(到期)(1m)","ycYWName":null,"worktime":"","seriesData":[[1633622400000,1.776],[1633708800000,1.7659],,,],"isPoint":false,"hyCurve":false,"point":false}

            # 第一组到期信息，需要插入数据库
            if i == 0:
                for j in data_json_list[i]["seriesData"]:
                    # 时间和利率信息如下
                    # [[1633622400000,1.776],[1633708800000,1.7659],,,]
                    p_day = self.millisecond_to_time(j[0])
                    rate = j[1]

                    try:
                        # 插入的SQL
                        inserting_sql = "INSERT INTO chn_gov_bonds_rates_di(1m,p_day,submission_date)" \
                                        "VALUES ('%s','%s','%s')" % (
                                        rate,p_day,today)
                        db_operator.DBOperator().operate("insert", "financial_data", inserting_sql)

                    except Exception as e:
                        # 日志记录
                        msg = '收集国债到期收益率(1月期)失败' + '  ' + str(e)
                        custom_logger.CustomLogger().log_writter(msg, 'error')

            # 其它组到期信息，需要更新数据库
            else:
                for j in data_json_list[i]["seriesData"]:
                    # 时间和利率信息如下
                    # [[1633622400000,1.776],[1633708800000,1.7659],,,]
                    p_day = self.millisecond_to_time(j[0])
                    rate = j[1]
                    try:
                        # 插入的SQL
                        # todo i=1, 插入2m; i=2, 插入3m; i=3, 插入6m;
                        inserting_sql = "UPDATE chn_gov_bonds_rates_di SET(1m,p_day,submission_date)" \
                                        "VALUES ('%s','%s','%s')" % (
                                        rate,p_day,today)
                        db_operator.DBOperator().operate("update", "financial_data", inserting_sql)

                    except Exception as e:
                        # 日志记录
                        msg = '收集国债到期收益率(1月期)失败' + '  ' + str(e)
                        custom_logger.CustomLogger().log_writter(msg, 'error')



if __name__ == '__main__':
    time_start = time.time()
    go = CollectCHNGovBondsRates()
    go.call_bonds_interface_to_collect_all_historical_data()
    time_end = time.time()
    print('Time Cost: ' + str(time_end - time_start))