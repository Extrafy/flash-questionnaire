import base64
import datetime
import json
import jieba
from collections import Counter
import pytz
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from django.db import transaction
from django.db.models import F

from QN.form import *
from QN.models import *
from User.models import *

KEY_STR = "%&%"
KEY_STR_wtf = "&_&"
class SubmitRecyleNumError(Exception):
    def __init__(self, num):
        self.num = num

    def __str__(self):
        return f"您报名的问卷回收数目为：{self.num}, 已达到最大回收量"

# Create your views here.

def finish_qn(qn_id):
    survey = Survey.objects.get(survey_id=qn_id)
    survey.is_finished = True
    survey.is_released = False
    survey.save()

    return 1

def hash_code(s, salt='Qn'):  # generate s+salt into hash_code (default: salt=online publish)
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())  # update method get bytes(type)
    return h.hexdigest()

# 创建选项
def create_option(question, content, sequence, num):
    option = Option()
    option.content = content
    question.option_num += 1
    option.question_id = question
    question.save()
    option.order = sequence
    option.save()
    option.max_num = num
    option.left_num = num
    option.save()


# 创建问题
def create_question(description, must, typee, qn_id, options, sequence, image_url, video_url, arg1, arg2, arg3):
    question = Question()
    try:
        question.description = description
        question.is_must_answer = must
        question.type = typee
        survey_id = qn_id
        question.survey_id = Survey.objects.get(survey_id=survey_id)
        question.sequence = sequence
        question.video_url = video_url
        question.image_url = image_url
        question.arg1 = arg1
        question.arg2 = arg2
        question.arg3 = arg3
    except:
        response = {'status_code': -3, 'message': '后端炸了'}
        return JsonResponse(response)
    try:
        survey = Survey.objects.get(survey_id=survey_id)
    except:
        response = {'status_code':2,'message':fk}
        return JsonResponse(response)

    question.save()
    if survey.type == '3':
        if question.type == '0' or question.type == '1':
            if question.image_url == 'true':
                option_num = 0
                option_list = options
                num_list = arg3.split(KEY_STR_wtf)
                for option in option_list:
                    content = option['content']
                    create_option(question, content, option_num,num_list[option_num])
                    option_num = option_num + 1
    else :
        if question.type == '0' or question.type == '1':
            option_num = 0
            option_list = options
            for option in option_list:
                content = option['content']
                create_option(question, content, option_num, 0)
                option_num = option_num + 1
    question.save()

# 创建问卷
@csrf_exempt
@api_view(['POST'])
def create_qn(request):
    # global survey
    response = {'status_code': 1, 'message': 'success'}
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        username = data['username']
        title = data['title']
        description = data['description']
        typee = data['type']
        finished_time = data['finished_time']
        do_time = data['fuck_time']
        question_list = data.get('list')
        try:
            user = User.objects.get(username=username)
        except:
            response = {'status_code': 2, 'message': '用户不存在'}
            return JsonResponse(response)

        if title == '':
            title = "默认标题"
        try:
            survey = Survey()
            survey.user_id = user.user_id
            survey.title = title
            survey.description = description
            survey.type = typee
            if finished_time != '':
                survey.finished_time = finished_time
            if do_time != '':
                survey.do_time = do_time
            survey.question_num = 0
            survey.recycling_num = 0
            survey.save()
        except:
            response = {'status_code': -3, 'message': '后端炸了'}
            return JsonResponse(response)
        # print("<<<<")
        question_num = 0
        for question in question_list:
            qs_options = question.get("options", [])
            qs_description = question.get("description", "")
            qs_type = str(question.get("type", ""))
            qs_must = question.get("must", "")
            qs_qn_id = survey.survey_id
            qs_img_url = question.get("img_url", "")
            qs_video_url = question.get("video_url", "")
            qs_arg1 = question.get("arg1", 0)
            qs_arg2 = question.get("arg2", 0)
            qs_arg3 = question.get("arg3", 0)
            create_question(qs_description, qs_must, qs_type, qs_qn_id, qs_options, question_num, qs_img_url,
                            qs_video_url, qs_arg1, qs_arg2, qs_arg3)
            question_num += 1
        survey.question_num = question_num
        survey.save()
        response['qn_id'] = survey.survey_id
        return JsonResponse(response)
    else:
        response = {'status_code': -2, 'message': 'invalid http method'}
        return JsonResponse(response)

# 发布问卷
@csrf_exempt
@api_view(['POST'])
def deploy_qn(request):
    response = {'status_code': 1, 'message': 'success'}
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        qn_id = data['qn_id']
        try:
            survey = Survey.objects.get(survey_id=qn_id)
        except:
            response = {'status_code': 2, 'message': '问卷不存在'}
            return JsonResponse(response)

        if survey.is_deleted == True:
            response = {'status_code': 4, 'message': '问卷已经放入回收站'}
            return JsonResponse(response)

        if survey.is_released == True:
            response = {'status_code': 3, 'message': '问卷已经发布，不要重复操作'}
            return JsonResponse(response)

        if survey.is_finished == True:
            response = {'status_code': 6, 'message': '问卷已经结束，不可操作'}
            return JsonResponse(response)

        if (Question.objects.filter(survey_id=survey)).count() == 0:
            response = {'status_code': 7, 'message': '问卷中无问题，不可发行'}
            return JsonResponse(response)

        survey.is_released = True
        if survey.release_time == '' or survey.release_time is None or survey.release_time == 'null':
            survey.release_time = datetime.datetime.now()
        # if survey.share_url == '' or survey.share_url is None or survey.share_url == 'null':
        #     # 生成问卷码
        #     code = hash_code(survey.username, str(survey.survey_id))
        #     # code = hash_code(code, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        #     end_info = code[:20].upper()
        #     while Survey.objects.filter(share_url=end_info):
        #         code = hash_code(code, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        #         end_info = code[:20].upper()
        #     survey.share_url = end_info
        #     survey.save()
        #     return JsonResponse({'status_code': 10, 'code': survey.share_url})
        survey.save()
        return JsonResponse(response)
    else:
        response = {'status_code': -2, 'message': '请求错误'}
        return JsonResponse(response)

