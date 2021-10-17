# 基金标的池

# fund_code : 基金代码
# fund_name : 基金名称
# fund_type : 基金类型，股票指数，混合，股票，债券型，联接
# tracking_index_name : 跟踪指数名称， https://www.joinquant.com/help/api/help?name=index#%E4%B8%8A%E6%B5%B7%E5%B8%82%E5%9C%BA%E6%8C%87%E6%95%B0%E5%88%97%E8%A1%A8
# tracking_index_code : 跟踪指数代码， https://www.joinquant.com/help/api/help?name=index#%E4%B8%8A%E6%B5%B7%E5%B8%82%E5%9C%BA%E6%8C%87%E6%95%B0%E5%88%97%E8%A1%A8
# index_company: 指数开发公司
# hold_or_not :  当前是否持有,True为持有，False不持有
# valuation_method_list :  估值方法
# B&H_strategy_list : 买入持有策略
# sell_out_strategy_list :  卖出策略
# monitoring_frequency_list :  监控频率, daily, weekly, monthly, seasonly, yearly, periodically

target_index_funds = {
	'161725': {'fund_name': '招商中证白酒指数分级', 'fund_type': '股票指数', 'tracking_index_name': '中证白酒',
			   'tracking_index_code': '399997.XSHE', 'index_company': '中证', 'hold_or_not': True,
			   'valuation_method_list': ['pe'], 'B&H_strategy_list': [], 'sell_out_strategy_list': [],
			   'monitoring_frequency_list': ['daily']},

    '160222': {'fund_name': '国泰国证食品饮料行业指数', 'fund_type': '股票指数 ', 'tracking_index_name': '国证食品',
               'tracking_index_code': '399396.XSHE', 'index_company': '国证', 'hold_or_not': True,
               'valuation_method_list': ['pe'], 'B&H_strategy_list': [], 'sell_out_strategy_list': [],
               'monitoring_frequency_list': ['daily']},

    '159928': {'fund_name': '汇添富中证主要消费ETF', 'fund_type': '股票指数,ETF-场内', 'tracking_index_name': '中证主要消费',
               'tracking_index_code': '000932.XSHG', 'index_company': '中证', 'hold_or_not': True,
               'valuation_method_list': ['pe'], 'B&H_strategy_list': [], 'sell_out_strategy_list': [],
               'monitoring_frequency_list': ['daily']},

    '160628': {'fund_name': '鹏华地产分级', 'fund_type': '股票指数', 'tracking_index_name': '中证800地产',
               'tracking_index_code': '399965.XSHE', 'index_company': '中证', 'hold_or_not': True,
               'valuation_method_list': ['pb'], 'B&H_strategy_list': [], 'sell_out_strategy_list': [],
               'monitoring_frequency_list': ['daily']},

    '160517': {'fund_name': '博时中证银行指数(LOF)', 'fund_type': '股票指数', 'tracking_index_name': '中证银行指数',
               'tracking_index_code': '399986.XSHE', 'index_company': '中证', 'hold_or_not': True,
               'valuation_method_list': ['pb'], 'B&H_strategy_list': [], 'sell_out_strategy_list': [],
               'monitoring_frequency_list': ['daily']},

    '510630': {'fund_name': '华夏消费ETF', 'fund_type': '股票指数', 'tracking_index_name': '上证主要消费行业指数',
               'tracking_index_code': '000036.XSHG', 'index_company': '中证', 'hold_or_not': False,
               'valuation_method_list': ['pe'], 'B&H_strategy_list': [], 'sell_out_strategy_list': [],
               'monitoring_frequency_list': ['daily']}
}
