from apscheduler.schedulers.blocking import BlockingScheduler
import sys
sys.path.append('..')
import strategy.fund_strategy_PE_estimation as fund_strategy_PE_estimation
import log.custom_logger as custom_logger

class NotificationScheduler:
    # 发送通知的任务调度器

    def __init__(self):
        pass

    def notification_schedule_plan(self):
        # 调度器，根据时间安排工作
        scheduler = BlockingScheduler()

        #####################      每天运行    ###################################################

        #########  盘中  #########

        try:
            # 每个交易日14：49计算并发送指数的动态市盈率
            scheduler.add_job(func=fund_strategy_PE_estimation.FundStrategyPEEstimation().
                              calculate_all_tracking_index_funds_real_time_PE_and_notificate, args=('email',), trigger='cron',
                              month='1-12', day_of_week='mon,tue,wed,thu,fri', hour=14, minute=49,
                              id='weekdayCalRealTimeIndexPETTM')
        except Exception as e:
            # 抛错
            custom_logger.CustomLogger().log_writter(e, 'error')



        # 启动调度器
        try:
            scheduler.start()
        except (KeyboardInterrupt, SystemExit):
            pass



if __name__ == '__main__':
    go = NotificationScheduler()
    go.notification_schedule_plan()

