import threading
import time
import multiprocessing

import sys
sys.path.append("..")
import database.db_operator as db_operator
import log.custom_logger as custom_logger


class CalculateIndexHistoricalEstimations:
    # 根据最新的指数成分和股票历史估值信息，运行mysql脚本，计算指数在历史上每一天的估值情况
    # 运行频率：每天收盘后

    def __init__(self):
        pass

    def read_run_cal_index_his_estimation_file(self):
        # 读取并运行mysql脚本

        with open('cal_index_his_estimation.sql', encoding='utf-8', mode='r') as f:
            # 读取整个sql文件
            inserting_sql = f.read()
            try:
                db_operator.DBOperator().operate("insert", "financial_data", inserting_sql)

            except Exception as e:
                # 日志记录
                msg = '失败，无法成功将指数的历史估值信息插入 aggregated_data数据库中的index_components_historical_estimations表' + '  ' + str(e)
                custom_logger.CustomLogger().log_writter(msg, 'error')



if __name__ == '__main__':
    go = CalculateIndexHistoricalEstimations()
    go.read_run_cal_index_his_estimation_file()

