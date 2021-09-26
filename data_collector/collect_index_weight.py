import requests
import json
import time
import sys

sys.path.append("..")
import config.joinquant_account_info as joinquant_account_info
import log.custom_logger as custom_logger
import database.db_operator as db_operator
import target_pool.read_collect_target_fund as read_collect_target_fund


class CollectIndexWeight:
    # 从聚宽获取指数的权重数据，并存入数据库
    # 运行频率：每月底

    def __init__(self):
        pass

    def get_index_stocks_weight(self, index_code):
        # 获取最新指数权重
        # 输入：index_code，指数代码，例如：399997.XSHE
        # 输出：指数构成信息

        url, body, token = joinquant_account_info.JoinquantAccountInfo().get_token()
        # 获取当前时间
        today = time.strftime("%Y-%m-%d", time.localtime())
        body = {
            "method": "get_index_weights",
            "token": token,
            "code": index_code,
            "date": today
        }

        try:
            # 获取聚宽返回的指数构成信息
            response = requests.post(url, data=json.dumps(body))
            # print(response.text)
            return response.text

        except Exception as e:
            # 日志记录
            msg = 'Failed to get joinquant index weights' + '  ' + str(e)
            custom_logger.CustomLogger().log_writter(msg, 'error')

    def get_db_index_stocks_weight(self, index_code):
        # 获取数据库中最新的指数权重
        # 输入：index_code，指数代码，例如：399997.XSHE
        # 输出：指数构成信息

        try:
            # 查询sql
            selecting_sql = "SELECT stock_code, stock_name, weight FROM index_constituent_stocks_weight WHERE index_code" \
                            " = '%s' AND submission_date = (SELECT MAX(submission_date) FROM " \
                            "index_constituent_stocks_weight WHERE index_code = '%s') " % (index_code, index_code)
            # 从数据库获取内容
            db_index_content = db_operator.DBOperator().select_all("financial_data", selecting_sql)
            return db_index_content

        except Exception as e:
            # 日志记录
            msg = 'Failed to get index weights from DB' + '  ' + str(e)
            custom_logger.CustomLogger().log_writter(msg, 'error')

    def is_the_db_containing_the_same_index_content(self, index_code):
        # 对比 新获取到的指数信息 与 数据库中的 指数信息
        # 输入：index_code，指数代码，例如：399997.XSHE
        # 返回：True是：包含同样信息；False否，未包含同样信息

        # 获取数据库中同一个的信息
        db_index_content_list = self.get_db_index_stocks_weight(index_code)

        # 如果未获取到任何信息
        # 说明 未包含同样信息
        if len(db_index_content_list) == 0:
            # 日志记录
            msg = 'DB has no any info about ' + index_code + '. Index ' + index_code + ' need to be collected'
            custom_logger.CustomLogger().log_writter(msg, 'info')

            return False

        # 获取最新的指数信息
        index_stocks_weight_str = self.get_index_stocks_weight(index_code)
        # 将聚宽传回的指数成分股及其权重信息，由string转化为list，便于处理
        index_holding_detail_list = index_stocks_weight_str.replace('\n', ',').split(',')
        stock_code = ''
        weight = 0

        # 聚宽返回的指数成分股的格式，每4个为一个循环，从第5个开始为正式数据['code','display_name','date', 'weight', '000568.XSHE','泸州老窖','2020-01-28','4.3930','000596.XSHE','古井贡酒','2020-01-28','1.0820',,,,]
        for new_content_index in range(4, len(index_holding_detail_list)):
            if new_content_index % 4 == 0:
                # 获取股票代码
                stock_code = index_holding_detail_list[new_content_index][:-5]
            elif new_content_index % 4 == 3:
                # 获取股票权重
                weight = index_holding_detail_list[new_content_index]
                # 遍历数据库中的信息
                for db_content_index in range(len(db_index_content_list)):
                    # 只要有 一个股票代码相同，但是权重不同， 说明新获取的指数信息与数据库中的信息不相同
                    if stock_code == db_index_content_list[db_content_index]["stock_code"] and \
                            weight != str(db_index_content_list[db_content_index]["weight"]):
                        # 日志记录
                        msg = index_code + '\'s info need to be updated '
                        custom_logger.CustomLogger().log_writter(msg, 'info')
                        return False

        # 日志记录
        msg = 'DB has the same info about ' + index_code
        custom_logger.CustomLogger().log_writter(msg, 'info')
        return True

    def save_index_stocks_weight_to_db(self, index_code, index_name):
        # 存入数据库
        # 输入：index_code，指数代码，例如：399997.XSHE
        # 		index_name，指数名称，例如：中证白酒指数
        # 输出：指数成分股存入数据库
        index_stocks_weight_str = self.get_index_stocks_weight(index_code)
        # 将聚宽传回的指数成分股及其权重信息，由string转化为list，便于处理
        index_holding_detail_list = index_stocks_weight_str.replace('\n', ',').split(',')
        # 获取今天日期
        today = time.strftime("%Y-%m-%d", time.localtime())

        global_stock_code = ''
        stock_name = ''
        weight = 0
        stock_exchange_location = ''

        # 聚宽返回的指数成分股的格式，每4个为一个循环，从第5个开始为正式数据['code','display_name','date', 'weight',
        # '000568.XSHE','泸州老窖','2020-01-28','4.3930','000596.XSHE','古井贡酒','2020-01-28','1.0820',,,,]
        for i in range(4, len(index_holding_detail_list)):
            if i % 4 == 0:
                # 获取股票代码
                global_stock_code = index_holding_detail_list[i]
                if global_stock_code[-4:] == "XSHE":
                    stock_exchange_location = 'sz'
                elif global_stock_code[-4:] == "XSHG":
                    stock_exchange_location = 'sh'
            elif i % 4 == 1:
                # 获取股票名称
                stock_name = index_holding_detail_list[i]
            elif i % 4 == 3:
                # 获取股票权重
                weight = index_holding_detail_list[i]

                try:
                    # 插入的SQL
                    inserting_sql = "INSERT INTO index_constituent_stocks_weight(index_code,index_name," \
                                    "global_stock_code,stock_code,stock_name,stock_exchange_location," \
                                    "weight,source,submission_date)" \
                                    "VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (
                                        index_code[:-5], index_name, global_stock_code, global_stock_code[:6], stock_name,
                                        stock_exchange_location, weight, '聚宽', today)
                    db_operator.DBOperator().operate("insert", "financial_data", inserting_sql)

                except Exception as e:
                    # 日志记录
                    msg = 'Failed to insert index weights into DB' + '  ' + str(e)
                    custom_logger.CustomLogger().log_writter(msg, 'error')

        # 日志记录
        msg = 'Save ' + index_code + ' ' + index_name + '\'s constituent stocks and weights into DB'
        custom_logger.CustomLogger().log_writter(msg, 'info')

    def main(self, index_code, index_name):
        # 收集指数信息
        # 输入：index_code，指数代码，例如：399997.XSHE
        # 		index_name，指数名称，例如：中证白酒指数
        # 输出：指数成分股存入数据库

        # 数据库中是否已包含相同的指数信息
        is_containing = self.is_the_db_containing_the_same_index_content(index_code)
        # 如果没有包含相同的信息，则收集
        if not is_containing:
            self.save_index_stocks_weight_to_db(index_code, index_name)

    def collect_tracking_index_weight(self):
        # 收集所跟踪关注指数的成分及权重
        # 输入：无
        # 输出：存入数据

        # 获取标的池中跟踪关注指数及他们的中文名称,字典形式。如，{'399396.XSHE': '国证食品', '000932.XSHG': '中证主要消费',,,,}
        tracking_indexes_names_dict = read_collect_target_fund.ReadCollectTargetFund().get_indexes_and_their_names()
        # 收集指数的成分及权重
        for index in tracking_indexes_names_dict:
            self.main(index, tracking_indexes_names_dict.get(index))
        # 日志记录
        msg = 'Just collected tracking index stocks and weight'
        custom_logger.CustomLogger().log_writter(msg, 'info')

if __name__ == "__main__":
    go = CollectIndexWeight()
    go.collect_tracking_index_weight()
    #result = go.get_index_stocks_weight('399997.XSHE')
    #print(result)
    # go.save_index_stocks_weight_to_db("399997.XSHE","中证白酒")
    #result = go.get_query_count()
    # result = go.get_db_index_stocks_weight('399997.XSHE')
    # result = go.is_the_db_containing_the_same_index_content('399997.XSHE')
    #print(result)
    # print(type(result))
    # print(len(result))
    #go.main("399396.XSHE", "国证食品")
    #go.main("399997.XSHE","中证白酒")
    #go.main("399965.XSHE", "800地产")
    #go.main("000932.XSHG", "中证主要消费")
    #print("--------------")
    #go.is_the_db_containing_the_same_index_content("399997.XSHE")
