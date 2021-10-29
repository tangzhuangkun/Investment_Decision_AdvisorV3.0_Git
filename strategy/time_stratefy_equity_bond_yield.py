

class TimeStrategyEquityBondYield:
    # 择时策略，股债收益率
    # 沪深全A股PE/十年国债收益率
    # 用于判断股市收益率与无风险收益之间的比值
    # 频率：每个交易日，盘中

    def __init__(self):
        pass

    # 来自中国外汇交易接口
    # 政府债券利率历史数据，一年期，十年期利率
    # http: // www.chinamoney.com.cn / ags / ms / cm - u - bk - currency / SddsIntrRateGovYldHis?lang = CN & startDate = 2020 - 10 - 24 & endDate = 2021 - 10 - 23 & pageNum = 1 & pageSize = 1000

    # 来自中国债券信息网接口
    # 十年期国债利率
    # https://yield.chinabond.com.cn/cbweb-mn/yc/queryYz?bjlx=no&&dcq=10,10y;&&startTime=2010-01-01&&endTime=2021-10-23&&qxlx=0,&&yqqxN=N&&yqqxK=K&&par=day&&ycDefIds=2c9081e50a2f9606010a3068cae70001,&&locale=zh_CN


    # 理杏仁-指数接口-基本面
    # 1000002 沪深A股