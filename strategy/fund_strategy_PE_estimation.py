import decimal
import sys
sys.path.append("..")
import database.db_operator as db_operator


class FundStrategyPEEstimation:
    # 基金策略，市盈率估值法
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

    def get_stock_historical_pe(self, stock_code, stock_name, day):
        # 提取股票的历史市盈率信息， 包括市盈率TTM, 扣非市盈率TTM
        # param: stock_code, 股票代码，如 000596
        # param: stock_name， 股票名称，如 古井贡酒
        # param: day, 日期， 如 2020-09-01
        # 返回：市盈率TTM, 扣非市盈率TTM
        selecting_sql = "select pe_ttm, pe_ttm_nonrecurring from stocks_main_estimation_indexes_historical_data where stock_code = '%s' and stock_name = '%s' and date = '%s' " % (stock_code, stock_name,day)
        pe_info = db_operator.DBOperator().select_all("financial_data", selecting_sql)
        return pe_info


    def calculate_a_historical_date_index_PE(self, index_code, day):
        # 基于当前指数构成，计算过去某一天该指数市盈率TTM, 扣非市盈率TTM
        # param: index_code 指数代码，如 399997
        # param: day, 日期， 如 2020-09-01
        # 返回 指数市盈率TTM, 扣非市盈率TTM, 均保留3位小数
        pe_ttm = 0
        pe_ttm_nonrecurring = 0

        # 获取指数成分股及权重
        index_constitute_stocks_weight = self.get_index_constitute_stocks(index_code)
        for stock_info in index_constitute_stocks_weight:
            # 获取指数市盈率信息
            pe_info = self.get_stock_historical_pe(stock_info['stock_code'], stock_info['stock_name'], day)
            # 计算市盈率TTM, 扣非市盈率TTM
            pe_ttm += decimal.Decimal(pe_info[0]["pe_ttm"])*decimal.Decimal(stock_info["weight"])/100
            pe_ttm_nonrecurring += decimal.Decimal(pe_info[0]["pe_ttm_nonrecurring"])*decimal.Decimal(stock_info["weight"])/100
        return round(pe_ttm,3), round(pe_ttm_nonrecurring,3)

    # todo 添加计算实时的市盈率

if __name__ == '__main__':
    go = FundStrategyPEEstimation()
    #result = go.get_index_constitute_stocks("399997")
    #print(result)
    #result = go.get_stock_historical_pe("000596", "古井贡酒", "2020-11-16")
    #print(result)
    pe_ttm, pe_ttm_nonrecurring = go.calculate_a_historical_date_index_PE("399965","2020-10-19")
    print(pe_ttm, pe_ttm_nonrecurring)