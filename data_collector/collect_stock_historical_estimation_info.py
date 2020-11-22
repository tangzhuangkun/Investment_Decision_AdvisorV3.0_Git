import requests
import json
import time

import sys

sys.path.append("..")
import database.db_operator as db_operator
import config.lxr_token as lxr_token
import log.custom_logger as custom_logger


class CollectStockHistoricalEstimationInfo:
    # 收集所需的股票的估值信息
    # PE-TTM :pe_ttm
    # PE-TTM(扣非) :d_pe_ttm
    # PB :pb
    # PS-TTM :ps_ttm
    # PCF-TTM :pcf_ttm
    # EV/EBIT :ev_ebit_r
    # 股票收益率 :ey
    # 股息率 :dyr
    # 股价 :sp
    # 成交量 :tv
    # 前复权 :fc_rights
    # 后复权 :bc_rights
    # 理杏仁前复权 :lxr_fc_rights
    # 股东人数 :shn
    # 市值 :mc
    # 流通市值 :cmc
    # 自由流通市值 :ecmc
    # 人均自由流通市值 :ecmc_psh
    # 融资余额 :fb
    # 融券余额 :sb
    # 陆股通持仓金额 :ha_shm

    # 运行频率：每天收盘后

    def __init__(self):
        pass

    def demanded_stocks(self):
        # 数据库中，哪些股票需要被收集估值信息
        # 输出： 需要被收集估值信息的股票代码和股票名称
        # 如 {'000568': '泸州老窖', '000596': '古井贡酒',,,,}
        selecting_sql = "SELECT DISTINCT stock_code, stock_name FROM index_constituent_stocks_weight"
        stock_codes_names = db_operator.DBOperator().select_all("financial_data", selecting_sql)
        # stock_codes_names 如  [{'stock_code': '000568', 'stock_name': '泸州老窖'}, {'stock_code': '000596', 'stock_name': '古井贡酒'},,, , , ]
        stock_codes_names_dict = dict()
        for piece in stock_codes_names:
            stock_codes_names_dict[piece["stock_code"]] = piece["stock_name"]
        return stock_codes_names_dict

    def get_lxr_token(self):
        # 随机获取一个理杏仁的token、
        # 输出：理杏仁的token
        return lxr_token.LXRToken().get_token()

    def collect_a_period_time_estimation(self, stock_code_name_dict, start_date, end_date):
        # 调取理杏仁接口，获取一段时间范围内，该股票估值数据, 并储存
        # param:  stock_code_name_dict 股票代码名称字典, 只能1支股票， 如  {"000568":"泸州老窖"}
        # param:  start_date, 开始时间，如 2020-11-12
        # param:  end_date, 结束时间，默认为空，如 2020-11-13
        # 输出： 将获取到股票估值数据存入数据库

        # 随机获取一个token
        token = self.get_lxr_token()
        # 理杏仁要求 在请求的headers里面设置Content-Type为application/json。
        headers = {'Content-Type': 'application/json'}
        # 理杏仁 获取基本面数据 接口
        url = 'https://open.lixinger.com/api/a/stock/fundamental/non_financial'
        # 接口参数，PE-TTM :pe_ttm
        # PE-TTM(扣非) :d_pe_ttm
        # PB :pb
        # PS-TTM :ps_ttm
        # PCF-TTM :pcf_ttm
        # EV/EBIT :ev_ebit_r
        # 股票收益率 :ey
        # 股息率 :dyr
        # 股价 :sp
        # 成交量 :tv
        # 前复权 :fc_rights
        # 后复权 :bc_rights
        # 理杏仁前复权 :lxr_fc_rights
        # 股东人数 :shn
        # 市值 :mc
        # 流通市值 :cmc
        # 自由流通市值 :ecmc
        # 人均自由流通市值 :ecmc_psh
        # 融资余额 :fb
        # 融券余额 :sb
        # 陆股通持仓金额 :ha_shm
        parms = {"token": token,
                 "startDate": start_date,
                 "endDate": end_date,
                 "stockCodes":
                     list(stock_code_name_dict.keys()),
                 "metricsList": [
                     "pe_ttm", "d_pe_ttm", "pb", "pb_wo_gw", "ps_ttm", "pcf_ttm", "ev_ebit_r", "ey", "dyr", "sp", "tv",
                     "fc_rights", "bc_rights", "lxr_fc_rights", "shn", "mc", "cmc", "ecmc", "ecmc_psh", "fb", "sb",
                     "ha_shm"
                 ]}
        values = json.dumps(parms)
        # 调用理杏仁接口
        req = requests.post(url, data=values, headers=headers)
        content = req.json()
        # content 如 {'code': 0, 'message': 'success', 'data': [{'date': '2020-11-13T00:00:00+08:00', 'pe_ttm': 48.04573277785343, 'd_pe_ttm': 47.83511443886097, 'pb': 14.42765025023379, 'pb_wo_gw': 14.42765025023379, 'ps_ttm': 22.564315310000808, 'pcf_ttm': 49.80250701327664, 'ev_ebit_r': 33.88432187818624, 'ey': 0.029323867066169462, 'dyr': 0.00998533724340176, 'sp': 1705, 'tv': 2815500, 'shn': 114300, 'mc': 2141817249000, 'cmc': 2141817249000, 'ecmc': 899670265725, 'ecmc_psh': 7871131, 'ha_shm': 173164289265, 'fb': 17366179363, 'sb': 2329851810, 'fc_rights': 1705, 'bc_rights': 1705, 'lxr_fc_rights': 1705, 'stockCode': '600519'}, {'date': '2020-11-12T00:00:00+08:00', 'pe_ttm': 48.88519458398379, 'd_pe_ttm': 48.67089629172529, 'pb': 14.679732186277464, 'pb_wo_gw': 14.679732186277464, 'ps_ttm': 22.95856220330575, 'pcf_ttm': 50.672663426136175, 'ev_ebit_r': 34.47543387050795, 'ey': 0.028824017925678805, 'dyr': 0.009813867960963575, 'sp': 1734.79, 'tv': 2347300, 'shn': 114300, 'mc': 2179239381462, 'cmc': 2179239381462, 'ecmc': 915389431248, 'ecmc_psh': 8008656, 'ha_shm': 176618263840, 'fb': 17207679699, 'sb': 2426239128, 'fc_rights': 1734.79, 'bc_rights': 1734.79, 'lxr_fc_rights': 1734.79, 'stockCode': '600519'}]}
        message = content['message']
        # 检查token是否失效
        if message == "illegal token.":
            # 日志记录失败
            msg = 'Failed to use token ' + token + ' ' + 'to collect_a_period_time_estimation of ' + \
                  str(stock_code_name_dict) + ' ' + start_date + ' ' + end_date
            custom_logger.CustomLogger().log_writter(msg, 'error')
            return self.collect_a_period_time_estimation(stock_code_name_dict, start_date, end_date)
        # 数据存入数据库
        self.save_content_into_db(content, stock_code_name_dict, "period")

    def collect_a_special_date_estimation(self, stock_codes_names_dict, date):
        # 调取理杏仁接口，获取特定一天，一只/多支股票估值数据, 并储存
        # param:  stock_codes_names_dict 股票代码名称字典, 可以多支股票， 如  {"000568":"泸州老窖", "000596":"古井贡酒",,,}
        # param:  date, 日期，如 2020-11-12
        # 输出： 将获取到股票估值数据存入数据库

        # 随机获取一个token
        token = self.get_lxr_token()
        # 理杏仁要求 在请求的headers里面设置Content-Type为application/json。
        headers = {'Content-Type': 'application/json'}
        # 理杏仁 获取基本面数据 接口
        url = 'https://open.lixinger.com/api/a/stock/fundamental/non_financial'
        # 接口参数，
        # PE-TTM :pe_ttm
        # PE-TTM(扣非) :d_pe_ttm
        # PB :pb
        # PS-TTM :ps_ttm
        # PCF-TTM :pcf_ttm
        # EV/EBIT :ev_ebit_r
        # 股票收益率 :ey
        # 股息率 :dyr
        # 股价 :sp
        # 成交量 :tv
        # 前复权 :fc_rights
        # 后复权 :bc_rights
        # 理杏仁前复权 :lxr_fc_rights
        # 股东人数 :shn
        # 市值 :mc
        # 流通市值 :cmc
        # 自由流通市值 :ecmc
        # 人均自由流通市值 :ecmc_psh
        # 融资余额 :fb
        # 融券余额 :sb
        # 陆股通持仓金额 :ha_shm
        parms = {"token": token,
                 "date": date,
                 "stockCodes":
                     list(stock_codes_names_dict.keys()),
                 "metricsList": [
                     "pe_ttm", "d_pe_ttm", "pb", "pb_wo_gw", "ps_ttm", "pcf_ttm", "ev_ebit_r", "ey", "dyr", "sp", "tv",
                     "fc_rights", "bc_rights", "lxr_fc_rights", "shn", "mc", "cmc", "ecmc", "ecmc_psh", "fb", "sb",
                     "ha_shm"
                 ]}
        values = json.dumps(parms)
        req = requests.post(url, data=values, headers=headers)
        content = req.json()
        # content 如 {'code': 0, 'message': 'success', 'data': [
        # {'date': '2020-11-13T00:00:00+08:00', 'pe_ttm': 48.2957825939533, 'd_pe_ttm': 48.62280236330014, 'pb': 12.491374104141297, 'pb_wo_gw': 12.491374104141297, 'ps_ttm': 17.156305422424143, 'pcf_ttm': 63.68585789882434, 'ev_ebit_r': 37.63760421342357, 'ey': 0.026088654822125818, 'dyr': 0.0085167925205312, 'sp': 186.69, 'tv': 13479800, 'shn': 113900, 'mc': 273454640491.19998, 'cmc': 273371391686, 'ecmc': 133902847844, 'ecmc_psh': 1175618, 'ha_shm': 5559655830, 'fc_rights': 186.69, 'bc_rights': 186.69, 'lxr_fc_rights': 186.69, 'stockCode': '000568'}, {'date': '2020-11-13T00:00:00+08:00', 'pe_ttm': 60.72940789130697, 'd_pe_ttm': 64.53258136924804, 'pb': 11.823197225442007, 'pb_wo_gw': 12.43465627328832, 'ps_ttm': 11.182674688897702, 'pcf_ttm': 216.59317739098543, 'ev_ebit_r': 48.032852603259784, 'ey': 0.02045252811485187, 'dyr': 0.006568863586599518, 'sp': 228.35, 'tv': 3310800, 'shn': 31900, 'mc': 114997060000, 'cmc': 87595060000, 'ecmc': 25619951576, 'ecmc_psh': 803133, 'ha_shm': 1181857851, 'fc_rights': 228.35, 'bc_rights': 228.35, 'lxr_fc_rights': 228.35, 'stockCode': '000596'}]}
        # 检查token是否失效
        if content['message'] == "illegal token.":
            # 日志记录失败
            msg = 'Failed to use token ' + token + ' ' + 'to collect_a_special_date_estimation of ' + \
                  str(stock_codes_names_dict) + ' ' + date
            custom_logger.CustomLogger().log_writter(msg, 'error')
            return self.collect_a_special_date_estimation(stock_codes_names_dict, date)
        # 数据存入数据库
        self.save_content_into_db(content, stock_codes_names_dict, "date")

    def save_content_into_db(self, content, stock_codes_names_dict, range):
        # 将 理杏仁接口返回的数据 存入数据库
        # param:  content, 理杏仁接口返回的数据
        # param:  stock_codes_names_dict 股票代码名称字典, 可以1支/多支股票， 如  {"000568":"泸州老窖", "000596":"古井贡酒",,,}
        # param： range， 时间范围，只能填 period 或者 date

        # 解析返回的数据
        for piece in content["data"]:
            stock_code = piece['stockCode']
            stock_name = stock_codes_names_dict[stock_code]
            date = piece['date'][:10]

            # 检查记录是否已在数据库中存在
            is_data_existing = self.is_existing(stock_code, stock_name, date)
            # 如果已存在，且获取的是，一只股在一段时间内的估值数据，则循环截止,不需要收集这一天和往前日期的数据
            if is_data_existing and range=="period":
                # 日志记录
                msg = date + " "+stock_code + " "+ stock_name+ '\'s info has already existed, there is no need to save it and the previous date again. '
                custom_logger.CustomLogger().log_writter(msg, 'info')
                break
            # 如果已存在，且获取的是，一/多只股在特定日期的估值数据，则停止收集该只数据，切换至下一个
            elif is_data_existing and range=="date":
                # 日志记录
                msg = date + " " + stock_code + " " + stock_name + '\'s info has already existed, there is no need to save it again. '
                custom_logger.CustomLogger().log_writter(msg, 'info')
                continue

            # 如果获取不到值，则置为0，避免出现 keyerror
            pe_ttm = piece.setdefault('pe_ttm', 0)
            pe_ttm_nonrecurring = piece.setdefault('d_pe_ttm', 0)
            pb = piece.setdefault('pb', 0)
            pb_wo_gw = piece.setdefault('pb_wo_gw', 0)
            ps_ttm = piece.setdefault('ps_ttm', 0)
            pcf_ttm = piece.setdefault('pcf_ttm', 0)
            ev_ebit = piece.setdefault('ev_ebit_r', 0)
            stock_yield = piece.setdefault('ey', 0)
            dividend_yield = piece.setdefault('dyr', 0)
            share_price = piece.setdefault('sp', 0)
            turnover = piece.setdefault('tv', 0)
            fc_rights = piece.setdefault('fc_rights', 0)
            bc_rights = piece.setdefault('bc_rights', 0)
            lxr_fc_rights = piece.setdefault('lxr_fc_rights', 0)
            shareholders = piece.setdefault('shn', 0)
            market_capitalization = piece.setdefault('mc', 0)
            circulation_market_capitalization = piece.setdefault('cmc', 0)
            free_circulation_market_capitalization = piece.setdefault('ecmc', 0)
            free_circulation_market_capitalization_per_capita = piece.setdefault('ecmc_psh', 0)
            financing_balance = piece.setdefault('fb', 0)
            securities_balances = piece.setdefault('sb', 0)
            stock_connect_holding_amount = piece.setdefault('ha_shm', 0)

            # 存入数据库
            inserting_sql = "INSERT INTO stocks_main_estimation_indexes_historical_data (stock_code, stock_name, date, pe_ttm,pe_ttm_nonrecurring,pb,pb_wo_gw,ps_ttm,pcf_ttm,ev_ebit,stock_yield,dividend_yield,share_price,turnover,fc_rights,bc_rights,lxr_fc_rights,shareholders,market_capitalization,circulation_market_capitalization,free_circulation_market_capitalization,free_circulation_market_capitalization_per_capita,financing_balance,securities_balances,stock_connect_holding_amount ) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s' )" % (
            stock_code, stock_name, date, pe_ttm, pe_ttm_nonrecurring, pb, pb_wo_gw, ps_ttm, pcf_ttm, ev_ebit,
            stock_yield, dividend_yield, share_price, turnover, fc_rights, bc_rights, lxr_fc_rights, shareholders,
            market_capitalization, circulation_market_capitalization, free_circulation_market_capitalization,
            free_circulation_market_capitalization_per_capita, financing_balance, securities_balances,
            stock_connect_holding_amount)
            db_operator.DBOperator().operate("insert", "financial_data", inserting_sql)

        # 日志记录
        msg = str(stock_codes_names_dict) + '\'s estimation info has been saved '
        custom_logger.CustomLogger().log_writter(msg, 'info')

    def is_existing(self, stock_code, stock_name, date):
        # 检查数据库中是否有记录，主要是检查是否为同一支股票同一日期
        # param: stock_code, 股票代码
        # param: stock_name，股票名称
        # param: date，日期
        # 输出：True，已存在； False，无记录

        selecting_sql = "SELECT pe_ttm FROM stocks_main_estimation_indexes_historical_data where stock_code = '%s' and stock_name = '%s' and date = '%s' " % (stock_code, stock_name, date)
        existing = db_operator.DBOperator().select_one("financial_data", selecting_sql)

        # 如果查询结果为None，则说明不存在；否则，说明有记录
        if existing == None:
            return False
        else:
            return True

    def collect_all_new_stocks_info_at_one_time(self, start_date, stock_codes_names_dict):
        # 将所有新的，且需要被收集估值信息的股票，一次性收集数据
        # param: start_date, 起始日期，默认 2010-01-02
        # param: stock_codes_names_dict 股票代码名称字典, 可以1支/多支股票， 如  {"000568":"泸州老窖", "000596":"古井贡酒",,,}

        # 获取当前时间
        today = time.strftime("%Y-%m-%d", time.localtime())
        # 遍历股票
        for k, v in stock_codes_names_dict.items():
            piece_dict = {k: v}
            # 收集单只股票，从2010-01-01至今的估值数据
            self.collect_a_period_time_estimation(piece_dict, start_date, today)

    def collect_stocks_recent_info(self, stock_codes_names_dict):
        # 收集当前所有股票最近的信息

        # 获取当前时间
        today = time.strftime("%Y-%m-%d", time.localtime())
        # 收集数据库中所有股票，今日的估值数据
        self.collect_a_special_date_estimation(stock_codes_names_dict, today)

    def main(self,start_date):
        # 与上次数据库中待收集的股票代码和名称对比，
        # 并决定是 同时收集多只股票特定日期的数据 还是 分多次收集个股票一段时间的数据

        # 当前数据库中，待收集的股票代码和名称
        stock_codes_names_dict = self.demanded_stocks()

        last_time_data = None
        with open("comparison.json", "r", encoding="utf-8") as com:
            last_time_data = json.load(com)

        # 如果待收集的内容与上次数据库中的一致
        # 则只收集最近日期的

        if stock_codes_names_dict == last_time_data["last_time_stock_codes_names_in_db_dict"]:
            self.collect_stocks_recent_info(stock_codes_names_dict)
        # 如果不相同，一次性收集所有数据
        else:
            self.collect_all_new_stocks_info_at_one_time(start_date, stock_codes_names_dict)
            # 更新comparison文件中的记录
            with open("comparison.json", "w", encoding="utf-8") as com:
                com.truncate()
                new_data = dict()
                new_data["last_time_stock_codes_names_in_db_dict"] = stock_codes_names_dict
                com.write(json.dumps(new_data, ensure_ascii=False))
            # 日志记录
            msg = 'Update comparison.json content '
            custom_logger.CustomLogger().log_writter(msg, 'info')

if __name__ == "__main__":
    go = CollectStockHistoricalEstimationInfo()
    # stock_codes_names_dict = go.demanded_stocks()
    # print(stock_codes_names_dict)
    #go.collect_a_period_time_estimation({"600519":"贵州茅台"}, "2020-11-04", "2020-11-05")
    #go.collect_a_special_date_estimation({"000568":"泸州老窖", "000596":"古井贡酒"}, "2020-11-09")
    # print(content)
    #go.collect_all_new_stocks_info_at_one_time()
    #result = go.is_existing("000568", "泸州老窖", "2020-11-19")
    #print(result)
    go.main("2010-01-02")
