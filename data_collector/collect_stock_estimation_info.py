import requests
import json
import time

import sys
sys.path.append("..")
import database.db_operator as db_operator
import config.lxr_token as lxr_token
import log.custom_logger as custom_logger


class CollectStockEstimationInfo:
    # 收集所需的股票的估值信息

    def __init__(self):
        pass

    def demanded_stocks(self):
        # 数据库中，哪些股票需要被收集估值信息
        # 输出： 需要被收集估值信息的股票代码和股票名称
        # 如 [{'stock_code': '000568', 'stock_name': '泸州老窖'}, {'stock_code': '000596', 'stock_name': '古井贡酒'},,,,,]
        selecting_sql = "SELECT DISTINCT stock_code, stock_name FROM index_constituent_stocks_weight"
        stock_code_name = db_operator.DBOperator().select_all("financial_data", selecting_sql)
        return stock_code_name

    def get_lxr_token(self):
        # 随机获取一个理杏仁的token、
        # 输出：理杏仁的token
        return lxr_token.LXRToken().get_token()


    def collect_a_period_time_estimation(self, stock_code_name_dict, start_date, end_date):
        # 调取理杏仁接口，获取一段时间范围内，该股票估值数据, 并储存
        # param:  stock_code_name_dict 股票代码名称字典, 只能1支股票， 如  {"000568":"泸州老窖"}
        # param:  start_date, 开始时间，如 2020-11-12
        # param:  end_date, 结束时间，默认为空，如 2020-11-13
        # 输出： 获取到股票估值数据

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
        message = content['message']
        # 检查token是否失效
        if message == "illegal token.":
            # 日志记录
            msg = 'Failed to use token ' + token + ' ' + 'to collect_a_period_time_estimation of ' + \
                  str(stock_code_name_dict) + ' ' + start_date + ' ' + end_date
            custom_logger.CustomLogger().log_writter(msg, 'error')
            return self.collect_a_period_time_estimation(stock_code_name_dict, start_date, end_date)
        return content





    def collect_a_special_date_estimation(self, stock_codes_names_dict, date):
        # 调取理杏仁接口，获取特定一天，一只/多支股票估值数据, 并储存
        # param:  stock_codes_names_dict 股票代码名称字典, 可以多支股票， 如  {"000568":"泸州老窖", "000596":"古井贡酒",,,}
        # param:  date, 日期，如 2020-11-12
        # 输出： 获取到股票估值数据
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
        # 检查token是否失效
        if content['message'] == "illegal token.":
            # 日志记录
            msg = 'Failed to use token ' + token + ' ' + 'to collect_a_special_date_estimation of ' + \
                  str(stock_codes_names_dict) + ' ' + date
            custom_logger.CustomLogger().log_writter(msg, 'error')
            return self.collect_a_special_date_estimation(stock_codes_names_dict, date)
        return content



    def save_content_into_db(self, content, stock_codes_names_dict):
        # 将 理杏仁接口返回的数据 存入数据库
        # param:  content, 理杏仁接口返回的数据
        # param:  stock_codes_names_dict 股票代码名称字典, 可以1支/多支股票， 如  {"000568":"泸州老窖", "000596":"古井贡酒",,,}



        pass


if __name__ == "__main__":
    go = CollectStockEstimationInfo()
    #go.demanded_stocks()
    content = go.collect_a_period_time_estimation({"600519":"贵州茅台"}, "2020-11-12", "2020-11-13")
    #content = go.collect_a_special_date_estimation({"000568":"泸州老窖", "000596":"古井贡酒"}, "2020-11-13")
    print(content)
