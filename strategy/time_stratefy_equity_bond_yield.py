

class TimeStrategyEquityBondYield:
    # 择时策略，股债收益率
    # 沪深全A股PE/十年国债收益率
    # 用于判断股市收益率与无风险收益之间的比值
    # 频率：每个交易日，盘中

    def __init__(self):
        pass


    '''
    steps
    1、收集政府债券利率历史数据，1年，3年，5年，10年期利率， done
    2、收集沪深300 历史市盈率, done
    3、收集沪深300成分股,done
    4、盘中，采集沪深300实时市盈率，并汇总
    5、盘中，采集债券实时利率
    6、盘中，通知实时股债比
    7、盘后，更新股债比
    '''


    # 来自中国外汇交易接口
    # 政府债券利率历史数据，一年期，十年期利率
    # http: // www.chinamoney.com.cn / ags / ms / cm - u - bk - currency / SddsIntrRateGovYldHis?lang = CN & startDate = 2020 - 10 - 24 & endDate = 2021 - 10 - 23 & pageNum = 1 & pageSize = 1000

    # 来自中国债券信息网接口
    # 十年期国债利率
    # https://yield.chinabond.com.cn/cbweb-mn/yc/queryYz?bjlx=no&&dcq=10,10y;&&startTime=2010-01-01&&endTime=2021-10-23&&qxlx=0,&&yqqxN=N&&yqqxK=K&&par=day&&ycDefIds=2c9081e50a2f9606010a3068cae70001,&&locale=zh_CN


    # 理杏仁-指数接口-基本面
    # 1000002 沪深A股
    # 0000300 沪深300
    '''
    {
        "token": "1ffe5978-c6a8-4273-8607-2f34eaeb4c42",
        "startDate": "2021-11-01",
        "endDate": "2021-11-03",
        "stockCodes": [
            "000300"
        ],
        "metricsList": [
            "pe_ttm.mcw",
            "pe_ttm.ew",
            "pe_ttm.ewpvo",
            "pe_ttm.avg",
            "pe_ttm.median"
        ]
    }
    
    '''



    # 股债比大于3，
    # 处于历史百分位，如果低于8%，反复提醒