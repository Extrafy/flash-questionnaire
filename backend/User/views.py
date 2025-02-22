import random
import json
import time
import uuid

#####
from django.conf import settings
from django.http import JsonResponse
import re
import datetime
import pytz
import base64
from User.RSA.code import *
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view

from User.models import ConfirmString,User
from utils.sendEmail import *

from .form import *

utc = pytz.UTC


# Create your views here.
@csrf_exempt
@api_view(['POST'])
def get_authkey(request):
    print("222")
    if request.method == 'POST':
        print("dddd")
        try:
            # 获取前端传来的 JSON 数据
            print("123")
            data = request.data
            print(data)
            current_timestamp = int(time.time() * 1000)
            data['timestamp'] = current_timestamp
            data['nonce'] = 'str(uuid.uuid4())'
            json_data = json.dumps(data)
            print(json_data)
            # current_timestamp = int(time.time() * 1000)
            # json_data['timestamp'] = current_timestamp
            # json_data['nonce'] = 'str(uuid.uuid4())'
            # 使用私钥对 JSON 数据进行签名（即加密）
            signature = rsa_encrypt(json_data)
            # 返回加密后的 authkey 和原始数据给前端
            return JsonResponse({'authkey': signature})
        except Exception as e:
            return JsonResponse({'error': e}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)


@csrf_exempt
@api_view(['POST'])
def login(request):#登录
    # request.session.flush()
    print(request.session.get('username'))
    if request.session.get('is_login'):  # login repeatedly not allowed
        return JsonResponse({'status_code': 2})

    login_form = LoginForm(request.POST)
    if login_form.is_valid():
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username)
        try:
            user = User.objects.get(username=username)
        except:
            return JsonResponse({'status_code': 3})
        print("444")
        if user.password == hash_code(password):
            if not user.has_confirmed:
                print("411")
                return JsonResponse({'status_code': 5})
            request.session['is_login'] = True
            request.session['username'] = username
            # print(request.session['is_login'])
            # print(username + " 登录成功")
            # print(request.session.get('username'))
            return JsonResponse({'status_code': 1, 'username': username,'email': user.email,'picture_url': user.url,'Flash_coin': user.Flash_coin})
        else:
            return JsonResponse({'status_code': 4})

    return JsonResponse({'status_code': -1})


@csrf_exempt
def register(request):#注册
    register_form = RegisterForm(request.POST)

    if register_form.is_valid():
        username = register_form.cleaned_data.get('username')
        password1 = register_form.cleaned_data.get('password1')
        password2 = register_form.cleaned_data.get('password2')
        email = register_form.cleaned_data.get('email')

        same_name_user = User.objects.filter(username=username)
        if same_name_user:
            return JsonResponse({'status_code': 2})

        same_email_user = User.objects.filter(email=email)
        if same_email_user:
            return JsonResponse({'status_code': 3})

        # 检测密码不符合规范：8-18，英文字母+数字
        if not re.match('^(?![0-9]+$)(?![a-zA-Z]+$)[0-9A-Za-z]{8,18}$', password1):
            return JsonResponse({'status_code': 4})

        if password1 != password2:
            return JsonResponse({'status_code': 5})

        # 成功
        new_user = User()
        new_user.username = username
        new_user.password = hash_code(password1)
        new_user.email = email
        new_user.save()

        # request.session['is_login'] = True
        # request.session['username'] = username

        code = make_confirm_string(new_user)
        try:
            send_email_confirm(email, code)#发送验证码
        except:
            new_user.delete()
            return JsonResponse({'status_code': 6})

        return JsonResponse({'status_code': 1})

    else:
        return JsonResponse({'status_code': -1})


@csrf_exempt
def logout(request):#登出
    if not request.session.get('is_login', None):
        return JsonResponse({'status_code': 401})

    print(request.session.get('is_login'))

    request.session.flush()
    return JsonResponse({'status_code': 200})


