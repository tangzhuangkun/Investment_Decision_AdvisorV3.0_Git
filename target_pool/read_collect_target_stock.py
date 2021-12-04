
import sys
sys.path.append('..')
import target_pool.target as target

class ReadCollectTargetStock:
    # 读取标的池中关于股票的信息

    def __init__(self):
        pass

    def get_stocks_and_their_names(self):
        # 获取标的池中跟踪关注股票及他们的中文名称
        # 输入：无
        # 输出：字典形式。如，{'000002': ('sz000002', '万科A'), '600048': ('sh600048', '保利发展')}

        target_stocks = target.target_stocks
        tracking_stocks_names_dict = {}
        for tracking_info in target_stocks:
            tracking_stocks_names_dict[tracking_info] = target_stocks.get(tracking_info).get('exchange_location')+tracking_info,target_stocks.get(tracking_info).get('stock_name')
        return tracking_stocks_names_dict

    def get_stocks_valuation_method_and_trigger(self):
        # 获取标的池中跟踪关注股票及对应的估值方式和触发条件
        # 输入：无
        # 输出：字典形式。如，{'000002': {'pb': (0.95, 0.5), 'pe': (1, 2)}, '600048': {'pb': (0.95, 0.5)}}

        target_stocks = target.target_stocks
        tracking_stocks_valuation_method_and_trigger_dict = {}
        for tracking_info in target_stocks:
            tracking_stocks_valuation_method_and_trigger_dict[tracking_info] = target_stocks.get(tracking_info).get(
                'valuation_method_and_trigger')
        return tracking_stocks_valuation_method_and_trigger_dict

    def get_stocks_monitoring_frequency(self):
        # 获取标的池中跟踪关注股票及对应的监控频率策略
        # 输入：无
        # 输出：字典形式。如 {'000002': ['minutely'], '600048': ['minutely']}

        target_stocks = target.target_stocks
        tracking_stocks_monitoring_frequency_dict = {}
        for tracking_info in target_stocks:
            tracking_stocks_monitoring_frequency_dict[tracking_info] = target_stocks.get(tracking_info).get(
                'monitoring_frequency_list')
        return tracking_stocks_monitoring_frequency_dict


if __name__ == '__main__':
    go = ReadCollectTargetStock()
    # result = go.get_stocks_and_their_names()
    # result = go.get_stocks_valuation_method_and_trigger()
    result = go.get_stocks_monitoring_frequency()
    print(result)