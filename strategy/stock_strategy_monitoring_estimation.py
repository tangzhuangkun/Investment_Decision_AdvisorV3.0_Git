import time
import threading

import sys
sys.path.append("..")
import database.db_operator as db_operator
import log.custom_logger as custom_logger
import target_pool.read_collect_target_stock as read_collect_target_stock
import data_collector.get_stock_real_time_indicator_from_xueqiu as get_stock_real_time_indicator_from_xueqiu


class StockStrategyMonitoringEstimation:
    # 股票的监控策略，当触发条件时，返回信息并通知

    def __init__(self):
        pass


    def get_tracking_stocks_realtime_indicators_single_thread(self):
        # 获取所有跟踪股票的实时指标, 单线程
        # 返回 所有触发了条件的股票及信息的字典
        # 如 {'000002': [('sz000002', '万科A', 'pb', '0.98', '小于设定估值 0.99'), ('sz000002', '万科A', 'pe_ttm', '5.84', '3.39% 小于设定估值百分位 12%')], '600048': [('sh600048', '保利发展', 'pb', '1.07', '小于设定估值 1.1')]}

        # 获取标的池中跟踪关注股票及他们的中文名称
        # {'000002': ('sz000002', '万科A'), '600048': ('sh600048', '保利发展')}
        tracking_stocks_names_dict = read_collect_target_stock.ReadCollectTargetStock().get_stocks_and_their_names()
        # 获取标的池中跟踪关注股票及对应的估值方式和触发条件(估值，低于等于历史百分位)
        # 如，{'000002': {'pb': (0.95, 0.5), 'pe': (1, 2)}, '600048': {'pb': (0.95, 0.5)}}
        tracking_stocks_valuation_method_and_trigger_dict = read_collect_target_stock.ReadCollectTargetStock().get_stocks_valuation_method_and_trigger()
        # 保存所有触发了条件的股票
        triggered_stocks_info_dict = dict()
        for stock_code in tracking_stocks_names_dict:
            # 含股票上市地的代码及中文名称，如 ('sz000002', '万科A')
            stock_id_name_tuple = tracking_stocks_names_dict.get(stock_code)
            # 该支股票的全部估值策略
            for estimation_method in tracking_stocks_valuation_method_and_trigger_dict.get(stock_code):
                # 估值方式所对应的触发条件(估值，低于等于历史百分位)，(0.95, 0.5)
                trigger_tuple = tracking_stocks_valuation_method_and_trigger_dict.get(stock_code).get(estimation_method)
                # 如果触发条件，result 返回 股票上市地的代码, 中文名称, 估值方式, 估值, 提示信息
                # 如果未触发条件，result 返回 None
                result = self.compare_realtime_estimation_with_triggers(stock_code, stock_id_name_tuple, estimation_method, trigger_tuple)
                # 如果返回的结果不为空
                if result != None:
                    # 纳入属于触发预设条件的股票范围
                    # 如果之前未保存过该股票的触发条件返回信息
                    if stock_code not in triggered_stocks_info_dict:
                       value_list = []
                       value_list.append(result)
                       triggered_stocks_info_dict[stock_code] = value_list
                    # 如果之前已保存过该股票的触发条件返回信息
                    else:
                        triggered_stocks_info_dict[stock_code].append(result)

        # 返回 所有触发了条件的股票
        return triggered_stocks_info_dict

    def get_tracking_stocks_realtime_indicators_multi_thread(self):
        # 获取所有跟踪股票的实时指标, 多线程
        # 返回 所有触发了条件的股票及信息的字典
        # 如 {'000002': [('sz000002', '万科A', 'pb', '0.98', '小于设定估值 0.99'), ('sz000002', '万科A', 'pe_ttm', '5.84', '3.39% 小于设定估值百分位 12%')], '600048': [('sh600048', '保利发展', 'pb', '1.07', '小于设定估值 1.1')]}


        # 获取标的池中跟踪关注股票及他们的中文名称
        # {'000002': ('sz000002', '万科A'), '600048': ('sh600048', '保利发展')}
        tracking_stocks_names_dict = read_collect_target_stock.ReadCollectTargetStock().get_stocks_and_their_names()
        # 获取标的池中跟踪关注股票及对应的估值方式和触发条件(估值，低于等于历史百分位)
        # 如，{'000002': {'pb': (0.95, 0.5), 'pe': (1, 2)}, '600048': {'pb': (0.95, 0.5)}}
        tracking_stocks_valuation_method_and_trigger_dict = read_collect_target_stock.ReadCollectTargetStock().get_stocks_valuation_method_and_trigger()

        # 保存所有触发了条件的股票
        triggered_stocks_info_dict = dict()

        # 启用多线程
        running_threads = []
        # 启用线程锁
        threadLock = threading.Lock()

        for stock_code in tracking_stocks_names_dict:
            # 含股票上市地的代码及中文名称，如 ('sz000002', '万科A')
            stock_id_name_tuple = tracking_stocks_names_dict.get(stock_code)
            # 股票预设的所有估值方式和对应的触发条件(估值，低于等于历史百分位)， 如 {'pb': (0.95, 0.5), 'pe': (1, 2)}
            stock_all_estimation_methods_and_triggers = tracking_stocks_valuation_method_and_trigger_dict.get(stock_code)
            # 启动线程
            running_thread = threading.Thread(target=self.get_single_tracking_stock_realtime_indicators,
                                              kwargs={"stock_code": stock_code, "stock_id_name_tuple": stock_id_name_tuple,
                                                      "stock_all_estimation_methods_and_triggers": stock_all_estimation_methods_and_triggers,
                                                      "triggered_stocks_info_dict": triggered_stocks_info_dict,
                                                      "threadLock": threadLock})
            # 添加线程
            running_threads.append(running_thread)

        # 开启新线程
        for mem in running_threads:
            mem.start()

        # 等待所有线程完成
        for mem in running_threads:
            mem.join()

        # 所有触发了条件的股票返回信息
        return triggered_stocks_info_dict


    def get_single_tracking_stock_realtime_indicators(self, stock_code, stock_id_name_tuple, stock_all_estimation_methods_and_triggers, triggered_stocks_info_dict, threadLock):
        # 获取单个跟踪股票，所有估值策略下的返回信息

        # stock_code, 股票代码，如 '000002'
        # stock_id_name_tuple， 含股票上市地的代码及中文名称，如 ('sz000002', '万科A')
        # stock_all_estimation_methods_and_triggers, 股票预设的所有估值方式和对应的触发条件(估值，低于等于历史百分位), 如 {'pb': (0.95, 0.5), 'pe': (1, 2)}
        # riggered_stocks_info_dict, 保存所有触发了条件的股票，一个dict
        # threadLock，线程锁，用于线程同步, 向 triggered_stocks_info_list添加东西时，避免冲突

        # 无返回，将该跟踪股票下，所有估值策略下的返回信息添加进triggered_stocks_info_list

        # 该支股票的全部估值策略
        for estimation_method in stock_all_estimation_methods_and_triggers:
            # 估值方式所对应的触发条件(估值，低于等于历史百分位)，(0.95, 0.5)
            trigger_tuple = stock_all_estimation_methods_and_triggers.get(estimation_method)
            # 如果触发条件，result 返回 股票上市地的代码, 中文名称, 估值方式, 估值, 提示信息
            # 如果未触发条件，result 返回 None
            result = self.compare_realtime_estimation_with_triggers(stock_code, stock_id_name_tuple, estimation_method,trigger_tuple)
            # 如果返回的结果不为空
            if result != None:
                # 纳入属于触发预设条件的股票范围

                # 获取锁，用于线程同步
                threadLock.acquire()
                # 如果之前未保存过该股票的触发条件返回信息
                if stock_code not in triggered_stocks_info_dict:
                    value_list = []
                    value_list.append(result)
                    triggered_stocks_info_dict[stock_code] = value_list
                # 如果之前已保存过该股票的触发条件返回信息
                else:
                    triggered_stocks_info_dict[stock_code].append(result)
                # 释放锁，开启下一个线程
                threadLock.release()


    def compare_realtime_estimation_with_triggers(self, stock_code, stock_id_name_tuple, estimation_method, trigger_tuple):
        # 对比获取到的估值与触发条件做对比

        # stock_code, 股票代码，如 '000002'
        # stock_id_name_tuple， 含股票上市地的代码及中文名称，如 ('sz000002', '万科A')
        # estimation_method, 估值方式，如 pe_ttm, pb, dr_ttm
        # trigger_tuple， 估值方式所对应的触发条件(估值，低于等于历史百分位)，(0.95, 0.5)
        # return:
        # 如果触发条件，返回 股票上市地的代码, 中文名称, 估值方式, 估值, 提示信息
        # 如果未触发条件，返回 None


        # 从雪球获取 估值
        estimation_from_xueqiu = get_stock_real_time_indicator_from_xueqiu.GetStockRealTimeIndicatorFromXueqiu().get_single_stock_real_time_indicator(
           stock_id_name_tuple[0], estimation_method)

        # 如果实时估值小于等于触发条件
        if( float(estimation_from_xueqiu)<=trigger_tuple[0]):
            # 返回 股票上市地的代码, 中文名称, 估值方式, 估值, 提示信息
            # 如 ('sz000002', '万科A', 'pb', '0.89', '小于设定估值 0.95')
            return stock_id_name_tuple[0],stock_id_name_tuple[1],estimation_method,estimation_from_xueqiu,"小于设定估值 "+str(trigger_tuple[0])

        # 从数据库获取该股票的历史估值数据
        # 如 [{'pb': Decimal('0.9009277645423478')}, {'pb': Decimal('0.9101209049968616')}, ，，，]
        # 或者 [{'pe_ttm': Decimal('0.9009277645423478')}, {'pe_ttm': Decimal('0.9101209049968616')},, ，，，]
        historical_estimation_list = self.get_stock_historical_estimation_from_db(stock_code, estimation_method)
        # 如果实时估值小于历史最小值
        if (float(estimation_from_xueqiu) <= historical_estimation_list[0][estimation_method]):
            # 返回 股票上市地的代码, 中文名称, 估值方式, 估值, 提示信息
            # 如 ('sz000002', '万科A', 'pb', '0.89', '处于历史最低位')
            return stock_id_name_tuple[0],stock_id_name_tuple[1],estimation_method,estimation_from_xueqiu,"处于历史最低位"

        # 遍历股票的历史估值数据
        for i in range(len(historical_estimation_list)):
            # 如果历史估值中某个数据大于等于实时估值
            if (historical_estimation_list[i][estimation_method]>=float(estimation_from_xueqiu)):
                # 计算处于历史百分位
                percent = round(i/len(historical_estimation_list)*100,2)
                # 如果小于等于设定估值百分位
                if (percent<=trigger_tuple[1]):
                    # 返回 股票上市地的代码, 中文名称, 估值方式, 估值, 提示信息
                    # 如 ('sz000002', '万科A', 'pb', '0.97', '0.47% 小于设定估值百分位 0.5%')
                    return stock_id_name_tuple[0], stock_id_name_tuple[1], estimation_method, estimation_from_xueqiu, str(percent)+"%"+" 小于设定估值百分位 " + str(trigger_tuple[1]) + "%"
                return None



    def get_stock_historical_estimation_from_db(self, stock_code, estimation_method):
        # 从数据库获取该股票的历史估值数据列表
        # stock_code, 股票代码，如 000002
        # estimation_method, 估值方式，目前限，pe_ttm 和 pb
        # return [{'pb': Decimal('0.9009277645423478')}, {'pb': Decimal('0.9101209049968616')}, {'pb': Decimal('0.9218676955776292')}, {'pb': Decimal('0.9223784256028800')}, ，，，]

        selecting_sql = "SELECT %s FROM stocks_main_estimation_indexes_historical_data where stock_code = '%s' order by %s " % (
        estimation_method, stock_code, estimation_method)
        historical_estimation_list = db_operator.DBOperator().select_all("financial_data", selecting_sql)
        return  historical_estimation_list

    def main(self):
        # 单线程方式
        # return self.get_tracking_stocks_realtime_indicators_single_thread()
        # 多线程方式
        return self.get_tracking_stocks_realtime_indicators_multi_thread()

if __name__ == '__main__':
    time_start = time.time()
    go = StockStrategyMonitoringEstimation()
    result = go.main()
    print(result)
    time_end = time.time()
    print('Time Cost: ' + str(time_end - time_start))