# 下架问卷
@csrf_exempt
@api_view(['POST'])
def pause_qn(request):
    response = {'status_code': 1, 'message': 'success'}
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        qn_id = data['qn_id']
        try:
            survey = Survey.objects.get(survey_id=qn_id)
        except:
            response = {'status_code': -1, 'message': '问卷不存在'}
            return JsonResponse(response)
        if survey.is_deleted == True:
            response = {'status_code': 2, 'message': '问卷已放入回收站'}
            return JsonResponse(response)
        if survey.is_finished == True:
            response = {'status_code': 6, 'message': '问卷已经结束，不可操作'}
            return JsonResponse(response)
        if not survey.is_released:
            response = {'status_code': 3, 'message': '问卷未发行，不可取消发行'}
            return JsonResponse(response)
        survey.is_released = False
        survey.save()
        return JsonResponse(response)
    else:
        response = {'status_code': -2, 'message': '请求错误'}
        return JsonResponse(response)

# 将问卷放入回收站
@csrf_exempt
@api_view(['POST'])
def delete_survey_not_real(request):
    response = {'status_code': 1, 'message': 'success'}
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        qn_id = data['qn_id']
        try:
            survey = Survey.objects.get(survey_id=qn_id)
        except:
            response = {'status_code': -1, 'message': '问卷不存在'}
            return JsonResponse(response)
        if survey.is_deleted == True:
            response = {'status_code': 0, 'message': '问卷已放入回收站'}
            return JsonResponse(response)
        survey.is_deleted = True
        survey.is_released = False
        survey.is_finished = False
        survey.is_collected = False
        survey.save()
        return JsonResponse(response)
    else:
        response = {'status_code': -2, 'message': '请求错误'}
        return JsonResponse(response)

# 将回收站中的问卷恢复
@csrf_exempt
@api_view(['POST'])
def recover_survey_from_delete(request):
    response = {'status_code': 1, 'message': 'success'}
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        qn_id = data['qn_id']
        try:
            survey = Survey.objects.get(survey_id=qn_id)
        except:
            response = {'status_code': -1, 'message': '问卷不存在'}
            return JsonResponse(response)
        if survey.is_deleted == False:
            response = {'status_code': 3, 'message': '问卷未放入回收站'}
            return JsonResponse(response)

        survey.is_deleted = False
        survey.is_released = False
        survey.is_finished = False
        survey.is_collected = False
        survey.save()
        return JsonResponse(response)
    else:
        response = {'status_code': -2, 'message': '请求错误'}
        return JsonResponse(response)

# 将回收站中的问卷彻底删除
@csrf_exempt
@api_view(['POST'])
def delete_survey_real(request):
    response = {'status_code': 1, 'message': 'success'}
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        qn_id = data.get('qn_id')
        try:
            survey = Survey.objects.get(survey_id=qn_id)
        except:
            response = {'status_code': -1, 'message': '问卷不存在'}
            return JsonResponse(response)

        survey.delete()
        # 是否真的删掉呢
        return JsonResponse(response)
    else:
        response = {'status_code': -2, 'message': '请求错误'}
        return JsonResponse(response)


# 将回收站中的所有问卷彻底删除
@csrf_exempt
@api_view(['POST'])
def delete_all_survey_real(request):
    response = {'status_code': 1, 'message': 'success'}
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        user_name = data.get('user_name')
        try:
            user = User.objects.get(username=user_name)
        except:
            response = {'status_code': -1, 'message': '用户不存在'}
            return JsonResponse(response)

        surveys = Survey.objects.filter(user_id=user.user_id)
        for survey in surveys:
            if survey.is_deleted:
                survey.delete()
        return JsonResponse(response)
    else:
        response = {'status_code': -2, 'message': '请求错误'}
        return JsonResponse(response)



