from bs4 import BeautifulSoup
import requests
import time

import sys

sys.path.append("..")
import parsers.disguise as disguise
import log.custom_logger as custom_logger
import target_pool.read_collect_target_fund as read_collect_target_fund
import database.db_operator as db_operator


class CollectCSIndexTop10StocksWeightDaily:
    # 从中证指数官网获取指数的权重数据，并存入数据库
    # 运行频率：每天

    def __init__(self):
        pass

    def parse_page_content(self, index_id, header, proxy):
        # 解析中证官网页信息
        # index_id: 指数代码（6位数字， 如 399997）
        # page_address，地址
        # header，伪装的UA
        # proxy，伪装的IP
        # 返回 tuple (截止日期, [前十成份股代码，名称，权重])
        # 如 ( '2021-09-24', [['600809', '山西汾酒', '17.95'], ['600519', '贵州茅台', '14.83'],,,,,])

        # 地址模板
        page_address = 'http://www.csindex.com.cn/zh-CN/indices/index-detail/' + index_id

        # 返回的前十成份股信息，成份股代码，名称，权重
        # [['600809', '山西汾酒', '17.95'], ['600519', '贵州茅台', '14.83'], ,,,,]
        top_10_stocks_detail_info_list = []

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

            # 解析网页信息，获取截止日期
            expiration_date_potential = bs.find_all("h2",attrs={'class': 't_3 mb-10 pr'})
            expiration_date = expiration_date_potential[2].find("p").get_text()[5:]

            # 解析网页信息，获取十大权重股信息
            top_10_stocks_table = bs.find('table', attrs={'class': 'table table-even table-bg p_table tc'})
            top_10_stocks_body = top_10_stocks_table.find('tbody')
            for stock_info in top_10_stocks_body.find_all('tr'):
                # 单个成份股的关键信息，如 ['600519', '贵州茅台', '14.83']
                stock_detail_info_list = []
                stock_info_iterator = iter(stock_info.find_all('td'))
                stock_detail_info_list.append(next(stock_info_iterator).get_text())
                stock_detail_info_list.append(next(stock_info_iterator).get_text())
                next(stock_info_iterator)
                stock_detail_info_list.append(next(stock_info_iterator).get_text())
                top_10_stocks_detail_info_list.append(stock_detail_info_list)

            # 日志记录
            # msg = "从中证官网 " + page_address + '  ' + "获取了 " + expiration_date + "的前十成份股信息"
            # custom_logger.CustomLogger().log_writter(msg, lev='info')

            # 返回如 ( '2021-09-24', [['600809', '山西汾酒', '17.95'], ['600519', '贵州茅台', '14.83'],,,,,])
            return  expiration_date, top_10_stocks_detail_info_list
        
        # 如果读取超时，重新在执行一遍解析页面
        except requests.exceptions.ReadTimeout:
            # 日志记录
            msg = "从中证官网" + page_address + '  ' + "获取前十成份股信息 "+" ReadTimeout。" + " 即将重试"
            custom_logger.CustomLogger().log_writter(msg, lev='warning')
            # 返回解析页面得到的股票指标
            return self.get_single_index_latest_constituent_stock_and_weight(index_id)

        # 如果连接请求超时，重新在执行一遍解析页面
        except requests.exceptions.ConnectTimeout:
            # 日志记录
            msg = "从中证官网" + page_address + '  ' + "获取前十成份股信息 " + " ConnectTimeout。" + " 即将重试"
            custom_logger.CustomLogger().log_writter(msg, lev='warning')
            # 返回解析页面得到的股票指标
            return self.get_single_index_latest_constituent_stock_and_weight(index_id)

        # 如果请求超时，重新在执行一遍解析页面
        except requests.exceptions.Timeout:
            # 日志记录
            msg = "从中证官网" + page_address + '  ' + "获取前十成份股信息 " + " Timeout。" + " 即将重试"
            custom_logger.CustomLogger().log_writter(msg, lev='warning')
            # 返回解析页面得到的股票指标
            return self.get_single_index_latest_constituent_stock_and_weight(index_id)

        except Exception as e:
            # 日志记录
            msg = "从中证官网" + page_address + '  ' + "获取前十成份股信息时 " + str(e)
            custom_logger.CustomLogger().log_writter(msg, lev='warning')
            # 返回解析页面得到的股票指标
            return self.get_single_index_latest_constituent_stock_and_weight(index_id)


    def get_single_index_latest_constituent_stock_and_weight(self, index_id):
        # 从中证官网获取单个指数最新的前十成份股和权重信息
        # index_id: 指数代码（6位数字， 如 399997）
        # 返回 tuple (截止日期, [前十成份股代码，名称，权重])
        # 如 ( '2021-09-24', [['600809', '山西汾酒', '17.95'], ['600519', '贵州茅台', '14.83'],,,,,])

        # 伪装，隐藏UA和IP
        ip_address, ua = disguise.Disguise().get_one_IP_UA()
        header = {"user-agent": ua['ua'], 'Connection': 'close'}
        proxy = {'https': 'https://' + ip_address['ip_address']}

        return self.parse_page_content(index_id, header, proxy)

    def collect_target_index_stock_info(self):
        # 收集目标池中的中证指数每日前十大权重股构成,并存入数据库

        # 获取标的池中关于 中证公司的 指数代码及指数名称
        cs_target_indexes_names_dict = read_collect_target_fund.ReadCollectTargetFund().get_given_index_company_index("中证")
        # 遍历这些指数
        for target_index_code in cs_target_indexes_names_dict:
            # 获取 该指数的最新更新日期及前十成份股信息
            stocks_info = self.get_single_index_latest_constituent_stock_and_weight(target_index_code[:6])
            # 截止日期
            expiration_date = stocks_info[0]
            # 指数代码，如 399997
            index_code = target_index_code[:6]
            # 指数名称，如 中证白酒
            index_name = cs_target_indexes_names_dict[target_index_code]
            for stock_info in stocks_info[1]:
                # 股票代码，如 600887
                stock_code = stock_info[0]
                # 股票名称，如 伊利股份
                stock_name = stock_info[1]
                # 权重，如 11.19
                weight = stock_info[2]
                try:
                    # 插入的SQL
                    inserting_sql = "INSERT INTO index_constituent_stocks_weight(index_code,index_name,stock_code,stock_name,weight,source,submission_date)" \
                                    "VALUES ('%s','%s','%s','%s','%s','%s','%s')" % (index_code, index_name, stock_code, stock_name,weight, '中证',expiration_date)
                    db_operator.DBOperator().operate("insert", "financial_data", inserting_sql)

                except Exception as e:
                    # 日志记录
                    msg = 'Failed to insert index weights into DB' + '  ' + str(e)
                    custom_logger.CustomLogger().log_writter(msg, 'error')



if __name__ == '__main__':

    time_start = time.time()
    go = CollectCSIndexTop10StocksWeightDaily()
    #real_time_pe_ttm = go.get_single_index_latest_constituent_stock_and_weight('399997')
    #print(real_time_pe_ttm)
    go.collect_target_index_stock_info()
    time_end = time.time()
    print('Time Cost: ' + str(time_end - time_start))