import time
import sys
sys.path.append('..')
import target_pool.read_collect_target_fund as read_collect_target_fund
import strategy.fund_strategy_PE_estimation as fund_strategy_PE_estimation
import strategy.fund_strategy_PB_estimation as fund_strategy_PB_estimation

class NotificationScheduler:
    # 发送通知的任务调度器

    def __init__(self):
        pass

    def calculate_all_tracking_index_funds_today_PE_and_notificate(self,channel):
        # 计算所有指数基金的今天的市盈率TTM, 扣非市盈率TTM，并发送通知
        # param: channel 发送的渠道, 可填 email 或 sms

        # 获取标的池中跟踪关注指数及他们的中文名称
        # 字典形式。如，{'399396.XSHE': '国证食品', '000932.XSHG': '中证主要消费',,,,}
        indexes_and_their_names = read_collect_target_fund.ReadCollectTargetFund().get_indexes_and_their_names()

        # 获取当前日期
        today = time.strftime("%Y-%m-%d", time.localtime())

        # 指数与今天的市盈率TTM, 扣非市盈率TTM
        # 形式如：
        indexes_and_today_PE = dict()
        for index in indexes_and_their_names:
            # 获取 实时市盈率TTM
            #pe_ttm, pe_ttm_nonrecurring = fund_strategy_PE_estimation.FundStrategyPEEstimation().calculate_a_historical_date_index_PE(index[:-5], today)
            # indexes_and_today_PE[index] = (pe_ttm, pe_ttm_nonrecurring)
            #print(pe_ttm, pe_ttm_nonrecurring)
            pass


        if channel == "email":
            pass



if __name__ == '__main__':
    go = NotificationScheduler()
    go.calculate_all_tracking_index_funds_today_PE_and_notificate("email")

