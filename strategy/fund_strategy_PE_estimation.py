import decimal
import time
import sys
import threading
sys.path.append("..")
import database.db_operator as db_operator
import data_collector.get_stock_real_time_indicator_from_xueqiu as xueqiu
import target_pool.read_collect_target_fund as read_collect_target_fund
import log.custom_logger as custom_logger
import data_miner.index_operator as index_operator


class FundStrategyPEEstimation:
    # 指数基金策略，市盈率估值法

    def __init__(self):
        pass

    def get_stock_historical_pe(self, stock_code, stock_name, day):
        # 提取股票的历史市盈率信息， 包括市盈率TTM, 扣非市盈率TTM
        # param: stock_code, 股票代码，如 000596
        # param: stock_name， 股票名称，如 古井贡酒
        # param: day, 日期， 如 2020-09-01
        # 返回：市盈率TTM, 扣非市盈率TTM
        # 例如 [{'pe_ttm': Decimal('61.6921425379745000'), 'pe_ttm_nonrecurring': Decimal('65.5556071829405200')}]
        selecting_sql = "select pe_ttm, pe_ttm_nonrecurring from stocks_main_estimation_indexes_historical_data " \
                        "where stock_code = '%s' and stock_name = '%s' and date = '%s' " % (stock_code, stock_name,day)
        pe_info = db_operator.DBOperator().select_all("financial_data", selecting_sql)
        return pe_info


    def calculate_a_historical_date_index_PE(self, index_code, day):
        # 基于当前指数构成，计算过去某一天该指数市盈率TTM, 扣非市盈率TTM
        # param: index_code 指数代码，如 399997
        # param: day, 日期， 如 2020-09-01
        # 返回 指数市盈率TTM, 扣非市盈率TTM, 均保留3位小数,
        # 例如，8.181 10.281
        pe_ttm = 0
        pe_ttm_nonrecurring = 0

        # 获取指数成分股及权重
        index_constitute_stocks_weight = index_operator.IndexOperator().get_index_constitute_stocks(index_code)
        for stock_info in index_constitute_stocks_weight:
            # 获取指数市盈率信息
            pe_info = self.get_stock_historical_pe(stock_info['stock_code'], stock_info['stock_name'], day)
            # 计算市盈率TTM, 扣非市盈率TTM
            pe_ttm += decimal.Decimal(pe_info[0]["pe_ttm"])*decimal.Decimal(stock_info["weight"])/100
            pe_ttm_nonrecurring += decimal.Decimal(pe_info[0]["pe_ttm_nonrecurring"])*decimal.Decimal(stock_info["weight"])/100
        return round(pe_ttm,3), round(pe_ttm_nonrecurring,3)

    def is_a_number(self, input_str):
        # 判断字符串是否为数字，int，float，负数（如：1，-32.34，-45, 34.65）
        # input_str: 输入的字符串
        # 为数字，输出 True; 不是数字，输出 False

        # 能成功转换为浮点型，则是数字
        try:
            float(input_str)
            return True
        except:
            return False

    def get_and_calculate_single_stock_pe_ttm_weight_in_index(self, stock_id, stock_weight, threadLock):
        # 获取并计算单个股票市盈率在指数中的权重
        # stock_id: 股票代码（2位上市地+6位数字， 如 sz000596）
        # stock_weight： 默认参数，在指数中，该成分股权重，默认为0
        # threadLock：线程锁

        # 通过抓取数据雪球页面，获取单个股票的实时滚动市盈率
        stock_real_time_pe_ttm = xueqiu.GetStockRealTimeIndicatorFromXueqiu().get_single_stock_real_time_indicator(stock_id, 'pe_ttm')
        # 如果获取的股票实时滚动市盈率不是数字，如’亏损‘
        if not self.is_a_number(stock_real_time_pe_ttm):
            # 股票实时滚动市盈率为200
            stock_real_time_pe_ttm = '200'

        # 获取锁，用于线程同步
        threadLock.acquire()
        print(stock_id)
        print(stock_real_time_pe_ttm)
        # 统计指数的实时市盈率，成分股权重*股票实时的市盈率
        self.index_real_time_pe_ttm += stock_weight * decimal.Decimal(stock_real_time_pe_ttm)
        # 释放锁，开启下一个线程
        threadLock.release()

    def calculate_real_time_index_pe_multiple_threads(self,index_code):
        # 多线程计算指数的实时市盈率
        # index_code, 指数代码（1、6位数字+交易所代码；2、6位数字；例如： 399997.XSHE 或者 399997）
        # 输出，指数的实时市盈率， 如 70.5937989

        # 统计指数实时的市盈率
        self.index_real_time_pe_ttm = 0

        # 获取指数的成分股和权重
        stocks_and_their_weights = index_operator.IndexOperator().get_index_constitute_stocks(index_code)

        # 启用多线程
        running_threads = []
        # 启用线程锁
        threadLock = threading.Lock()

        # 遍历指数的成分股
        for i in range(len(stocks_and_their_weights)):
            # 用于储存股票代码，例如 sh600726
            stock_id = ''

            # 获取成分股上市地，
            # XSHG 上海证券交易所
            # XSHE 深圳证券交易所
            stock_exchange = stocks_and_their_weights[i]["global_stock_code"][7:11]
            # 获取成分股代码，6位纯数字
            stock_code = stocks_and_their_weights[i]["global_stock_code"][:6]
            # 获取成分股权重
            stock_weight = stocks_and_their_weights[i]["weight"]

            # 将股票代码进行转换，
            # 由 6位数字+4位上市地（如 000596.XSHE） ---> 2位上市地+6位数字（如 sz000596）
            if stock_exchange == 'XSHG':
                stock_id = 'sh' + stock_code
            elif stock_exchange == 'XSHE':
                stock_id = 'sz' + stock_code

            # 启动线程
            running_thread = threading.Thread(target=self.get_and_calculate_single_stock_pe_ttm_weight_in_index,
                                              kwargs={"stock_id": stock_id, "stock_weight": stock_weight,
                                                      "threadLock": threadLock})
            running_threads.append(running_thread)

        # 开启新线程
        for mem in running_threads:
            mem.start()

        # 等待所有线程完成
        for mem in running_threads:
            mem.join()

        # 整体市盈率除以100，因为之前的权重没有除以100
        self.index_real_time_pe_ttm = self.index_real_time_pe_ttm / 100

        return self.index_real_time_pe_ttm

    def calculate_all_tracking_index_funds_real_time_PE_and_generate_msg(self):
        # 计算所有指数基金的实时市盈率TTM
        # return: 返回计算结果

        # 获取标的池中跟踪关注指数及他们的中文名称
        # 字典形式。如，{'399396.XSHE': '国证食品', '000932.XSHG': '中证主要消费',,,,}
        indexes_and_their_names = read_collect_target_fund.ReadCollectTargetFund().get_indexes_and_their_names()

        # 获取当前日期
        today = time.strftime("%Y-%m-%d", time.localtime())

        # 拼接需要发送的指数实时动态市盈率信息
        indexes_and_real_time_PE_msg = '指数实时动态市盈率信息： \n\n'
        for index in indexes_and_their_names:
            # 获取 实时市盈率TTM
            index_real_time_pe_ttm = self.calculate_real_time_index_pe_multiple_threads(index)
            indexes_and_real_time_PE_msg += indexes_and_their_names[index] + ": "+ str(index_real_time_pe_ttm) + "\n"
            # 日志记录
            log_msg = 'Just got the '+indexes_and_their_names[index] + ' real time PE TTM'
            custom_logger.CustomLogger().log_writter(log_msg, 'debug')
        return indexes_and_real_time_PE_msg



if __name__ == '__main__':
    time_start = time.time()
    go = FundStrategyPEEstimation()
    #result = go.get_index_constitute_stocks("399997")
    #print(result)
    #result = go.get_stock_historical_pe("000596", "古井贡酒", "2020-11-16")
    #print(result)
    #pe_ttm, pe_ttm_nonrecurring = go.calculate_a_historical_date_index_PE("399965","2020-10-19")
    #print(pe_ttm, pe_ttm_nonrecurring)
    #result = go.calculate_real_time_index_pe_multiple_threads("399997.XSHE")
    #print(result)
    msg = go.calculate_all_tracking_index_funds_real_time_PE_and_generate_msg()
    print(msg)
    time_end = time.time()
    print('time:')
    print(time_end - time_start)