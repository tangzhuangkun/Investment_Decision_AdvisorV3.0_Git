import requests
import time

import sys
sys.path.append("..")
import config.notification_account as notification_account
import log.custom_logger as custom_logger

class WechatNotification:
    # 通过虾推啥发送微信通知

    def __init__(self):
        pass


    def push_customized_content(self, token, object, send_content):
        # 自定义微信推送主题+内容，仅推送给特定的人
        # param: token, 虾推啥的token
        # param: object, 邮件主题
        # param: send_content, 自定义的内容
        # 发送微信推送

        # 虾推啥的
        wechat_push = {
            'text': object,
            'desp': send_content
        }

        try:
            # 调用接口发送推送
            requests.post('http://wx.xtuis.cn/'+token+'.send', data=wechat_push)
            # 日志记录
            log_msg = '成功, 向' +token+' 微信推送成功'
            custom_logger.CustomLogger().log_writter(log_msg, 'info')
        except Exception as e:
            # 日志记录
            log_msg = '失败, 微信推送失败' + wechat_push['text'] + '  '+ wechat_push['desp']+ str(e)
            custom_logger.CustomLogger().log_writter(log_msg, 'error')

    def push_to_all(self, object, send_content):
        # 将自定义内容微信推送给所有人
        # param: object, 邮件主题
        # param: send_content, 自定义的内容

        # 获取虾推啥token，决定需要推送给哪些人
        tokens = notification_account.xtuis_tokens
        # 获取当前时间
        today = time.strftime("%Y-%m-%d", time.localtime())

        # 推送给所有人
        for token in tokens:
            self.push_customized_content(token, today+object, send_content)


if __name__ == '__main__':
    time_start = time.time()
    go = WechatNotification()
    # 获取当前时间
    today = time.strftime("%Y-%m-%d", time.localtime())
    go.push_to_all(' 基金行情分析test', 'good night FC')
    time_end = time.time()
    print(time_end-time_start)