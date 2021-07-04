
import sys
sys.path.append('..')
import target_pool.target as target
import data_collector.collect_index_weight as collect_index_weight
import log.custom_logger as custom_logger


class ReadCollectTargetFund:
    # 读取标的池中关于基金的信息

    def __init__(self):
        pass

    def get_indexes_and_their_names(self):
        # 获取标的池中跟踪关注指数及他们的中文名称
        # 输入：无
        # 输出：获取标的池中跟踪关注指数及他们的中文名称,字典形式。如，{'399396.XSHE': '国证食品', '000932.XSHG': '中证主要消费',,,,}

        target_index_funds = target.target_index_funds
        tracking_indexes_names_dict = {}
        for tracking_info in target_index_funds:
            tracking_indexes_names_dict[target_index_funds.get(tracking_info).get('tracking_index_code')] = target_index_funds.get(tracking_info).get('tracking_index_name')
        return tracking_indexes_names_dict

    '''
    def collect_tracking_index_weight(self):
        # 收集所跟踪关注指数的成分及权重
        # 输入：无
        # 输出：存入数据


        # 获取标的池中跟踪关注指数及他们的中文名称,字典形式。如，{'399396.XSHE': '国证食品', '000932.XSHG': '中证主要消费',,,,}
        tracking_indexes_names_dict = self.get_indexes_and_their_names()
        # 收集指数的成分及权重
        for index in tracking_indexes_names_dict:
            collect_index_weight.CollectIndexWeight().main(index, tracking_indexes_names_dict.get(index))
        # 日志记录
        msg = 'Just collected tracking index stocks and weight'
        custom_logger.CustomLogger().log_writter(msg, 'info')
    '''

    def get_index_valuation_method(self):
        # 获取标的池中跟踪关注指数的估值方式
        # 输入：无
        # 输出：获取标的池中跟踪关注指数代码及对应估值方式,
        # 如{'399396.XSHE': ['pe'], '000932.XSHG': ['pe'], '399997.XSHE': ['pe'], '399965.XSHE': ['pb'], '399986.XSHE': ['pb'], '000036.XSHG': ['pe']}

        target_index_funds = target.target_index_funds
        tracking_indexes_valuation_methods_dict = {}
        for tracking_info in target_index_funds:
            tracking_indexes_valuation_methods_dict[target_index_funds.get(tracking_info).get('tracking_index_code')] =target_index_funds.get(tracking_info).get('valuation_method_list')
        return tracking_indexes_valuation_methods_dict

    def index_valuated_by_method(self,method):
        # 获取通过xx估值法 估值的指数代码及其对应名称
        # 输入：method, 估值方式，目前有 pe：市盈率估值法； pb:市净率估值法
        # 输出：估值的指数代码及其对应名称
        # 如 {'399396.XSHE': '国证食品', '000932.XSHG': '中证主要消费', '399997.XSHE': '中证白酒', '000036.XSHG': '上证主要消费行业指数'}

        # 获取到 跟踪的指数代码及其对应名称
        tracking_indexes_names_dict = self.get_indexes_and_their_names()
        # 获取到 跟踪的指数代码及其估值方法
        tracking_indexes_valuation_methods_dict = self.get_index_valuation_method()
        # 指数代码及其对应名称
        valuation_method_indexes_names_dict = {}

        # 遍历跟踪的指数代码及其估值方法
        for index in tracking_indexes_valuation_methods_dict:
            # 如果所找的估值法在该指数对应的估值方法列表中
            if method in tracking_indexes_valuation_methods_dict.get(index):
                # 汇总指数代码及指数名称
                valuation_method_indexes_names_dict[index] = tracking_indexes_names_dict[index]
        return valuation_method_indexes_names_dict


if __name__ == '__main__':
    go = ReadCollectTargetFund()
    #go.get_indexes_and_their_names()
    #result = go.get_index_valuation_method()
    #print(result)
    result = go.index_valuated_by_method('pe')
    print(result)