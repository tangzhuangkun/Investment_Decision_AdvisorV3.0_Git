#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
import time
import json

import sys

sys.path.append("..")
import parsers.disguise as disguise
import log.custom_logger as custom_logger
import data_miner.data_miner_common_target_index_operator as target_index_operator
import database.db_operator as db_operator
import data_collector.collector_tool_to_distinguish_stock_market as collector_tool_to_distinguish_stock_market



class CollectIndexWeightFromCNIndexInterface:
    # 从国证指数官网获取指数成分股及其权重

    def __init__(self):
        pass

    def call_interface_to_get_index_weight(self, index_id, current_month, header, proxy):
        # 调用国证指数公司接口获取指数成分股及权重
        # index_id: 指数代码（6位数字， 如 399396）
        # current_month，所查月份，如 2021-12
        # header，伪装的UA
        # proxy，伪装的IP
        # 返回 tuple (截止日期, [成份股代码，名称，上市地，交易所代码，权重])
        # 如 ( '2021-09-24', [['600519', '贵州茅台','sh','XSHG',15.19'], ['600887', '伊利股份','sh','XSHG',10.37'], ,,,,])

        # 地址模板
        page_address = 'http://www.cnindex.com.cn/sample-detail/detail?indexcode='+index_id+'&dateStr='+current_month+'&pageNum=1&rows=1000'

        # 返回成份股信息，成份股代码，名称，权重
        # [['600519', '贵州茅台','sh','XSHG',15.19'], ['600887', '伊利股份','sh','XSHG',10.37'], ,,,,]
        stocks_detail_info_list = []

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
            # 转换成字典数据
            data_json = json.loads(raw_page)
            # 获取更新日期
            update_date = data_json['data']['rows'][1]['dateStr']
            # 遍历成分股权重列表
            for stock_info in data_json['data']['rows']:
                # 单个成份股的关键信息，如 ['600519', '贵州茅台','sh','XSHG',15.19']
                stock_detail_info_list = []
                # 获取股票代码
                stock_detail_info_list.append(stock_info['seccode'])
                # 将名称中间的空格替换
                stock_detail_info_list.append(stock_info['secname'].replace(' ',''))
                # 通过股票代码获取，上市地，股票交易所代码, 返回如 sh, XSHG
                market_init, market_code = collector_tool_to_distinguish_stock_market.CollectorToolToDistinguishStockMarket().distinguishStockMarketByCode(stock_info['seccode'])
                stock_detail_info_list.append(market_init)
                stock_detail_info_list.append(market_code)
                # 权重
                stock_detail_info_list.append(stock_info['weight'])
                stocks_detail_info_list.append(stock_detail_info_list)
            # 返回如 ('2021-12-13', [['600519', '贵州茅台', 'sh', 'XSHG', 15.19], ['000858', '五粮液', 'sz', 'XSHE', 15.18],,,,,])
            return update_date, stocks_detail_info_list


        # 如果读取超时，重新在执行一遍解析页面
        except requests.exceptions.ReadTimeout:
            # 日志记录
            msg = "从国证指数官网" + page_address + '  ' + "获取最新成份股权重信息 " + " ReadTimeout。" + " 即将重试"
            custom_logger.CustomLogger().log_writter(msg, lev='warning')
            # 返回解析页面得到的股票指标
            return self.get_single_index_latest_constituent_stock_and_weight(index_id)

        # 如果连接请求超时，重新在执行一遍解析页面
        except requests.exceptions.ConnectTimeout:
            # 日志记录
            msg = "从国证指数官网" + page_address + '  ' + "获取最新成份股权重信息 " + " ConnectTimeout。" + " 即将重试"
            custom_logger.CustomLogger().log_writter(msg, lev='warning')
            # 返回解析页面得到的股票指标
            return self.get_single_index_latest_constituent_stock_and_weight(index_id)

        # 如果请求超时，重新在执行一遍解析页面
        except requests.exceptions.Timeout:
            # 日志记录
            msg = "从国证指数官网" + page_address + '  ' + "获取最新成份股权重信息 " + " Timeout。" + " 即将重试"
            custom_logger.CustomLogger().log_writter(msg, lev='warning')
            # 返回解析页面得到的股票指标
            return self.get_single_index_latest_constituent_stock_and_weight(index_id)

        except Exception as e:
            # 日志记录
            msg = "从国证指数官网" + page_address + '  ' + "获取最新成份股权重信息 " + str(e)+ " 即将重试"
            custom_logger.CustomLogger().log_writter(msg, lev='warning')
            # 返回解析页面得到的股票指标
            return self.get_single_index_latest_constituent_stock_and_weight(index_id)

    def get_single_index_latest_constituent_stock_and_weight(self, index_id):
        # 从国证官网获取单个指数最新成份股和权重信息
        # index_id: 指数代码（6位数字， 如 399396）
        # 返回 tuple (截止日期, [成份股代码，名称，上市地，交易所代码，权重])
        # 如 ( '2021-09-24', [['600519', '贵州茅台','sh','XSHG',15.19'], ['600887', '伊利股份','sh','XSHG',10.37'], ,,,,])

        # 伪装，隐藏UA和IP
        ip_address, ua = disguise.Disguise().get_one_IP_UA()
        header = {"user-agent": ua['ua'], 'Connection': 'close'}
        proxy = {'https': 'https://' + ip_address['ip_address']}
        current_month = time.strftime("%Y-%m", time.localtime())

        return self.call_interface_to_get_index_weight(index_id, current_month, header, proxy)

    def get_cn_index_from_index_target(self):
        # 从标的池中获取国证公司的指数
        # 返回：指数代码及对应的指数名称的字典
        # 如 {'399396': '国证食品饮料行业', '399440': '国证钢铁',,,}

        # 存放指数代码及对应的指数名称的字典
        target_cn_index_dict = dict()

        #[{'index_code': '399396', 'index_name': '国证食品饮料行业', 'index_code_with_init': 'sz399396', 'index_code_with_market_code': '399396.XSHE'},,,]
        target_cs_index_info_list =  target_index_operator.DataMinerCommonTargetIndexOperator().get_given_index_company_index("国证")
        for info in target_cs_index_info_list:
            target_cn_index_dict[info["index_code"]] = info["index_name"]
        return target_cn_index_dict


if __name__ == '__main__':
    time_start = time.time()
    go = CollectIndexWeightFromCNIndexInterface()
    go.collect_all_target_cn_index_weight_single_thread()
    #result = go.collect_all_target_cn_index_weight_single_thread()
    #print(result)
    time_end = time.time()
    print('Time Cost: ' + str(time_end - time_start))