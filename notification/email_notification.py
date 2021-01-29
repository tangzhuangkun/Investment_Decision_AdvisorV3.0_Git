#! /usr/bin/env python3
#coding:utf-8
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import time

import sys
sys.path.append("..")
import config.notification_account as notification_account
import log.custom_logger as custom_logger

# todo 维护document

class EmailNotification:
	# 通过邮件发送提醒
	
	def __init__(self):
		# 设置发送邮件的参数
		# 设置服务器,第三方 SMTP 服务
		self.email_host = notification_account.email_host
		# 用户名
		self.email_user = notification_account.email_user
		# 获取授权码，不是密码
		self.email_pass = notification_account.email_pass
		# 发件人账号
		self.email_sender = notification_account.email_sender
		# 接收邮件
		self.email_receivers = notification_account.email_receivers
		# 获取当前时间
		self.today= time.strftime("%Y-%m-%d", time.localtime())
		# 设置邮件主题
		self.subject = self.today

	
	def send_customized_content(self, object, send_content):
		# 自定义邮件主题+内容
		# param: object, 邮件主题
		# param: send_content, 自定义的内容
		# 发送邮件
		
		# MIMEText 类来实现支持HTML格式的邮件，支持所有HTML格式的元素，包括表格，图片，动画，css样式，表单
		# 第一个参数为邮件内容,第二个设置文本格式，第三个设置编码
		message = MIMEText(send_content, 'plain', 'utf-8')  
		# 发件人
		message['From'] = self.email_sender  
		# 收件人
		message['To'] = ",".join(self.email_receivers)
		# 主题
		message['Subject'] = Header(self.subject + object, 'utf-8')
	
		try:
			# 创建实例
			smtpObj = smtplib.SMTP_SSL(self.email_host)
			# 连接服务器，25 为 SMTP 端口号
			smtpObj.ehlo(self.email_host)
			# 登录账号
			smtpObj.login(self.email_user, self.email_pass)
			# 发送邮件
			smtpObj.sendmail(self.email_sender, self.email_receivers, message.as_string())
			# 日志记录
			msg = '邮件发送成功'
			custom_logger.CustomLogger().log_writter(msg, 'info')
		except smtplib.SMTPException as e:
			# 日志记录
			msg = '无法发送邮件' + str(e)
			custom_logger.CustomLogger().log_writter(msg, 'error')
	
	
if __name__ == '__main__':
	time_start = time.time()
	go = EmailNotification()
	#real_time_pe = go.get_index_real_time_pe('399997')
	send_content = 'hello 2021-01-29  '
	go.send_customized_content(' 基金行情分析', send_content)
	time_end = time.time()
	print(time_end-time_start)
	