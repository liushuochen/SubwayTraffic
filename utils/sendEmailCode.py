# coding:utf-8
import smtplib
from email.mime.text import MIMEText
from email.header import Header


def __init__(self, receivers):
    # 第三方 SMTP 服务

    self.mail_host = "smtp.qq.com"  # 设置服务器:这个是qq邮箱服务器，直接复制就可以
    self.mail_pass = "viczlpjpflqmbjcj"  # 刚才我们获取的授权码
    self.sender = 'gaoxiangyucc@qq.com'  # 你的邮箱地址
    self.receivers = [receivers]  # 收件人的邮箱地址，可设置为你的QQ邮箱或者其他邮箱，可多个


def send(self, vcode):
    header = 'SubwayTrafficAdmin' + '<' + self.sender + '>'
    content = '<html><h1>你的验证码是:' + vcode + '</html></h1>'
    message = MIMEText(content, 'html', 'utf-8')

    message['From'] = Header(header)

    subject = 'test1234'  # 发送的主题，可自由填写
    message['Subject'] = Header(subject, 'utf-8')
    try:
        smtpObj = smtplib.SMTP_SSL(self.mail_host, 465)
        smtpObj.login(self.sender, self.mail_pass)
        smtpObj.sendmail(self.sender, self.receivers, message.as_string())
        smtpObj.quit()
        print('邮件发送成功')
    except smtplib.SMTPException as e:
        print('邮件发送失败')
