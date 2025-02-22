from django.db import models
from User.models import *
# Create your models here.

# def question_image_directory_path(instance, filename):
#     # 文件上传到 MEDIA_ROOT/image/question_<id>/<filename>目录中
#     return 'image/question_{0}/{1}'.format(instance.question_id, filename)
#
#
# def question_video_directory_path(instance, filename):
#     # 文件上传到 MEDIA_ROOT/video/question_<id>/<filename>目录中
#     return 'video/question_{0}/{1}'.format(instance.question_id, filename)

class Survey(models.Model):
    survey_id = models.AutoField(primary_key=True,verbose_name="id")  # 问卷ID
    title = models.CharField(max_length=50,verbose_name="标题")  # 问卷标题
    description = models.CharField(max_length=256,verbose_name="简介",blank=True)  # 问卷简介

    question_num = models.PositiveIntegerField(default=0,verbose_name="题目数目")  # 问卷的题目数量
    recycling_num = models.PositiveIntegerField(default=0,verbose_name="回收数目")  # 问卷的回收数量
    max_recycling = models.PositiveIntegerField(default=999999,verbose_name="最大回收数目")  # 问卷的最大回收数量

    created_time = models.DateTimeField(auto_now_add=True,verbose_name="创建时间")  # 问卷创建时间
    release_time = models.DateTimeField(verbose_name="发布时间",null=True)  # 问卷的发布时间
    finished_time = models.DateTimeField(verbose_name="结束时间",null=True)  # 问卷的结束时间
    do_time = models.DateTimeField(verbose_name="填写时间", null=True)  # 问卷的填写时间
    is_released = models.BooleanField(default=False,verbose_name="是否已发行")  # 问卷的发行标志
    is_deleted = models.BooleanField(default=False,verbose_name="是否已删除")  # 问卷的删除标志
    is_collected = models.BooleanField(default=False, verbose_name="是否被收藏")  # 问卷的收藏标志
    is_finished = models.BooleanField(default=False, verbose_name="是否已结束")  # 问卷的结束标志
    is_square = models.BooleanField(default=False, verbose_name="是否已发布到广场") 
    # is_encrypted_pin = models.BooleanField(default=False)

    user_id = models.IntegerField(default=0,verbose_name="用户ID")

    share_url = models.URLField(verbose_name="分享链接",default='')  # 问卷的分享链接
    # docx_url = models.URLField(verbose_name="word链接",default='')
    # pdf_url = models.URLField(verbose_name="pdf链接", default='')
    # excel_url = models.URLField(verbose_name="答卷数据统计excel链接",default='')
    type = models.CharField(max_length=32, verbose_name="问卷类型", default='0')  # 问卷类型
    SURVEY_TYPE_CHOICES = [
        (0,'调查问卷'),
        (1,'考试问卷'),
        (2,'投票问卷'),
        (3,'报名问卷'),
    ]
    # is_logic = models.BooleanField(default=False,verbose_name="是否存在逻辑问题")


class Question(models.Model):

    question_id = models.AutoField(primary_key=True,verbose_name="问题id")  # 问题ID
    title = models.CharField(max_length=64,verbose_name="标题",blank=True,default='默认标题')  # 问题标题
    description = models.CharField(max_length=256,blank=True,verbose_name="说明")  # 问题说明
    is_must_answer = models.BooleanField(default=False,verbose_name="是必答题")  # 问题是否是必答题
    survey_id = models.ForeignKey(Survey,on_delete=models.CASCADE,verbose_name="所属问卷id")  # 问题所属问卷ID
    sequence = models.IntegerField(default=0,verbose_name="题目顺序")  # 问题题目顺序
    option_num = models.PositiveIntegerField(default=0,verbose_name="选项数目")  # 问题的选项数量

    arg1 = models.PositiveIntegerField(default=1,verbose_name="选项上限数量")
    arg2 = models.PositiveIntegerField(default=1,verbose_name="选项下限数量")
    arg3 = models.CharField(max_length=1024, verbose_name="第三选项", blank=True, default='')
    type = models.CharField(max_length=256,verbose_name="问题类型",default='0')
    right_answer = models.CharField(max_length=256,verbose_name="正确答案",default='')

    has_image = models.BooleanField(default=False, verbose_name="包含图片")
    has_video = models.BooleanField(default=False, verbose_name="包含视频")
    image_url = models.CharField(max_length=1024,verbose_name="图片链接",blank=True,default='')
    video_url = models.CharField(max_length=1024,verbose_name="视频链接",blank=True,default='')

    is_shown = models.BooleanField(default=True, verbose_name="展示题目")

    TYPE_CHOICES = [
        (0, '单选'),
        (1, '多选'),
        (2, '评分'),
        (3, '填空'),
    ]


class Option(models.Model):
    option_id = models.AutoField(primary_key=True,verbose_name="选项编号")
    order = models.PositiveIntegerField(default=1,verbose_name="选项位置")
    #从1递增
    content = models.CharField(max_length=128,verbose_name="内容")
    question_id  = models.ForeignKey(Question, on_delete=models.CASCADE,verbose_name="问题编号")
    choosed = models.BooleanField(default=False, verbose_name="是否选中")
    max_num = models.IntegerField(default=0,verbose_name="最大填写数量")
    left_num = models.IntegerField(default=0,verbose_name="剩余填写数量")


class Submit(models.Model):
    submit_id = models.AutoField(primary_key=True,verbose_name="提交编号")
    survey_id = models.ForeignKey(Survey,on_delete=models.CASCADE,verbose_name="问卷编号")
    submit_time = models.DateTimeField(auto_now_add=True,verbose_name="提交时间")
    user_id = models.IntegerField(default=0,verbose_name="用户ID")
    is_valid = models.BooleanField(default=True,verbose_name="答卷是否有效")



class Answer(models.Model):
    answer_id = models.AutoField(primary_key=True,verbose_name="回答编号")
    question_id = models.ForeignKey(Question, on_delete=models.CASCADE,verbose_name="问题编号")
    submit_id = models.ForeignKey(Submit, on_delete=models.CASCADE,verbose_name="提交编号")
    answer = models.CharField(max_length=256,verbose_name="答案")
    user_id = models.IntegerField(default=0,verbose_name="用户ID")
    TYPE_CHOICES = [
        (0, '单选'),
        (1, '多选'),
        (2, '评分'),
        (3, '填空'),
    ]
    type = models.CharField(max_length=32, verbose_name="问题类型",default='')