@csrf_exempt
def user_confirm(request):#确认邮箱的验证码
    if request.method == 'POST':
        code = request.POST.get('code')  # get code from url (?code=..)
        try:
            confirm = ConfirmString.objects.get(code=code)
        except:
            return JsonResponse({'status_code': 2})

        c_time = confirm.c_time.replace(tzinfo=utc)
        now = datetime.datetime.now().replace(tzinfo=utc)
        if now > c_time + datetime.timedelta(settings.CONFIRM_DAYS):
            confirm.user.delete()
            return JsonResponse({'status_code': 3})
        else:
            confirm.user.has_confirmed = True
            confirm.user.save()
            confirm.delete()
            return JsonResponse({'status_code': 1})


@csrf_exempt
def send_unverified_email(request):#第一次验证失败，进行重新验证
    try:
        this_user = User.objects.get(username=request.session['username'])
    except:
        return JsonResponse({'status_code': 2})

    if this_user.has_confirmed:
        return JsonResponse({'status_code': 3})

    try:
        code = ConfirmString.objects.get(user_id=this_user.id).code
        send_email_confirm(this_user.email, code)
    except:
        this_user.delete()
        return JsonResponse({'status_code': 4})
    return JsonResponse({'status_code': 1})


@csrf_exempt
def find_password_back_FS(request):
    if request.method == 'POST':
        password_form = FindPasswordBackForm_FS(request.POST)
        if password_form.is_valid():
            user_name = password_form.cleaned_data.get('username')
            user_email = password_form.cleaned_data.get('email')
            try:
                user = User.objects.get(username=user_name)
            except:
                return JsonResponse({'status_code': 2})
            if user.email==user_email:
                if user.has_confirmed:
                    print("sss")
                    code = make_confirm_string(user)
                    try:
                        print("aaaa")
                        send_email_confirm(user_email, code)  # 发送验证码
                    except:
                        return JsonResponse({'status_code': 3})
                    return JsonResponse({'status_code': 1})
                else:
                    return JsonResponse({'status_code': 4, 'message': '用户未进行邮箱验证'})
            else:
                return JsonResponse({'status_code': 5,'message': '邮箱不匹配'})
        else:
            response = {'status_code': -1, 'message': 'invalid form'}
            return JsonResponse(response)
    else:
        response = {'status_code': -2, 'message': '请求错误'}
        return JsonResponse(response)

@csrf_exempt
def find_password_back_SE(request):
    if request.method == 'POST':
        password_form = FindPasswordBackForm_SE(request.POST)
        if password_form.is_valid():
            code = password_form.cleaned_data.get('code')
            new_password_1 = password_form.cleaned_data.get('password_1')
            new_password_2 = password_form.cleaned_data.get('password_2')
            try:
                confirm = ConfirmString.objects.get(code=code)
            except:
                return JsonResponse({'status_code': 2})
            c_time = confirm.c_time.replace(tzinfo=utc)
            now = datetime.datetime.now().replace(tzinfo=utc)
            if now > c_time + datetime.timedelta(settings.CONFIRM_DAYS):
                return JsonResponse({'status_code': 3})
            if new_password_1 != new_password_2:
                response = {'status_code': 4, 'message': '两次输入的密码不同'}
                return JsonResponse(response)
            # 检测密码不符合规范：8-18，英文字母+数字
            if not re.match('^(?![0-9]+$)(?![a-zA-Z]+$)[0-9A-Za-z]{8,18}$', new_password_1):
                return JsonResponse({'status_code': 5})
            confirm.user.password = hash_code(new_password_1)
            confirm.user.save()
            confirm.delete()
            return JsonResponse({'status_code': 1, 'message': 'success'})
        else:
            response = {'status_code': -1, 'message': 'invalid form'}
            return JsonResponse(response)
    else:
        response = {'status_code': -2, 'message': '请求错误'}
        return JsonResponse(response)


