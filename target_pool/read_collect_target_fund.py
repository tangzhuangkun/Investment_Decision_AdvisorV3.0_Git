
import sys
sys.path.append('..')
import target_pool.target as target
import data_collector.collect_index_weight as collect_index_weight


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


    def collect_tracking_index_weight(self):
        # 收集所跟踪关注指数的成分及权重
        # 输入：无
        # 输出：存入数据


        # 获取标的池中跟踪关注指数及他们的中文名称,字典形式。如，{'399396.XSHE': '国证食品', '000932.XSHG': '中证主要消费',,,,}
        tracking_indexes_names_dict = self.get_indexes_and_their_names()
        # 收集指数的成分及权重
        for index in tracking_indexes_names_dict:
            collect_index_weight.CollectIndexWeight().main(index, tracking_indexes_names_dict.get(index))



if __name__ == '__main__':
    go = ReadCollectTargetFund()
    tracking_indexes_names_dict = go.collect_tracking_index_weight()
    print(tracking_indexes_names_dict)