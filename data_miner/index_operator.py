import sys
sys.path.append("..")
import database.db_operator as db_operator


class IndexOperator:
    # 对指数的通用操作

    def __init__(self):
        pass

    def get_index_constitute_stocks(self, index_code):
        # 获取数据库中的指数最新的构成股和比例
        # param: index_code 指数代码，如 399997 或者 399997.XSHE
        # 返回： 指数构成股及其权重,
        # 如 [{'global_stock_code': '000568.XSHE', 'stock_code': '000568', 'stock_name': '泸州老窖', 'weight': Decimal('14.8100')},
        # {'global_stock_code': '000596.XSHE', 'stock_code': '000596', 'stock_name': '古井贡酒', 'weight': Decimal('3.6940')}]
        selecting_sql = "SELECT global_stock_code, stock_code, stock_name, weight FROM index_constituent_stocks_weight " \
                        "WHERE index_code LIKE '%s' AND submission_date = (" \
                        "SELECT submission_date FROM index_constituent_stocks_weight " \
                        "WHERE index_code LIKE '%s' " \
                        "ORDER BY submission_date DESC LIMIT 1)" % (index_code+'%', index_code+'%')
        index_constitute_stocks_weight = db_operator.DBOperator().select_all("financial_data", selecting_sql)
        return index_constitute_stocks_weight

    def get_index_name(self, index_code):
        # 根据指数代码获取指数名称
        selecting_sql = "SELECT index_name FROM index_constituent_stocks_weight where index_code LIKE '%s' limit 1" % (index_code + '%')
        index_name = db_operator.DBOperator().select_one("financial_data", selecting_sql)
        return index_name["index_name"]


if __name__ == '__main__':
    go = IndexOperator()
    #index_constitute_stocks_weight = go.get_index_constitute_stocks('399997')
    #print(index_constitute_stocks_weight)
    index_name = go.get_index_name("399997.XSHE")
    print(index_name)