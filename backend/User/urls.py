from django.urls import path
from .views import *


urlpatterns = [
    path('login', login),#登录
    path('register', register),#注册
    path('logout', logout),#登出
    path('confirm/email', user_confirm),#邮箱验证
    path('send_verify_email', send_unverified_email),#重复邮箱验证
    path('find_password_back_FirstStep',find_password_back_FS),#找回密码第一步
    path('find_password_back_SecondStep',find_password_back_SE),#找回密码第二步
    path('change/username',change_username),#修改用户名
    path('change/email_FS', change_email_FS),#更改邮箱第一步
    path('change/email_SE', change_email_SE),#更改邮箱第二步
    path('change/picture',change_picture),#修改用户头像
    path('fk',get_authkey),

    # path('change/password', change_password),
    # path('send/code', send_code),
    # path('get/userinfo', get_userinfo),
    # path('confirm/userinfo', confirm_userinfo),
]