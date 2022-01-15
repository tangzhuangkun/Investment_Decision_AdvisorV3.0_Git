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

class CollectExcellentIndexFromCSIndex:
    # 从中证指数官网接口获取过去几年表现优异的指数

    def __init__(self):

        # 衡量标准
        # 3年年化收益率
        self.three_year_rate_standard = 20
        # 5年年化收益率
        self.five_year_rate_standard = 18



    def parse_interface_to_get_index_code_name_content(self, header, proxy):
        '''
        从中证接口获取全部指数的代码和名称
        :param header: 伪装的UA
        :param proxy: 伪装的IP
        :return: 指数代码的set
        如 {'000951', '000131', '000938', '930902', '931036', ，，，}
        '''

        # 指数代码
        index_code_set = set()

        # 接口地址
        interface_url = "https://www.csindex.com.cn/csindex-home/index-list/query-index-item"
        # 处理python中无null的问题
        null = None
        # 传入的参数
        body = {"sorter": {"sortField": "null", "sortOrder": null},
                "pager": {"pageNum": 1, "pageSize": 10000},
                "indexFilter": {"ifCustomized": null, "ifTracked": null, "ifWeightCapped": null,
                                "indexCompliance": null,
                                "hotSpot": null, "indexClassify": null, "currency": null, "region": null,
                                "indexSeries": null,
                                "undefined": null}
                }

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
            raw_page = requests.post(interface_url, headers=header, proxies=proxy, verify=False, stream=False,json=body,
                                    timeout=10).text
            # 转换成字典数据
            data_json = json.loads(raw_page)["data"]

            # 存入字典中
            for index_info in data_json:
                index_code_set.add(index_info["indexCode"])

        except Exception as e:
            # 日志记录
            msg = "从中证官网接口 " + interface_url + '  ' + "获取全部指数的代码和名称失败 " + str(e) + " 即将重试"
            custom_logger.CustomLogger().log_writter(msg, lev='warning')
            # 返回解析页面得到的股票指标
            return self.call_interface_to_get_all_index_code_name_from_cs_index()

        return index_code_set


    def call_interface_to_get_all_index_code_name_from_cs_index(self):
        '''
        调用接口，从中证指数官网获取全部指数代码和名称
        return: 数代码的set
        '''

        # 伪装，隐藏UA和IP
        ip_address, ua = disguise.Disguise().get_one_IP_UA()
        header = {"user-agent": ua['ua'], 'Connection': 'close'}
        proxy = {'http': 'https://' + ip_address['ip_address']}

        return self.parse_interface_to_get_index_code_name_content(header, proxy)





    def parse_and_check_whether_an_excellent_index(self,index_code, satisfied_index_list, threadLock, header, proxy):
        '''
        解析判断是否为
        解析接口内容，获取单个指数过去几年的表现
        :param index_code: 指数代码（6位数字， 如 399997）
        :param satisfied_index_list: 满足收集指标的指数
        :param threadLock: 线程锁
        :param header: 伪装的UA
        :param proxy: 伪装的IP
        :return:
        '''

        interface_url = "https://www.csindex.com.cn/csindex-home/perf/get-index-yield-item/"+index_code

        # 指数近3，5年表现的字典
        index_performance_dict = dict()

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
            if (not raw_data["success"]):
                return

            # 获取data数据
            data_json = raw_data["data"]
            if(data_json==None):
                return

            index_name = data_json["indexNameCn"]

            index_performance_dict["index_code"] = index_code
            index_performance_dict["index_name"] = index_name

            three_year_rate = 0
            five_year_rate = 0

            if (data_json["threeYear"] != None):
                three_year_rate = float(data_json["threeYear"])
                index_performance_dict["three_year_rate"] = three_year_rate
            if (data_json["fiveYear"] != None):
                five_year_rate = float(data_json["fiveYear"])
                index_performance_dict["five_year_rate"] = five_year_rate

            if (three_year_rate > self.three_year_rate_standard or five_year_rate > self.five_year_rate_standard):
                # 获取锁，用于线程同步
                threadLock.acquire()
                satisfied_index_list.append(index_performance_dict)
                # 释放锁，开启下一个线程
                threadLock.release()

        except Exception as e:
            # 日志记录
            msg = "从中证官网接口" + interface_url + '  ' + "获取指数过去表现 " + str(e)+ " 即将重试"
            custom_logger.CustomLogger().log_writter(msg, lev='warning')
            # 返回解析页面得到的股票指标
            return self.call_interface_to_get_single_index_past_performance(index_code)

    def call_interface_to_get_single_index_past_performance(self, index_code, satisfied_index_list, threadLock):

        '''
        调用接口获取指数过去几年的表现
        :param index_code: 指数代码（6位数字， 如 399997）
        :param satisfied_index_list: 满足收集指标的指数
        :param threadLock: 线程锁
        :return:
        '''

        # 伪装，隐藏UA和IP
        ip_address, ua = disguise.Disguise().get_one_IP_UA()
        header = {"user-agent": ua['ua'], 'Connection': 'close'}
        proxy = {'http': 'https://' + ip_address['ip_address']}

        return self.parse_and_check_whether_an_excellent_index(index_code, satisfied_index_list, threadLock, header, proxy)

    def check_all_index_and_get_all_excellent_index(self):

        # 获取所有指数的代码
        index_code_set = self.call_interface_to_get_all_index_code_name_from_cs_index()
        # 满足条件的指数
        satisfied_index_list = []

        # 启用多线程
        running_threads_list = []
        # 启用线程锁
        threadLock = threading.Lock()

        for index_code in index_code_set:
            # 启动线程
            running_thread = threading.Thread(target=self.call_interface_to_get_single_index_past_performance,
                                              kwargs={"index_code": index_code,
                                                      "satisfied_index_list": satisfied_index_list,
                                                      "threadLock": threadLock
                                                      })
            running_threads_list.append(running_thread)

            # 开启新线程
        for mem in running_threads_list:
            mem.start()

            # 等待所有线程完成
        for mem in running_threads_list:
            mem.join()

        return satisfied_index_list


if __name__ == '__main__':
    time_start = time.time()
    go = CollectExcellentIndexFromCSIndex()
    #result = go.call_interface_to_get_all_index_code_name_from_cs_index()
    #result = go.call_interface_to_get_single_index_past_performance("399997")
    #print(result)
    result = go.check_all_index_and_get_all_excellent_index()
    print(result)
    #go.call_interface_to_get_single_index_past_performance("H50059")
    time_end = time.time()
    print('Time Cost: ' + str(time_end - time_start))