# 填写问卷第一步
@csrf_exempt
@api_view(['POST'])
def fill_in_QN_FS(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        qn_id = data.get('q_id')
        print("i am here")
        try:
            survey = Survey.objects.get(survey_id=qn_id)
        except:
            response = {'status_code':2, 'message': 'fuck you'}
            return JsonResponse(response)
        if survey.is_deleted:
            response = {'status_code':4,'message':'问卷已删除'}
            return JsonResponse(response)
        if survey.is_released == False:
            return JsonResponse({'status_code': 5, 'message': '问卷未发布'})
        if survey.recycling_num >= survey.max_recycling & survey.max_recycling != 0:
            finish_qn(survey.survey_id)
            return JsonResponse({'status_code': 6, 'message': '人数已满'})
        response = {}
        response['status_code'] = 1
        response['message'] = 'damn'
        response['type'] = survey.type
        response['title'] = survey.title
        response['description'] = survey.description
        response['finished_time'] = survey.finished_time
        response['created_time'] = survey.created_time
        response['fuck_time'] = survey.do_time
        question_list = Question.objects.filter(survey_id=qn_id)
        questions = []
        for question in question_list:
            question_backing = {}
            question_backing['type'] = question.type
            question_backing['description'] = question.description
            question_backing['arg1'] = question.arg1
            question_backing['arg2'] = question.arg2
            question_backing['arg3'] = question.arg3
            question_backing['must'] = question.is_must_answer
            question_backing['img_url'] = question.image_url
            question_backing['video_url'] = question.video_url

            id = question.question_id
            option_list = Option.objects.filter(question_id=id)
            options = []
            for option in option_list:
                option_backing = {}
                option_backing['content'] = option.content
                option_backing['choosed'] = option.choosed
                option_backing['left_num'] = option.left_num
                options.append(option_backing)
            question_backing['options'] = options
            questions.append(question_backing)
        response['list'] = questions
        # print(questions)
        return JsonResponse(response)
    else :
        response = {'status_code': -2, 'message': '请求错误'}
        return JsonResponse(response)

# 填写问卷第二步
@csrf_exempt
@api_view(['POST'])
def fill_in_QN_SE(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        user_name = data.get('user_name')
        answer_list = data.get('answer_list')
        qn_id = data.get('q_id')
        judge = data.get('isBao')
        print(qn_id)
        try:
            survey = Survey.objects.get(survey_id=qn_id)
        except:
            response = {'status_code':2, 'message': 'fuck you'}
            return JsonResponse(response)
        try:
            user = User.objects.get(username=user_name)
        except:
            response = {'status_code':3, 'message':'wtf?'}
            return JsonResponse(response)
        if survey.is_deleted:
            response = {'status_code':4,'message':'问卷已删除'}
            return JsonResponse(response)
        if survey.is_released == False:
            return JsonResponse({'status_code': 5, 'message': '问卷未发布'})
        if survey.recycling_num >= survey.max_recycling & survey.max_recycling != 0:
            finish_qn(survey.survey_id)
            return JsonResponse({'status_code': 6, 'message': '人数已满'})

        if Submit.objects.filter(survey_id=survey, user_id=user.user_id).exists():
            submit_old = Submit.objects.get(survey_id=survey,user_id=user.user_id)
            submit_old.user_id = 0
            submit_old.save()
        try:
            with transaction.atomic():
                survey_lock = Survey.objects.select_for_update().get(survey_id=survey.survey_id)
                if survey_lock.recycling_num + 1 > survey_lock.max_recycling:
                    raise SubmitRecyleNumError(survey.recycling_num)
                survey_lock.recycling_num = survey_lock.recycling_num + 1
                survey_lock.save()
        except SubmitRecyleNumError as e:
            finish_qn(qn_id)
            return JsonResponse({'status_code': 11, 'message': '问卷报名已满'})
        submit = Submit(user_id=user.user_id, survey_id=survey)
        submit.save()
        questions = Question.objects.filter(survey_id=survey).order_by('question_id')
        num = 0
        for answer_dict in answer_list:
            if answer_dict['ans'] is None:
                continue
            question = questions[num]
            wtf = judge[num]
            answer = Answer(answer=answer_dict['ans'], user_id=user.user_id, question_id=question, submit_id=submit)
            if answer.answer == '' or answer.answer is None:
                answer.answer = ''
            answer.save()
            if wtf == 1:
                answer_dick = answer.answer.split(KEY_STR)
                options = Option.objects.filter(question_id=question)
                for option in options:
                    if option.content in answer_dick:
                        option.left_num = option.left_num-1
                        option.save()
            num = num + 1

        add_filledQN = str(qn_id)
        histories = user.filled_QN
        history_list = histories.split(KEY_STR)
        if histories == '':
            user.filled_QN = add_filledQN
        else:
            if add_filledQN not in history_list:
                user.filled_QN = user.filled_QN + KEY_STR + add_filledQN
        user.save()
        coins = user.Flash_coin
        coins = coins + 1
        user.Flash_coin = coins
        user.save()
        response = JsonResponse({'status_code': 1, 'message': 'm3?'})
        return response
    else:
        response = {'status_code': -2, 'message': '请求错误'}
        return JsonResponse(response)

# 获取用户数据
@csrf_exempt
@api_view(['POST'])
def get_survey_data(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        user_name = data['user_name']
        try:
            user = User.objects.get(username=user_name)
        except:
            response = {'status_code':2,'message':'fk you'}
            return JsonResponse(response)
        list = []
        surveys = Survey.objects.filter(user_id=user.user_id).order_by('survey_id')
        for survey in surveys:
            if survey.is_deleted:
                continue
            damn = {}
            damn['id'] = survey.survey_id
            damn['name'] = survey.title
            damn['type'] = survey.type
            if survey.is_released:
                damn['state'] = 1
            else:
                damn['state'] = 2
            damn['time'] = survey.created_time
            damn['used_time'] = survey.recycling_num
            list.append(damn)
        response = {'status_code':1,'list':list}
        return JsonResponse(response)
    else:
        response = {'status_code': -2, 'message': '请求错误'}
        return JsonResponse(response)

# 获取回收站中的数据
@csrf_exempt
@api_view(['POST'])
def get_survey_in_recyclebin_data(request):
    if request.method == 'POST':
        print("23")
        data = json.loads(request.body.decode('utf-8'))
        user_name = data['user_name']
        try:
            user = User.objects.get(username=user_name)
        except:
            response = {'status_code':2,'message':'fk you'}
            return JsonResponse(response)
        list = []
        surveys = Survey.objects.filter(user_id=user.user_id).order_by('survey_id')
        for survey in surveys:
            if not survey.is_deleted:
                continue
            damn = {}
            damn['id'] = survey.survey_id
            damn['name'] = survey.title
            damn['type'] = survey.type
            damn['time'] = survey.created_time
            damn['used_time'] = survey.recycling_num
            list.append(damn)
        response = {'status_code':1,'list':list}
        return JsonResponse(response)
    else:
        response = {'status_code': -2, 'message': '请求错误'}
        return JsonResponse(response)

# 交叉分析第一步
@csrf_exempt
@api_view(['POST'])
def cross_analyse_FS(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        qn_id = data['qn_id']
        print(qn_id)
        try:
            survey = Survey.objects.get(survey_id=qn_id)
        except:
            response = {'status_code':2,'message':'fk you'}
            return JsonResponse(response)
        list = []
        questions = Question.objects.filter(survey_id=survey).order_by('question_id')
        for question in questions:
            damn = {}
            damn['id'] = question.question_id
            damn['title'] = question.description
            list.append(damn)
        print(list)
        response = {'status_code':1,'list':list}
        return JsonResponse(response)
    else:
        response = {'status_code': -2, 'message': '请求错误'}
        return JsonResponse(response)

# 交叉分析第二步
@csrf_exempt
@api_view(['POST'])
def cross_analyse_SE(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        qn_id = data['qn_id']
        q_id1 = data['q_id1']
        q_id2 = data['q_id2']
        print(qn_id,q_id1,q_id2)
        try:
            survey = Survey.objects.get(survey_id=qn_id)
        except:
            response = {'status_code':2,'message':'fk you'}
            return JsonResponse(response)
        list = []
        try:
            question1 = Question.objects.get(question_id=q_id1)
        except:
            response = {'status_code': 2, 'message': 'fk you'}
            return JsonResponse(response)
        try:
            question2 = Question.objects.get(question_id=q_id2)
        except:
            response = {'status_code': 2, 'message': 'fk you'}
            return JsonResponse(response)
        submit_list = Submit.objects.filter(survey_id=survey).order_by('submit_id')
        damn = {}
        m3 = {}
        wfy = []
        sxb = []
        if question1.type == '2' and question2.type == '2':
            max2 = question2.arg2
            max1 = question1.arg2
            for i in range(max2+1):
                man = {}
                man['content'] = i
                wfy.append(man)
            damn['q2_options'] = wfy
            list.append(damn)
            for i in range(max1+1):
                wtf = {}
                wtf['content'] = i
                gm = []
                for j in range(max2+1):
                    num = 0
                    content1 = str(i)
                    content2 = str(j)
                    tmp = {}
                    for submit in submit_list:
                        answer1 = Answer.objects.get(submit_id=submit, question_id=question1)
                        answer2 = Answer.objects.get(submit_id=submit, question_id=question2)
                        answer1_content_list = answer1.answer.split(KEY_STR)
                        answer2_content_list = answer2.answer.split(KEY_STR)
                        if content1 in answer1_content_list and content2 in answer2_content_list:
                            num = num + 1
                    tmp['count'] = num
                    gm.append(tmp)
                wtf['options'] = gm
                sxb.append(wtf)
            m3['count'] = sxb
            list.append(m3)
        elif question1.type != 2 and question2.type !=2:
            options2 = Option.objects.filter(question_id=question2).order_by('option_id')
            options1 = Option.objects.filter(question_id=question1).order_by('option_id')
            for option in options2:
                man = {}
                man['content'] = option.content
                wfy.append(man)
            damn['q2_options'] = wfy
            list.append(damn)
            for option in options1:
                wtf = {}
                wtf['content'] = option.content
                gm = []
                for option_damn in options2:
                    num = 0
                    content1 = option.content
                    content2 = option_damn.content
                    tmp = {}
                    for submit in submit_list:
                        answer1 = Answer.objects.get(submit_id=submit, question_id=question1)
                        answer2 = Answer.objects.get(submit_id=submit, question_id=question2)
                        answer1_content_list = answer1.answer.split(KEY_STR)
                        answer2_content_list = answer2.answer.split(KEY_STR)
                        if content1 in answer1_content_list and content2 in answer2_content_list:
                            num = num + 1
                    tmp['count'] = num
                    gm.append(tmp)
                wtf['options'] = gm
                sxb.append(wtf)
            m3['count'] = sxb
            list.append(m3)
        elif question1.type == 2 and question2.type != 2:
            options2 = Option.objects.filter(question_id=question2).order_by('option_id')
            max1 = question1.arg2
            for option in options2:
                man = {}
                man['content'] = option.content
                wfy.append(man)
            damn['q2_options'] = wfy
            list.append(damn)
            for i in range(max1+1):
                wtf = {}
                wtf['content'] = i
                gm = []
                for option_damn in options2:
                    num = 0
                    content1 = str(i)
                    content2 = option_damn.content
                    tmp = {}
                    for submit in submit_list:
                        answer1 = Answer.objects.get(submit_id=submit, question_id=question1)
                        answer2 = Answer.objects.get(submit_id=submit, question_id=question2)
                        answer1_content_list = answer1.answer.split(KEY_STR)
                        answer2_content_list = answer2.answer.split(KEY_STR)
                        if content1 in answer1_content_list and content2 in answer2_content_list:
                            num = num + 1
                    tmp['count'] = num
                    gm.append(tmp)
                wtf['options'] = gm
                sxb.append(wtf)
            m3['count'] = sxb
            list.append(m3)
        else :
            options1 = Option.objects.filter(question_id=question1).order_by('option_id')
            max2 = question1.arg2
            for i in range(max2 + 1):
                man = {}
                man['content'] = i
                wfy.append(man)
            damn['q2_options'] = wfy
            list.append(damn)
            for option in options1:
                wtf = {}
                wtf['content'] = option.content
                gm = []
                for i in range(max2+1):
                    num = 0
                    content1 = option.content
                    content2 = str(i)
                    tmp = {}
                    for submit in submit_list:
                        answer1 = Answer.objects.get(submit_id=submit, question_id=question1)
                        answer2 = Answer.objects.get(submit_id=submit, question_id=question2)
                        answer1_content_list = answer1.answer.split(KEY_STR)
                        answer2_content_list = answer2.answer.split(KEY_STR)
                        if content1 in answer1_content_list and content2 in answer2_content_list:
                            num = num + 1
                    tmp['count'] = num
                    gm.append(tmp)
                wtf['options'] = gm
                sxb.append(wtf)
            m3['count'] = sxb
            list.append(m3)
        response = {'status_code':1,'list':list}
        return JsonResponse(response)
    else:
        response = {'status_code': -2, 'message': '请求错误'}
        return JsonResponse(response)

# 复制问卷
@csrf_exempt
@api_view(['POST'])
def copy_survey(request):
    response = {'status_code': 1, 'message': 'success'}
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        qn_id = data['qn_id']
        title = data['title']
        try:
            survey_old = Survey.objects.get(survey_id=qn_id)
        except:
            response = {'status_code': -1, 'message': '问卷不存在'}
            return JsonResponse(response)
        if survey_old.is_deleted == True:
            response = {'status_code': 0, 'message': '问卷已放入回收站'}
            return JsonResponse(response)
        user_id = survey_old.user_id
        description = survey_old.description
        typee = survey_old.type
        finished_time = survey_old.finished_time
        do_time = survey_old.do_time
        question_list = []
        questions = Question.objects.filter(survey_id=survey_old).order_by('question_id')
        for question in questions:
            sxb = {}
            sxb['type'] = question.type
            sxb['description'] = question.description
            sxb['arg1'] = question.arg1
            sxb['arg2'] = question.arg2
            sxb['arg3'] = question.arg3
            sxb['must'] = question.is_must_answer
            options = Option.objects.filter(question_id=question).order_by('option_id')
            damn = []
            for option in options:
                tmp = {}
                tmp['content'] = option.content
                tmp['choosed'] = option.choosed
                damn.append(tmp)
            sxb['options'] = damn
            question_list.append(sxb)

        if title == '':
            title = "默认标题"
        try:
            # survey = Survey(username=username, title=title, type=type, description=description, question_num=0, recycling_num=0)
            survey = Survey()
            survey.user_id = user_id
            survey.title = title
            survey.description = description
            survey.type = typee
            if finished_time != '':
                survey.finished_time = finished_time
            if do_time != '':
                survey.do_time = do_time
            survey.question_num = 0
            survey.recycling_num = 0
            survey.save()
        except:
            response = {'status_code': -3, 'message': '后端炸了'}
            return JsonResponse(response)
        question_num = 0
        for question in question_list:
            qs_options = question.get("options", [])
            qs_description = question.get("description", "")
            qs_type = question.get("type", "")
            qs_must = question.get("must", "")
            qs_qn_id = survey.survey_id
            qs_img_url = question.get("img_url", "")
            qs_video_url = question.get("video_url", "")
            qs_arg1 = question.get("arg1", 0)
            qs_arg2 = question.get("arg2", 0)
            qs_arg3 = question.get("arg3", 0)
            create_question(qs_description, qs_must, qs_type, qs_qn_id, qs_options, question_num, qs_img_url,
                            qs_video_url, qs_arg1, qs_arg2, qs_arg3)
            question_num += 1

        survey.question_num = question_num
        survey.save()
        response['qn_id'] = survey.survey_id
        return JsonResponse(response)
    else:
        response = {'status_code': -2, 'message': '请求错误'}
        return JsonResponse(response)

# 编辑问卷第一步
@csrf_exempt
@api_view(['POST'])
def edit_survey_FS(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        qn_id = data['qn_id']
        print(qn_id)
        try:
            survey_old = Survey.objects.get(survey_id=qn_id)
        except:
            response = {'status_code': -1, 'message': '问卷不存在'}
            return JsonResponse(response)
        if survey_old.is_deleted == True:
            response = {'status_code': 0, 'message': '问卷已放入回收站'}
            return JsonResponse(response)
        title = survey_old.title
        description = survey_old.description
        typee = survey_old.type
        finished_time = survey_old.finished_time
        question_list = []
        questions = Question.objects.filter(survey_id=survey_old).order_by('question_id')
        for question in questions:
            sxb = {}
            sxb['type'] = question.type
            sxb['description'] = question.description
            sxb['arg1'] = question.arg1
            sxb['arg2'] = question.arg2
            sxb['arg3'] = question.arg3
            sxb['must'] = question.is_must_answer
            sxb['img_url'] = question.image_url
            options = Option.objects.filter(question_id=question).order_by('option_id')
            damn = []
            for option in options:
                tmp = {}
                tmp['content'] = option.content
                tmp['choosed'] = option.choosed
                damn.append(tmp)
            sxb['options'] = damn
            question_list.append(sxb)
        response = {'status_code':1,'title':title,'description':description,'type':typee,'finished_time':finished_time,'question_list':question_list}
        return JsonResponse(response)
    else:
        response = {'status_code': -2, 'message': '请求错误'}
        return JsonResponse(response)


# 编辑问卷第二步
@csrf_exempt
@api_view(['POST'])
def edit_survey_SE(request):
    # global survey
    response = {'status_code': 1, 'message': 'success'}
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        username = data['username']
        title = data['title']
        description = data['description']
        typee = data['type']
        finished_time = data['finished_time']
        old_ID = data['old_ID']
        print(old_ID)
        question_list = data.get('list')
        try:
            old_survey = Survey.objects.get(survey_id=old_ID)
        except:
            response = {'status_code': 3, 'message': '旧问卷ID不存在'}
            return JsonResponse(response)
        old_survey.user_id = 0
        old_survey.save()
        try:
            user = User.objects.get(username=username)
        except:
            response = {'status_code': 2, 'message': '用户不存在'}
            return JsonResponse(response)
        if title == '':
            title = "默认标题"
        try:
            # survey = Survey(username=username, title=title, type=type, description=description, question_num=0, recycling_num=0)
            survey = Survey()
            survey.user_id = user.user_id
            survey.title = title
            survey.description = description
            survey.type = typee
            if finished_time != '':
                survey.finished_time = finished_time
            survey.question_num = 0
            survey.recycling_num = 0
            survey.save()
        except:
            response = {'status_code': -3, 'message': '后端炸了'}
            return JsonResponse(response)
        question_num = 0
        for question in question_list:
            qs_options = question.get("options", [])
            qs_description = question.get("description", "")
            qs_type = str(question.get("type", ""))
            qs_must = question.get("must", "")
            qs_qn_id = survey.survey_id
            qs_img_url = question.get("img_url", "")
            qs_video_url = question.get("video_url", "")
            qs_arg1 = question.get("arg1", 0)
            qs_arg2 = question.get("arg2", 0)
            qs_arg3 = question.get("arg3", 0)
            create_question(qs_description, qs_must, qs_type, qs_qn_id, qs_options, question_num, qs_img_url,
                            qs_video_url, qs_arg1, qs_arg2, qs_arg3)
            question_num += 1
        survey.question_num = question_num
        # print("保存成功，该问卷的问题数目为：" + str(question_num))
        survey.save()
        response['qn_id'] = survey.survey_id
        return JsonResponse(response)
    else:
        response = {'status_code': -2, 'message': 'invalid http method'}
        return JsonResponse(response)

# 数据分析第一步
@csrf_exempt
@api_view(['POST'])
def data_analysis_FS(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        qn_id = data.get('q_id')
        user_name = data.get('user_name')
        try:
            survey = Survey.objects.get(survey_id=qn_id)
        except:
            response = {'status_code':2, 'message': 'fuck you'}
            return JsonResponse(response)
        try:
            user = User.objects.get(username=user_name)
        except:
            response = {'status_code':3, 'message': 'invalid username'}
            return JsonResponse(response)
        if survey.user_id != user.user_id:
            boughts = user.bought_QN
            bought_list = boughts.split(KEY_STR)
            check = str(survey.survey_id)
            if check not in bought_list:
                response = {'status_code': 7, 'message': 'fkme'}
                return JsonResponse(response)
        if survey.is_deleted:
            response = {'status_code':4,'message':'问卷已删除'}
            return JsonResponse(response)
        # if survey.is_released == False:
        #     return JsonResponse({'status_code': 5, 'message': '问卷未发布'})
        if survey.recycling_num >= survey.max_recycling & survey.max_recycling != 0:
            finish_qn(survey.survey_id)
            return JsonResponse({'status_code': 6, 'message': '人数已满'})
        response = {}
        response['status_code'] = 1
        response['message'] = 'damn'
        response['type'] = survey.type
        response['title'] = survey.title
        response['description'] = survey.description
        response['finished_time'] = survey.finished_time
        response['created_time'] = survey.created_time
        response['fuck_time'] = survey.do_time
        question_list = Question.objects.filter(survey_id=qn_id)
        questions = []
        for question in question_list:
            question_backing = {}
            question_backing['type'] = question.type
            question_backing['description'] = question.description
            question_backing['arg1'] = question.arg1
            question_backing['arg2'] = question.arg2
            question_backing['arg3'] = question.arg3
            question_backing['must'] = question.is_must_answer
            question_backing['img_url'] = question.image_url
            question_backing['video_url'] = question.video_url
            option_list = Option.objects.filter(question_id=question)
            options = []
            for option in option_list:
                option_backing = {}
                option_backing['content'] = option.content
                option_backing['choosed'] = option.choosed
                options.append(option_backing)
            question_backing['options'] = options
            questions.append(question_backing)
        response['list'] = questions
        return JsonResponse(response)
    else :
        response = {'status_code': -2, 'message': '请求错误'}
        return JsonResponse(response)


# 数据分析第二步
@csrf_exempt
@api_view(['POST'])
def data_analysis_SE(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        qn_id = data['qn_id']
        print(qn_id)
        try:
            survey_old = Survey.objects.get(survey_id=qn_id)
        except:
            response = {'status_code': -1, 'message': '问卷不存在'}
            return JsonResponse(response)
        if survey_old.is_deleted == True:
            response = {'status_code': 0, 'message': '问卷已放入回收站'}
            return JsonResponse(response)
        questions = Question.objects.filter(survey_id=qn_id).order_by('question_id')
        submit_list = Submit.objects.filter(survey_id=qn_id).order_by('submit_id')
        klg = []
        for question in questions:
            ysh=[]
            if question.type == '0' or question.type == '1':
                options = Option.objects.filter(question_id=question).order_by('option_id')
                for option in options:
                    man = {}
                    content = option.content
                    man['name'] = content
                    count = 0
                    for submit in submit_list:
                        answer_tmp = Answer.objects.get(submit_id=submit, question_id=question)
                        answer_content_list = answer_tmp.answer.split(KEY_STR)
                        if content in answer_content_list:
                            count = count + 1
                    man['y'] = count
                    ysh.append(man)
            elif question.type == '3':
                words=[]
                total = ''
                for submit in submit_list:
                    answer_tmp = Answer.objects.get(submit_id=submit, question_id=question)
                    answer_content = answer_tmp.answer
                    if total == '':
                        total = answer_content
                    else:
                        total = total + '。' + answer_content
                seg_list = jieba.cut(total, cut_all=False)
                words.extend(seg_list)
                word_counts = Counter(words)
                result_dict = dict(word_counts)
                result_list = [{'name': word, 'y': count} for word, count in result_dict.items()]
                ysh.extend(result_list)
            else:
                max = question.arg2
                for i in range(max):
                    man = {}
                    man['name'] = i
                    man['y'] = 0
                    ysh.append(man)
                for submit in submit_list:
                    answer_tmp = Answer.objects.get(submit_id=submit, question_id=question)
                    answer_content = answer_tmp.answer
                    ans = int(answer_content)
                    tmp_jj = ysh[ans-1]
                    tmp_ans = tmp_jj['y']
                    tmp_ans = tmp_ans + 1
                    ysh[ans-1]['y'] = tmp_ans
            klg.append(ysh)
        response = {'status_code': 1, 'list':klg}
        return JsonResponse(response)
    else:
        response = {'status_code': -2, 'message': '请求错误'}
        return JsonResponse(response)

# 数据分析第三步
@csrf_exempt
@api_view(['POST'])
def data_analysis_TH(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        qn_id = data['qn_id']
        print(qn_id)
        try:
            survey_old = Survey.objects.get(survey_id=qn_id)
        except:
            response = {'status_code': -1, 'message': '问卷不存在'}
            return JsonResponse(response)
        if survey_old.is_deleted == True:
            response = {'status_code': 0, 'message': '问卷已放入回收站'}
            return JsonResponse(response)
        questions = Question.objects.filter(survey_id=qn_id).order_by('question_id')
        submit_list = Submit.objects.filter(survey_id=qn_id).order_by('submit_id')
        colname = []
        rows = []
        num1 = 1
        for question in questions:
            content = question.title + str(num1)
            num1 = num1 + 1
            colname.append(content)
        for submit in submit_list:
            if submit.user_id == 0:
                continue
            tmp = {}
            num2 = 1
            for question in questions:
                description = question.title + str(num2)
                num2 = num2 + 1
                answer_tmp = Answer.objects.get(submit_id=submit, question_id=question)
                answer_content = answer_tmp.answer
                if question.type == '1':
                    answer_content = '，'.join(['【' + s + '】'for s in answer_content.split(KEY_STR)])
                tmp[description] = answer_content
            rows.append(tmp)
        response = {'status_code': 1, 'colname':colname,'rows':rows}
        return JsonResponse(response)
    else:
        response = {'status_code': -2, 'message': '请求错误'}
        return JsonResponse(response)

# 收藏问卷
@csrf_exempt
@api_view(['POST'])
def collect_survey(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        qn_id = data['qn_id']
        user_name = data['user_name']
        print(qn_id,user_name)
        try:
            user = User.objects.get(username=user_name)
        except:
            response = {'status_code':2,'message':'fk'}
            return JsonResponse(response)
        add_collection = str(qn_id)
        collections = user.collection
        collection_list = collections.split(KEY_STR)
        if collections == '':
            user.collection = add_collection
        else:
            if add_collection in collection_list:
                response = {'status_code':4,'message':'fkme'}
                return JsonResponse(response)
            user.collection = user.collection + KEY_STR + add_collection
        user.save()
        response = {'status_code':1,'message':'good'}
        return JsonResponse(response)
    else:
        response = {'status_code': -2, 'message': '请求错误'}
        return JsonResponse(response)

# 获取收藏问卷记录
@csrf_exempt
@api_view(['POST'])
def get_collections(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        user_name = data['user_name']
        try:
            user = User.objects.get(username=user_name)
        except:
            response = {'status_code':2,'message':'fk'}
            return JsonResponse(response)
        collections = user.collection
        collection_list = collections.split(KEY_STR)
        blocks = []
        for collection in collection_list:
            try:
                survey = Survey.objects.get(survey_id=int(collection))
            except:
                response = {'status_code':3,'message':'问卷不存在'}
                return JsonResponse(response)
            tmp = {}
            tmp['id'] = survey.survey_id
            tmp['title'] = survey.title
            tmp['state'] = survey.is_released
            tmp['used_time'] = survey.recycling_num
            tmp['type'] = survey.type
            blocks.append(tmp)
        response = {'status_code':1,'blocks':blocks}
        return JsonResponse(response)
    else:
        response = {'status_code': -2, 'message': '请求错误'}
        return JsonResponse(response)

# 取消问卷收藏
@csrf_exempt
@api_view(['POST'])
def cancel_collections(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        user_name = data['user_name']
        qn_id = data['qn_id']
        print(qn_id)
        print(user_name)
        try:
            user = User.objects.get(username=user_name)
        except:
            response = {'status_code':2,'message':'fk'}
            return JsonResponse(response)
        collections = user.collection
        collection_list = collections.split(KEY_STR)
        ans_collection = ''
        for collection in collection_list:
            if str(qn_id) != collection:
                if ans_collection != '':
                    ans_collection = ans_collection + KEY_STR + collection
                else:
                    ans_collection = collection
        user.collection = ans_collection
        user.save()
        response = {'status_code':1,'message':'fk'}
        return JsonResponse(response)
    else:
        response = {'status_code': -2, 'message': '请求错误'}
        return JsonResponse(response)

# 获取用户问卷填写记录
@csrf_exempt
@api_view(['POST'])
def get_history(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        user_name = data['user_name']
        print(user_name)
        try:
            user = User.objects.get(username=user_name)
        except:
            response = {'status_code':2,'message':'fk'}
            return JsonResponse(response)
        histories = user.filled_QN
        if not histories:
            print("wtf")
        history_list = histories.split(KEY_STR)
        list1 = []
        if history_list:
            for history in history_list:
                try:
                    survey = Survey.objects.get(survey_id=int(history))
                except:
                    response = {'status_code': 3, 'message': '问卷不存在'}
                    return JsonResponse(response)
                tmp = {}
                tmp['id'] = survey.survey_id
                tmp['title'] = survey.title
                tmp['state'] = survey.is_released
                tmp['used_time'] = survey.recycling_num
                tmp['type'] = survey.type
                list1.append(tmp)
        list2 = []
        list3 = []
        boughts = user.bought_QN
        bought_list = boughts.split(KEY_STR)
        if boughts:
            for bought in bought_list:
                id = int(bought)
                try:
                    survey = Survey.objects.get(survey_id=id)
                except:
                    response = {'status_code': 3, 'message': 'fk'}
                    return JsonResponse(response)
                damn = {}
                damn['id'] = survey.survey_id
                list2.append(damn)
        collections = user.collection
        collection_list = collections.split(KEY_STR)
        if not collections:
            response = {'status_code': 1, 'list1':list1, 'list2': list2, 'list3': list3}
            return JsonResponse(response)
        for collection in collection_list:
            id = int(collection)
            try:
                survey = Survey.objects.get(survey_id=id)
            except:
                response = {'status_code': 3, 'message': 'fk'}
                return JsonResponse(response)
            damn = {}
            damn['id'] = survey.survey_id
            list3.append(damn)
        response = {'status_code':1,'list1':list1,'list2':list2,'list3':list3}
        return JsonResponse(response)
    else:
        response = {'status_code': -2, 'message': '请求错误'}
        return JsonResponse(response)

# 删除用户问卷填写记录
@csrf_exempt
@api_view(['POST'])
def cancel_history(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        user_name = data['user_name']
        qn_id = data['q_id']
        try:
            user = User.objects.get(username=user_name)
        except:
            response = {'status_code':2,'message':'fk'}
            return JsonResponse(response)
        histories = user.filled_QN
        history_list = histories.split(KEY_STR)
        ans_history = ''
        for history in history_list:
            if str(qn_id) != history:
                if ans_history != '':
                    ans_history = ans_history + KEY_STR + history
                else:
                    ans_history = history
        user.filled_QN = ans_history
        user.save()
        response = {'status_code':1,'message':'fk'}
        return JsonResponse(response)
    else:
        response = {'status_code': -2, 'message': '请求错误'}
        return JsonResponse(response)

# 获取用户问卷购买记录
@csrf_exempt
@api_view(['POST'])
def get_bought(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        user_name = data['user_name']
        try:
            user = User.objects.get(username=user_name)
        except:
            response = {'status_code':2,'message':'fk'}
            return JsonResponse(response)
        all_bought = user.bought_QN
        bought_list = all_bought.split(KEY_STR)
        blocks = []
        for bought in bought_list:
            try:
                survey = Survey.objects.get(survey_id=int(bought))
            except:
                response = {'status_code':3,'message':'问卷不存在'}
                return JsonResponse(response)
            tmp = {}
            tmp['id'] = survey.survey_id
            tmp['title'] = survey.title
            tmp['state'] = survey.is_released
            tmp['used_time'] = survey.recycling_num
            tmp['type'] = survey.type
            blocks.append(tmp)
        response = {'status_code':1,'blocks':blocks}
        return JsonResponse(response)
    else:
        response = {'status_code': -2, 'message': '请求错误'}
        return JsonResponse(response)

# 发布问卷至广场
@csrf_exempt
@api_view(['POST'])
def release_to_square(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        qn_id = data['qn_id']
        try:
            survey = Survey.objects.get(survey_id=qn_id)
        except:
            response = {'status_code': 2, 'message': 'fk'}
            return JsonResponse(response)
        survey.is_square = True
        survey.save()
        response = {'status_code':1,'message':'good'}
        return JsonResponse(response)
    else:
        response = {'status_code': -2, 'message': '请求错误'}
        return JsonResponse(response)

# 获取广场问卷数据
@csrf_exempt
@api_view(['POST'])
def get_square_survey_data(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        user_name = data['user_name']
        try:
            user = User.objects.get(username=user_name)
        except:
            response = {'status_code':2, 'message': 'fk'}
            return JsonResponse(response)
        list1 = []
        surveys = Survey.objects.all().order_by('survey_id')
        for survey in surveys:
            if survey.is_deleted:
                continue
            if not survey.is_square:
                continue
            damn = {}
            damn['id'] = survey.survey_id
            damn['title'] = survey.title
            damn['type'] = survey.type
            if survey.is_released:
                damn['state'] = 1
            else:
                damn['state'] = 0
            damn['used_time'] = survey.recycling_num
            list1.append(damn)
        list2 = []
        list3 = []
        list4 = []
        list5 = []
        boughts = user.bought_QN
        bought_list = boughts.split(KEY_STR)
        if boughts:
            for bought in bought_list:
                id = int(bought)
                try:
                    survey = Survey.objects.get(survey_id=id)
                except:
                    response = {'status_code': 3, 'message': 'fk'}
                    return JsonResponse(response)
                damn = {}
                damn['id'] = survey.survey_id
                list2.append(damn)
        collections = user.collection
        collection_list = collections.split(KEY_STR)
        if collections:
            for collection in collection_list:
                id = int(collection)
                try:
                    survey = Survey.objects.get(survey_id=id)
                except:
                    response = {'status_code': 3, 'message': 'fk'}
                    return JsonResponse(response)
                damn = {}
                damn['id'] = survey.survey_id
                list3.append(damn)
        histories = user.filled_QN
        history_list = histories.split(KEY_STR)
        if histories:
            for history in history_list:
                id = int(history)
                try:
                    survey = Survey.objects.get(survey_id=id)
                except:
                    response = {'status_code': 3, 'message': 'fk'}
                    return JsonResponse(response)
                damn = {}
                damn['id'] = survey.survey_id
                damn['title'] = survey.title
                damn['type'] = survey.type
                if survey.is_released:
                    damn['state'] = 1
                else:
                    damn['state'] = 0
                damn['used_time'] = survey.recycling_num
                list4.append(damn)
        histories = user.filled_QN
        history_list = histories.split(KEY_STR)
        if histories:
            for history in history_list:
                id = int(history)
                try:
                    survey = Survey.objects.get(survey_id=id)
                except:
                    response = {'status_code': 3, 'message': 'fk'}
                    return JsonResponse(response)
                damn = {}
                damn['id'] = survey.survey_id
                damn['title'] = survey.title
                damn['type'] = survey.type
                if survey.is_released:
                    damn['state'] = 1
                else:
                    damn['state'] = 0
                damn['used_time'] = survey.recycling_num
                list4.append(damn)
        surveys = Survey.objects.filter(user_id=user.user_id).order_by('survey_id')
        for survey in surveys:
            if survey.is_deleted:
                continue
            damn = {}
            damn['id'] = survey.survey_id
            list5.append(damn)
        response = {'status_code':1,'list1':list1,'list2':list2,'list3': list3,'list4':list4,'list5':list5}
        return JsonResponse(response)
    else:
        response = {'status_code': -2, 'message': '请求错误'}
        return JsonResponse(response)

# 购买问卷
@csrf_exempt
@api_view(['POST'])
def buy_survey(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        qn_id = data['qn_id']
        user_name = data['user_name']
        try:
            user = User.objects.get(username=user_name)
        except:
            response = {'status_code':2,'message':'fk'}
            return JsonResponse(response)
        add_bought = str(qn_id)
        boughts = user.bought_QN
        if boughts == '':
            user.bought_QN = add_bought
        else:
            user.bought_QN = user.bought_QN + KEY_STR + add_bought
        user.Flash_coin = user.Flash_coin - 3
        user.save()
        response = {'status_code':1,'message':'good'}
        return JsonResponse(response)
    else:
        response = {'status_code': -2, 'message': '请求错误'}
        return JsonResponse(response)