@csrf_exempt
def change_username(request):
    if request.method == 'POST':
        username_form = ChangeUserNameForm(request.POST)
        if username_form.is_valid():
            old_username = username_form.cleaned_data['old_username']
            new_username = username_form.cleaned_data['new_username']
            try:
                user = User.objects.get(username=old_username)
            except:
                return JsonResponse({'status_code': 2})
            try:
                user_1 = User.objects.get(username=new_username)
                if user_1:
                    return JsonResponse({'status_code': 3})
            except:
                user.username = new_username
                user.save()
                return JsonResponse({'status_code': 1})
        else:
            return JsonResponse({'status_code': -1, 'message':'invalid form'})
    else: return JsonResponse({'status_code': -2, 'message': '请求错误'})




@csrf_exempt
def change_email_FS(request):
    if request.method == 'POST':
        email_form = ChangeEmailForm_FS(request.POST)
        if email_form.is_valid():
            old_email = email_form.cleaned_data['old_email']
            new_email = email_form.cleaned_data['new_email']
            try:
                user = User.objects.get(email=old_email)
            except:
                return JsonResponse({'status_code': 2})
            if user.has_confirmed:
                print(user.username)
                if ConfirmString.objects.filter(user=user).exists():
                    return JsonResponse({'status_code':7,'message':"fk you"})
                code = make_confirm_string(user)
                print(code)
                try:
                    send_email_change_confirm(new_email, code)  # 发送验证码
                except:
                    return JsonResponse({'status_code': 3})
                return JsonResponse({'status_code': 1})
            else:
                return JsonResponse({'status_code': 4, 'message': '用户未进行邮箱验证'})
        else:
            response = {'status_code': -1, 'message': 'invalid form'}
            return JsonResponse(response)
    else:
        response = {'status_code': -2, 'message': '请求错误'}
        return JsonResponse(response)

@csrf_exempt
def change_email_SE(request):
    if request.method == 'POST':
        email_form = ChangeEmailForm_SE(request.POST)
        if email_form.is_valid():
            old_email = email_form.cleaned_data['old_email']
            new_email = email_form.cleaned_data['new_email']
            code = email_form.cleaned_data['code']
            try:
                confirm = ConfirmString.objects.get(code=code)
            except:
                return JsonResponse({'status_code': 2})
            c_time = confirm.c_time.replace(tzinfo=utc)
            now = datetime.datetime.now().replace(tzinfo=utc)
            if now > c_time + datetime.timedelta(settings.CONFIRM_DAYS):
                return JsonResponse({'status_code': 3})
            confirm.user.email = new_email
            confirm.user.save()
            confirm.delete()
            return JsonResponse({'status_code': 1, 'message': 'success'})
        else:
            response = {'status_code': -1, 'message': 'invalid form'}
            return JsonResponse(response)
    else:
        response = {'status_code': -2, 'message': '请求错误'}
        return JsonResponse(response)


@csrf_exempt
def change_picture(request):
    if request.method == 'POST':
        picture_form = ChangePictureForm(request.POST)
        if picture_form.is_valid():
            url = picture_form.cleaned_data['url']
            username = picture_form.cleaned_data['username']
            try:
                user = User.objects.get(username=username)
            except:
                return JsonResponse({'status_code': 2})
            user.url = url
            user.save()
            return JsonResponse({'status_code': 1})
        else:
            print("7777")
            return JsonResponse({'status_code': -1, 'message': 'invalid form'})
    else: return JsonResponse({'status_code': -2, 'message': '请求错误'})


