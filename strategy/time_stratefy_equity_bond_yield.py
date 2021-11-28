import time
import sys
sys.path.append("..")
import database.db_operator as db_operator
import log.custom_logger as custom_logger
import data_collector.collect_chn_gov_bonds_rates as collect_chn_gov_bonds_rates
import data_collector.collect_index_estimation_from_lxr as collect_index_estimation_from_lxr

class TimeStrategyEquityBondYield:
    # 择时策略，股债收益率
    # 沪深全A股PE/十年国债收益率
    # 用于判断股市收益率与无风险收益之间的比值
    # 频率：每个交易日，盘后

    def __init__(self):
        pass

    def prepare_index_estimation_and_bond_rate(self):
        # 准备数据，收集最新沪深300指数市值加权估值和国债利率

        # 收集最新国债收益率
        collect_chn_gov_bonds_rates.CollectCHNGovBondsRates().main()
        # 收集最新沪深300指数市值加权估值
        collect_index_estimation_from_lxr.CollectIndexEstimationFromLXR().main()


    def truncate_table(self):
        # 清空已计算好的股债比信息表
        # 插入数据之前，先进行清空操作
        truncating_sql = 'truncate table aggregated_data.stock_bond_ratio_di'

        try:
            db_operator.DBOperator().operate("update", "aggregated_data", truncating_sql)

        except Exception as e:
            # 日志记录
            msg = '失败，无法清空 aggregated_data数据库中的stock_bond_ratio_di表' + '  ' + str(e)
            custom_logger.CustomLogger().log_writter(msg, 'error')


    def run_sql_script_and_cal_ratio(self):
        # 运行mysql脚本以计算股债收益比

        # 相对路径，是相对于程序执行命令所在的目录，./ 表示的不是脚本所在的目录，而是程序执行命令所在的目录，也就是所谓的当前目录。
        with open("../data_miner/cal_stock_bond_ratio.sql", encoding='utf-8', mode='r') as script_f:
            # 分割sql文件中的执行语句，挨句执行
            sql_list = script_f.read().split(';')[:-1]
            for x in sql_list:
                # 判断包含空行的
                if '\n' in x:
                    # 替换空行为1个空格
                    x = x.replace('\n', ' ')

                # 判断多个空格时
                if '    ' in x:
                    # 替换为空
                    x = x.replace('    ', '')

                # sql语句添加分号结尾
                inserting_sql = x + ';'

                try:
                    db_operator.DBOperator().operate("insert", "financial_data", inserting_sql)

                except Exception as e:
                    # 日志记录
                    msg = '失败，无法成功运行mysql脚本以计算股债收益比' + '  ' + str(e)
                    custom_logger.CustomLogger().log_writter(msg, 'error')

    def cal_the_ratio_percentile_in_history(self):
        # 计算当前日期市盈率，10年期国债收益率，股债比，及历史百分位
        # 返回：如 {'trading_date': '2021-11-26', 'pe': Decimal('13.0141'), 'bond': Decimal('2.8200'), 'ratio': Decimal('2.7248'), 'percent': 74.47}

        # 获取当前日期
        # today = time.strftime("%Y-%m-%d", time.localtime())
        today = "2021-11-26"

        # 返回的字典
        today_info_dict = {}

        # 获取 交易日期和对应的股债比，按股债比从大到小排列
        selecting_sql = 'select trading_date, round(pe,4) as pe, round(10y_bond_rate*100,4) as bond, round(ratio,4) as ' \
                        'ratio from stock_bond_ratio_di order by ratio'
        trading_date_and_ratio_list = db_operator.DBOperator().select_all( "aggregated_data", selecting_sql)

        # 有多长的时间
        date_counter = len(trading_date_and_ratio_list)

        for i in range(len(trading_date_and_ratio_list)):
            # 日期与今天一致
            # 股债比，及历史百分位 均只保留4位小数
            if str(trading_date_and_ratio_list[i]["trading_date"]) == today:
                # 返回中存入今天日期
                today_info_dict["trading_date"] = today
                # 返回中存入今天沪深300的市盈率
                today_info_dict["pe"] = trading_date_and_ratio_list[i]["pe"]
                # 返回中存入今天国债收益率
                today_info_dict["bond"] = trading_date_and_ratio_list[i]["bond"]
                # 返回中存入今天股债收益比
                today_info_dict["ratio"] = trading_date_and_ratio_list[i]["ratio"]

                # 返回中存入所处历史百分位
                # 处于历史最大值
                if(i==date_counter-1):
                    today_info_dict["percent"] = 1
                # 处于历史极小值
                elif (i==0):
                    today_info_dict["percent"] = 0
                # 处于中间某个值
                else:
                    today_info_dict["percent"] = round(i / date_counter,4)*100
                return today_info_dict

    def generate_strategy_msg(self):
        # 生成通知信息
        '''
        返回：
        2021-11-26:
        股债比: 2.7248
        自2010年百分位: 74.47%
        沪深300市盈率: 13.0141
        国债收益率: 2.8200
        '''

        # 今天市盈率，10年期国债收益率，股债比，及历史百分位信息
        # {'trading_date': '2021-11-26', 'pe': Decimal('13.0141'), 'bond': Decimal('2.8200'), 'ratio': Decimal('2.7248'), 'percent': 0.7447}
        today_info_dict = self.cal_the_ratio_percentile_in_history()

        msg = ''
        # 如果股债收益比大于等于3 或者 大于等于历史百分位94
        if today_info_dict['ratio'] >= 3 or today_info_dict['percent']>=94:
            msg += "需特别注意，已进入重点投资区间\n\n"
        msg += today_info_dict['trading_date'] + ': \n'
        msg += '股债比: ' + str(today_info_dict['ratio']) + '\n'
        msg += '自2010年百分位: ' + str(today_info_dict['percent'])+'%' + '\n'
        msg += '沪深300市盈率: ' + str(today_info_dict['pe']) + '\n'
        msg += '国债收益率: ' + str(today_info_dict['bond']) + '\n'
        return msg

    def main(self):
        self.prepare_index_estimation_and_bond_rate()
        self.truncate_table()
        self.run_sql_script_and_cal_ratio()
        self.generate_strategy_msg()


    # 股债比大于3，
    # 处于历史百分位，如果低于8%，反复提醒


if __name__ == '__main__':
    time_start = time.time()
    go = TimeStrategyEquityBondYield()
    #go.main()
    go.generate_strategy_msg()
    time_end = time.time()
    print('Time Cost: ' + str(time_end - time_start))