import time
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



    def get_tracking_stocks_realtime_indicators(self):
        # 获取所有跟踪股票的实时指标

        # 获取标的池中跟踪关注股票及他们的中文名称
        # {'000002': ('sz000002', '万科A'), '600048': ('sh600048', '保利发展')}
        tracking_stocks_names_dict = read_collect_target_stock.ReadCollectTargetStock().get_stocks_and_their_names()
        # 获取标的池中跟踪关注股票及对应的估值方式和触发条件(估值，低于等于历史百分位)
        # 如，{'000002': {'pb': (0.95, 0.5), 'pe': (1, 2)}, '600048': {'pb': (0.95, 0.5)}}
        tracking_stocks_valuation_method_and_trigger_dict = read_collect_target_stock.ReadCollectTargetStock().get_stocks_valuation_method_and_trigger()

        for stock_code in tracking_stocks_names_dict:
            # 该支股票的全部估值策略
            for estimation_method in tracking_stocks_valuation_method_and_trigger_dict.get(stock_code):
               result = self.compare_realtime_estimation_with_triggers(stock_code,tracking_stocks_names_dict.get(stock_code),estimation_method,tracking_stocks_valuation_method_and_trigger_dict.get(stock_code).get(estimation_method))
               print(result)

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


    '''
        def call_xueqiu_to_get_estimation(self, stock_id_name_tuple, estimation_method):
        # 调用雪球获取估值参数
        # stock_id_name_tuple， 含股票上市地的代码及中文名称，如 ('sz000002', '万科A')
        # estimation_method, 估值方式，如 pe_ttm, pb, dr_ttm
        # return, 返回tuple( 股票上市地的代码, 中文名称, 估值方式, 估值)， 如 sz000002 万科A pb 0.98； sz000002 万科A pe_ttm 5.84

        # 股票代码，如 'sz000002'
        stock_id_with_exchange = stock_id_name_tuple[0]
        # 股票名称， 如 万科A
        stock_name= stock_id_name_tuple[1]
        estimation_from_xueqiu = get_stock_real_time_indicator_from_xueqiu.GetStockRealTimeIndicatorFromXueqiu().get_single_stock_real_time_indicator(
            stock_id_with_exchange, estimation_method)
        # 返回 股票上市地的代码, 中文名称, 估值方式, 估值
        # 如 ('sz000002', '万科A', 'pb', '0.98')
        return stock_id_with_exchange, stock_name, estimation_method, estimation_from_xueqiu
    '''



if __name__ == '__main__':
    time_start = time.time()
    go = StockStrategyMonitoringEstimation()
    go. get_tracking_stocks_realtime_indicators()
    #go.get_stock_historical_estimation_from_db("000002","pb")
    #result = go.compare_realtime_estimation_with_triggers('000002', ('sz000002', '万科A'), 'pb', (0.95, 0.5))
    #print(result)
    time_end = time.time()
    print('Time Cost: ' + str(time_end - time_start))