

class FundStrategyPEGEstimation:
    # 指数基金策略，PEG指标(市盈率相对盈利增长比率)
    # 用于衡量行业的估值与成长性
    # 频率：每个交易日，盘中

    def __init__(self):
        pass

    # 通过 joinquant get_fundamentals() 接口获取 净利润同比增长率，净利润环比增长率

    # 通过joinquant接口  get_factor_effect(security, start_date, end_date, period, factor, group_num=5) 获取PEG 因子