import decimal
import sys
sys.path.append("..")
import database.db_operator as db_operator


class FundStrategyPBEstimation:
    # 基金策略，市净率率估值法
    # 运行时间： 每个交易日14:45

    def __init__(self):
        pass

    def get_index_constitute_stocks(self, index_code):
        # 获取数据库中的指数最新的构成股和比例
        # param: index_code 指数代码，如 399997
        # 返回： 指数构成股及其权重
        selecting_sql = "SELECT stock_code, stock_name, weight FROM index_constituent_stocks_weight WHERE index_code LIKE '%s' AND submission_date = (SELECT submission_date FROM index_constituent_stocks_weight WHERE index_code LIKE '%s' ORDER BY submission_date DESC LIMIT 1)" % (index_code+'%', index_code+'%')
        index_constitute_stocks_weight = db_operator.DBOperator().select_all("financial_data", selecting_sql)
        return index_constitute_stocks_weight


    def get_stock_historical_pb(self, stock_code, stock_name, day):
        # 提取股票的历史市净率信息， 包括市净率, 扣商誉市净率
        # param: stock_code, 股票代码，如 000596
        # param: stock_name， 股票名称，如 古井贡酒
        # param: day, 日期， 如 2020-09-01
        # 返回：市净率, 扣商誉市净率
        selecting_sql = "select pb, pb_wo_gw from stocks_main_estimation_indexes_historical_data where stock_code = '%s' and stock_name = '%s' and date = '%s' " % (stock_code, stock_name,day)
        pb_info = db_operator.DBOperator().select_all("financial_data", selecting_sql)
        return pb_info

    def calculate_a_historical_date_index_PB(self, index_code, day):
        # 基于当前指数构成，计算过去某一天该指数市净率, 扣商誉市净率
        # param: index_code 指数代码，如 399997
        # param: day, 日期， 如 2020-09-01
        # 返回 指数市净率, 扣商誉市净率
        pb = 0
        pb_wo_gw = 0

        # 获取指数成分股及权重
        index_constitute_stocks_weight = self.get_index_constitute_stocks(index_code)
        for stock_info in index_constitute_stocks_weight:
            # 获取指数市净率信息
            pb_info = self.get_stock_historical_pb(stock_info['stock_code'], stock_info['stock_name'], day)
            # 计算市净率, 扣商誉市净率
            pb += decimal.Decimal(pb_info[0]["pb"])*decimal.Decimal(stock_info["weight"])/100
            pb_wo_gw += decimal.Decimal(pb_info[0]["pb_wo_gw"])*decimal.Decimal(stock_info["weight"])/100
        return pb, pb_wo_gw

if __name__ == '__main__':
    go = FundStrategyPBEstimation()
    pb, pb_wo_gw = go.calculate_a_historical_date_index_PB("399965", "2020-11-18")
    print(pb, pb_wo_gw)