# @csrf_exempt
# def change_email(request):
#     email = request.POST.get("email")
#     code = request.POST.get("code")
#
#     if User.objects.filter(email=email):
#         return JsonResponse({'status_code': 4})
#
#     try:
#         confirm = ConfirmString.objects.get(code=code)
#     except:
#         return JsonResponse({'status_code': 2})
#
#     c_time = confirm.c_time.replace(tzinfo=utc)
#     now = datetime.datetime.now().replace(tzinfo=utc)
#     if now > c_time + datetime.timedelta(settings.CONFIRM_DAYS):
#         return JsonResponse({'status_code': 3})
#     else:
#         confirm.user.has_confirmed = True
#         confirm.user.email = email
#         confirm.user.save()
#         confirm.delete()
#         return JsonResponse({'status_code': 1})
#
#
# @csrf_exempt
# def send_code(request):
#     if request.method == 'POST':
#         email = request.POST.get('email')
#
#         if User.objects.filter(email=email):
#             return JsonResponse({'status_code': 4})
#
#         user = User.objects.get(username=request.session.get('username'))
#         code = ""
#         for i in range(6):
#             ch = chr(random.randrange(ord('0'), ord('9') + 1))
#             code += ch
#
#         if ConfirmString.objects.filter(user=user):
#             cs = ConfirmString.objects.get(user=user)
#             cs.delete()
#
#         ConfirmString.objects.create(code=code, user=user, )
#         print(user.username + "申请更改邮箱地址，生成随机码为 " + code)
#
#         try:
#             send_email_change_confirm(email=email, code=code)
#             return JsonResponse({'status_code': 1})
#         except:
#             return JsonResponse({'status_code': 2})
#     return JsonResponse({'status_code': 3})
#
#
# @csrf_exempt
# def change_password(request):
#     if request.method == 'POST':
#         password_form = ChangePasswordForm(request.POST)
#         if password_form.is_valid():
#             try:
#                 this_user = User.objects.get(username=request.session['username'])
#             except:
#                 return JsonResponse({'status_code': 0})
#             old_password = password_form.cleaned_data.get('old_password')
#             new_password_1 = password_form.cleaned_data.get('new_password_1')
#             new_password_2 = password_form.cleaned_data.get('new_password_2')
#             if this_user.password != hash_code(old_password):
#                 return JsonResponse({'status_code': 4})
#             if new_password_1 != new_password_2:
#                 response = {'status_code': 2, 'message': '两次输入的密码不同'}
#                 return JsonResponse(response)
#             # 检测密码不符合规范：8-18，英文字母+数字
#             if not re.match('^(?![0-9]+$)(?![a-zA-Z]+$)[0-9A-Za-z]{8,18}$', new_password_1):
#                 return JsonResponse({'status_code': 5})
#             if new_password_1 == old_password:
#                 response = {'status_code': 3, 'message': '新旧密码相同'}
#                 return JsonResponse(response)
#             this_user.password = hash_code(new_password_1)
#             this_user.save()
#             return JsonResponse({'status_code': 1, 'message': 'success'})
#
#         else:
#             response = {'status_code': -1, 'message': 'invalid form'}
#             return JsonResponse(response)
#     else:
#         response = {'status_code': -2, 'message': '请求错误'}
#         return JsonResponse(response)
#
#
#
#
#
# @csrf_exempt
# def get_userinfo(request):
#     if not request.session.get('is_login'):
#         return JsonResponse({'status_code': 3})
#     username = request.session.get('username')
#     print(username + " 请求进入账户设置页面")
#     try:
#         user = User.objects.get(username=username)
#     except:
#         print(username + " 进入账户设置页面失败，将清除前端登录信息")
#         return JsonResponse({'status_code': 2})
#     print(user.username + " 成功进入账户设置页面")
#     return JsonResponse({'status_code': 1, 'username': user.username, 'is_confirmed': user.has_confirmed, 'email': user.email})
#
#
# @csrf_exempt
# def confirm_userinfo(request):
#     username = request.POST.get('username')
#     print(username + " 请求验证登录信息")
#     try:
#         username_backend = request.session['username']
#         print("后端存储用户名为 " + username_backend + ", 前端存储用户名为 " + username)
#         if username_backend != username:
#             print(username + " 验证登录信息失败，将强制退出登录")
#             request.session.flush()
#             return JsonResponse({'status_code': 2})
#     except:
#         print(username + " 验证登录信息失败，将强制退出登录")
#         request.session.flush()
#         return JsonResponse({'status_code': 2})
#     else:
#         print(username + " 验证登录信息成功")
#         return JsonResponse({'status_code': 1})
