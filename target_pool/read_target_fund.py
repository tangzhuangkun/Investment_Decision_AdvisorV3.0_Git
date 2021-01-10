
import sys
sys.path.append('..')
import target_pool.target_fund as targetFund


class ReadTargetFund:
    # 读取标的池中的信息

    def __init__(self):
        pass

    def getIndexesAndTheirNames(self):
        # 输入：无
        # 输出：获取标的池中跟踪关注指数及他们的中文名称,字典形式。如，{'399396.XSHE': '国证食品', '000932.XSHG': '中证主要消费',,,,}

        target_index_funds = targetFund.target_index_funds
        tracking_indexes_names_dict = {}
        for tracking_info in target_index_funds:
            tracking_indexes_names_dict[target_index_funds.get(tracking_info).get('tracking_index_code')] = target_index_funds.get(tracking_info).get('tracking_index_name')
        return tracking_indexes_names_dict





if __name__ == '__main__':
    go = ReadTargetFund()
    tracking_indexes_names_dict = go.getIndexesAndTheirNames()
    print(tracking_indexes_names_dict)