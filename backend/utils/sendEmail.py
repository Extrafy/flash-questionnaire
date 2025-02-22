from config import settings

from User.models import ConfirmString
from utils.toHash import *

import datetime

def make_confirm_string(user):  # generate confirm_code for user (username+c_time)
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    code = hash_code(user.username, now)
    ConfirmString.objects.create(code=code, user=user,)
    return code

def send_email_confirm(email, code):
    from django.core.mail import EmailMultiAlternatives
    subject = '来自yangyang的注册确认邮件'
    text_content = '''感谢注册QN，这里是软工冲冲冲，专注于管理与发布问卷！\
                    如果你看到这条消息，说明你的邮箱服务器不提供HTML链接功能，请联系管理员！'''
    html_content = '''
                    <p>感谢注册QN，这里是软工冲冲冲，专注于管理与发布问卷！</p>
                    <p>请根据验证码：{}完成注册确认！</p>
                    <p>此链接有效期为{}天！</p>
                    '''.format( code, settings.CONFIRM_DAYS)   # url must be corrected
    msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, [email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()



def send_email_change_confirm(email, code):

    from django.core.mail import EmailMultiAlternatives

    subject = '来自yangyang的邮箱确认邮件'

    text_content = '''感谢使用QN，这里是软工冲冲冲，专注于管理与发布问卷！\
                    您的邮箱验证码为 {}\
                    验证码有效期为{}天'''.format(code, settings.CONFIRM_DAYS)

    html_content = '''
                    <p>感谢使用QN,这里是问卷星球，专注于管理与发布问卷！</p>
                    <p>您的邮箱验证码为 {}</p>
                    <p>验证码有效期为{}天！</p>
                    '''.format(code, settings.CONFIRM_DAYS)   # url must be corrected

    msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, [email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
