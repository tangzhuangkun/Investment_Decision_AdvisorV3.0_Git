from apscheduler.schedulers.blocking import BlockingScheduler
import sys
sys.path.append('..')
import strategy.fund_strategy_PE_estimation as fund_strategy_PE_estimation
import log.custom_logger as custom_logger
import notification.email_notification as email_notification

class NotificationPlan:
    # 发送通知计划

    def __init__(self):
        pass

    def estimation_notification(self):
        # 估值信息, 邮件通知

        # 计算指数的动态市盈率
        indexes_and_real_time_PE_msg = fund_strategy_PE_estimation.FundStrategyPEEstimation().calculate_all_tracking_index_funds_real_time_PE_and_generate_msg()

        # 估值信息汇总
        estimation_msg = indexes_and_real_time_PE_msg

        # 邮件发送所有估值信息
        try:
            email_notification.EmailNotification().send_customized_content(' 指数基金估值数据', estimation_msg)
            # 日志记录
            log_msg = '指数基金估值信息，邮件发送成功'
            custom_logger.CustomLogger().log_writter(log_msg, 'info')
        except Exception as e:
            # 日志记录
            log_msg = '指数基金估值信息，邮件发送失败'+str(e)
            custom_logger.CustomLogger().log_writter(log_msg, 'error')




if __name__ == '__main__':
    go = NotificationPlan()
    go.estimation_notification()

