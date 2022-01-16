#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import requests
import json
import threading

import sys
sys.path.append("..")
import parsers.disguise as disguise
import log.custom_logger as custom_logger
import database.db_operator as db_operator

class CollectExcellentIndexFromCNIndex:
    # 从国证指数官网接口收集过去几年表现优异的指数

    def __init__(self):

        # 衡量标准
        # 3年年化收益率
        self.three_year_yield_rate_standard = 20
        # 5年年化收益率
        self.five_year_yield_rate_standard = 15
        # 最大线程数
        self.max_thread_num = 20


    def parse_interface_to_get_index_code_content(self, header, proxy):
        '''
        从国证接口获取全部指数的代码和名称
        :param header: 伪装的UA
        :param proxy: 伪装的IP
        :return: 指数代码的set
        如 {'000951', '000131', '000938', '930902', '931036', ，，，}
        '''

        # 指数代码
        index_code_set = set()

        # 接口地址
        interface_url = "http://www.cnindex.com.cn/index/indexList?channelCode=-1&rows=20000&pageNum=1"

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
            raw_page = requests.get(interface_url, headers=header, proxies=proxy, verify=False, stream=False,
                                    timeout=10).text

            # 转换成字典数据
            data_json = json.loads(raw_page)["data"]["rows"]

            for index_info in data_json:
                index_code_set.add(index_info["indexcode"])

            return index_code_set


        except Exception as e:
            # 日志记录
            msg = "从国证官网接口 " + interface_url + '  ' + "获取全部指数的代码失败 " + str(e) + " 即将重试"
            custom_logger.CustomLogger().log_writter(msg, lev='warning')
            # 返回解析页面得到的股票指标
            return self.call_interface_to_get_all_index_code_from_cn_index()

    def call_interface_to_get_all_index_code_from_cn_index(self):
        '''
        调用接口，从国证指数官网获取全部指数代码和名称
        return: 数代码的set
        '''

        # 伪装，隐藏UA和IP
        ip_address, ua = disguise.Disguise().get_one_IP_UA()
        header = {"user-agent": ua['ua'], 'Connection': 'close'}
        proxy = {'https': 'https://' + ip_address['ip_address']}

        return self.parse_interface_to_get_index_code_content(header, proxy)


    def parse_interface_to_get_index_relative_funds(self, index_code, header, proxy):
        '''
        从中证接口获取指数的相关基金代码和名称
        :param index_code: 指数代码（6位数字， 如 399997）
        :param header: 伪装的UA
        :param proxy: 伪装的IP
        :return: 指数相关基金的信息
        如 [{'512190': '浙商汇金中证凤凰50ETF'}, {'007431': '浙商汇金中证凤凰50ETF联接'}]
        '''
        # 地址模板
        interface_url = "http://www.cnindex.com.cn/info/fund?indexCode="+index_code+"&pageNum=1&rows=200"
        # 相关基金的列表
        relative_funds_list = []

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
            raw_page = requests.get(interface_url, headers=header, proxies=proxy, verify=False, stream=False,
                                    timeout=10).text
            # 转换成字典数据
            raw_data = json.loads(raw_page)

            # 判断接口是否调用成功
            if (raw_data["code"] != 200):
                return

            # 获取data数据
            data_json = raw_data["data"]["rows"]
            if (data_json == None or len(data_json)==0):
                return

            # 遍历获取到的接口数据
            for fund_info in data_json:
                fund_dict = dict()
                fund_code = fund_info["fundCode"]
                fund_name = fund_info["fundName"]
                fund_dict[fund_code] = fund_name
                relative_funds_list.append(fund_dict)

            # 返回 如， [{'512190': '浙商汇金中证凤凰50ETF'}, {'007431': '浙商汇金中证凤凰50ETF联接'}]
            return relative_funds_list

        except Exception as e:
            # 日志记录
            msg = "从国证官网接口 " + interface_url + '  ' + "获取相关基金产品失败 " + str(e) + " 即将重试"
            custom_logger.CustomLogger().log_writter(msg, lev='warning')
            # 返回解析页面得到的股票指标
            return self.get_satisfied_index_relative_funds(index_code)


    def get_satisfied_index_relative_funds(self, index_code):
        '''
        获取满足指标的指数的相关基金
        :param index_code: 指数代码（6位数字， 如 399997）
        :return:
        '''

        # 伪装，隐藏UA和IP
        ip_address, ua = disguise.Disguise().get_one_IP_UA()
        header = {"user-agent": ua['ua'], 'Connection': 'close'}
        proxy = {'https': 'https://' + ip_address['ip_address']}

        return self.parse_interface_to_get_index_relative_funds(index_code, header, proxy)



if __name__ == '__main__':
    go = CollectExcellentIndexFromCNIndex()
    result = go.get_satisfied_index_relative_funds("399001")
    #result = go.call_interface_to_get_all_index_code_from_cn_index()
    print(result)