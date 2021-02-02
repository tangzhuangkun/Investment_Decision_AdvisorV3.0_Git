import decimal
import datetime
import sys
sys.path.append("..")
import database.db_operator as db_operator


class FundStrategyPBEstimation:
    # 指数基金策略，市净率率估值法

    def __init__(self):
        pass

    def get_index_constitute_stocks(self, index_code):
        # 获取数据库中的指数最新的构成股和比例
        # param: index_code 指数代码，如 399997
        # 返回： 指数构成股及其权重, 如[{'stock_code': '000002', 'stock_name': '万科A', 'weight': Decimal('15.5390')}, {'stock_code': '000031', 'stock_name': '大悦城', 'weight': Decimal('0.9320')}, {'stock_code': '001914', 'stock_name': '招商积余', 'weight': Decimal('1.7160')}, {'stock_code': '000069', 'stock_name': '华侨城A', 'weight': Decimal('4.2780')}]
        selecting_sql = "SELECT stock_code, stock_name, weight FROM index_constituent_stocks_weight WHERE index_code LIKE '%s' AND submission_date = (SELECT submission_date FROM index_constituent_stocks_weight WHERE index_code LIKE '%s' ORDER BY submission_date DESC LIMIT 1)" % (index_code+'%', index_code+'%')
        index_constitute_stocks_weight = db_operator.DBOperator().select_all("financial_data", selecting_sql)
        return index_constitute_stocks_weight


    def get_stock_historical_pb(self, stock_code, stock_name, day):
        # 提取股票的历史某一天的市净率信息， 包括市净率, 扣商誉市净率
        # param: stock_code, 股票代码，如 000596
        # param: stock_name， 股票名称，如 古井贡酒
        # param: day, 日期， 如 2020-09-01
        # 返回：市净率, 扣商誉市净率
        selecting_sql = "select pb, pb_wo_gw from stocks_main_estimation_indexes_historical_data where stock_code = '%s' and stock_name = '%s' and date = '%s' " % (stock_code, stock_name,day)
        pb_info = db_operator.DBOperator().select_all("financial_data", selecting_sql)
        return pb_info

    def calculate_index_PB_in_a_historical_date_(self, index_code, day):
        # 基于当前指数构成，计算过去某一天该指数市净率, 扣商誉市净率
        # param: index_code 指数代码，如 399997
        # param: day, 日期， 如 2020-09-01
        # 返回 指数市净率, 扣商誉市净率， 如 1.510749960655767552952 1.541282892742027267960
        pb = 0
        pb_wo_gw = 0

        # TODO 建立一张表，记录交易日
        # TODO day判断，跳过非交易日, http://php-note.com/article/1854.html

        # 获取指数成分股及权重
        index_constitute_stocks_weight = self.get_index_constitute_stocks(index_code)
        for stock_info in index_constitute_stocks_weight:
            # 获取指数市净率信息
            pb_info = self.get_stock_historical_pb(stock_info['stock_code'], stock_info['stock_name'], day)
            # 如果能获取到信息
            if len(pb_info)!=0:
                # 计算市净率, 扣商誉市净率
                pb += decimal.Decimal(pb_info[0]["pb"])*decimal.Decimal(stock_info["weight"])/100
                pb_wo_gw += decimal.Decimal(pb_info[0]["pb_wo_gw"])*decimal.Decimal(stock_info["weight"])/100
                # print(stock_info['stock_name'])
                # print(decimal.Decimal(pb_info[0]["pb"])*decimal.Decimal(stock_info["weight"])/100)
                # print(pb)
                # print(decimal.Decimal(pb_info[0]["pb_wo_gw"])*decimal.Decimal(stock_info["weight"])/100)
                # print(pb_wo_gw)

            # 如果不能获取到信息
            else:
                # TODO 检查某个日期的 前后数据
                # TODO 某个日期无数据，这个日期前后有数据的，取之后的数据
                # TODO 某个日期无数据，这个日期，后有数据，前无数据的，所有成分股计算完成之后，返回数值按等比例放大，以弥补缺失的数据。需要考虑可能多只股票同时缺失数据的情况。

                # 离某个日期最近的数据
                # SELECT *, abs(UNIX_TIMESTAMP(date) - UNIX_TIMESTAMP('2016-07-01')) as min
                # from stocks_main_estimation_indexes_historical_data
                # where stock_code = "000002" order BY min asc limit 1;
                return 0,0
        return pb, pb_wo_gw

    def calculate_index_pb_in_a_period_time(self, index_code, n_year):
        # 基于当前成分股和比例，计算该指数过去x年，每一天的市净率，扣商誉市净率
        # param: index_code 指数代码，如 399997
        # 返回 每一天的指数市净率, 扣商誉市净率
        # 获取今天日期

        # todo 未完
        now_time = datetime.date.today()
        # 获取n年前的起始日期
        last_n_year = now_time + datetime.timedelta(days=-round(365*n_year))
        # 遍历这段时间
        for i in range((now_time - last_n_year).days + 1):
            specific_day = last_n_year + datetime.timedelta(days=i)
            pb, pb_wo_gw = self.calculate_index_PB_in_a_historical_date_(index_code, str(specific_day))
            print(specific_day, pb, pb_wo_gw)




if __name__ == '__main__':
    go = FundStrategyPBEstimation()
    #result = go.get_index_constitute_stocks("399965")
    #print(result)
    #result = go.get_stock_historical_pb("000002", "万科A", "2020-05-24")
    #print(result)
    pb, pb_wo_gw = go.calculate_index_PB_in_a_historical_date_("399965", "2020-11-18")
    print(pb, pb_wo_gw)
    #go.calculate_index_pb_in_a_period_time("399965",0.5)