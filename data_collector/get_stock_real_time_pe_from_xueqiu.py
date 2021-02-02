# coding:utf-8
# !user/bin/env python

from bs4 import BeautifulSoup
import requests
import time

import sys

sys.path.append("..")
import parsers.disguise as disguise
import log.custom_logger as custom_logger


class GetStockRealTimePEFromXueqiu:
    # 获取雪球上股票估值数据
    # 1、获取实时的股票滚动市盈率

    def __init__(self):
        pass

    def parse_page_content(self, page_address, header, proxy):
        # 解析雪球网页信息
        # page_address，地址
        # header，伪装的UA
        # proxy，伪装的IP
        # 返回 股票滚动市盈率

        # 递归算法，处理异常
        try:
            # 增加连接重试次数,默认10次
            requests.adapters.DEFAULT_RETRIES = 10
            # 关闭多余的连接：requests使用了urllib3库，默认的http connection是keep-alive的，
            # requests设置False关闭
            s = requests.session()
            s.keep_alive = False

            # 忽略警告
            requests.packages.urllib3.disable_warnings()
            # 得到页面的信息
            raw_page = requests.get(page_address, headers=header, proxies=proxy, verify=False, stream=False,
                                    timeout=10).text

            # 使用BeautifulSoup解析页面
            bs = BeautifulSoup(raw_page, "html.parser")

            # 解析网页信息，获取动态市盈率
            real_time_stock_info = bs.find('tr', attrs={'class': 'separateBottom'})
            tdlist = real_time_stock_info.find_all('td')
            real_time_pe_ttm = tdlist[3].find('span').get_text()

            # 日志记录
            msg = "Collected stock real time PE from " + page_address
            custom_logger.CustomLogger().log_writter(msg, lev='debug')

            # 返回 股票滚动市盈率
            return real_time_pe_ttm


        # 如果读取超时，重新在执行一遍解析页面
        except requests.exceptions.ReadTimeout:
            # 日志记录
            msg = "Collected stock real time PE from " +page_address + '  ' + "ReadTimeout"
            custom_logger.CustomLogger().log_writter(msg, lev='warning')
            # 返回解析页面得到的股票滚动市盈率
            return self.parse_page_content(page_address, header, proxy)

        # 如果连接请求超时，重新在执行一遍解析页面
        except requests.exceptions.ConnectTimeout:
            # 日志记录
            msg = "Collected stock real time PE from " +page_address + '  ' + "ConnectTimeout"
            custom_logger.CustomLogger().log_writter(msg, lev='warning')
            # 返回解析页面得到的股票滚动市盈率
            return self.parse_page_content(page_address, header, proxy)

        # 如果请求超时，重新在执行一遍解析页面
        except requests.exceptions.Timeout:
            # 日志记录
            msg = "Collected stock real time PE from " +page_address + '  ' + "Timeout"
            custom_logger.CustomLogger().log_writter(msg, lev='warning')
            # 返回解析页面得到的股票滚动市盈率
            return self.parse_page_content(page_address, header, proxy)

        except Exception as e:
            # 日志记录
            msg = str(e)
            custom_logger.CustomLogger().log_writter(msg, lev='warning')

    def get_single_stock_real_time_pe_ttm(self, stock_id):
        # 从雪球网获取实时的股票滚动市盈率pe_ttm
        # stock_id: 股票代码（2位上市地+6位数字， 如 sz000596）
        # 返回： 获取的实时的股票滚动市盈率 格式如 32.74

        # 地址模板
        page_address = 'https://xueqiu.com/S/' + stock_id
        # 伪装，隐藏UA和IP
        ip_address, ua = disguise.Disguise().get_one_IP_UA()
        header = {"user-agent": ua['ua'], 'Connection': 'close'}
        proxy = {'http': 'http://' + ip_address['ip_address']}

        return self.parse_page_content(page_address, header, proxy)


if __name__ == '__main__':

    time_start = time.time()
    go = GetStockRealTimePEFromXueqiu()
    real_time_pe_ttm = go.get_single_stock_real_time_pe_ttm('SH600519')
    print(real_time_pe_ttm)
    '''
    for i in range(1000):
        real_time_pe_ttm = go.get_single_stock_real_time_pe_ttm('SH600519')
        print(real_time_pe_ttm)
        real_time_pe_ttm = go.get_single_stock_real_time_pe_ttm('SZ002505')
        print(real_time_pe_ttm)
        print()
    '''
    time_end = time.time()
    print('Time Cost: ' + str(time_end - time_start))