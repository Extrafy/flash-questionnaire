from django.db import models

# Create your models here.
class User(models.Model):
    user_id = models.AutoField(primary_key=True,verbose_name="user_id")  # 用户ID
    username = models.CharField(max_length=128, unique=True)#用于存储用户名，必须是唯一的
    email = models.EmailField(unique=True)#用于存储用户电子邮件地址，且必须是唯一的
    password = models.CharField(max_length=256)#用于存储用户密码
    url = models.CharField(max_length=128, blank=True)#用户存储头像地址

    user_desc = models.CharField(max_length=500, blank=True)#用于存储用户描述信息，可以为空

    c_time = models.DateTimeField(auto_now_add=True)#用于存储用户创建时间，在用户创建时自动添加当前时间
    has_confirmed = models.BooleanField(default=False)#表示用户是否已确认，初始值为 False
    Flash_coin = models.IntegerField(default=0)
    collection = models.CharField(max_length=128, blank=True) #收藏的问卷ID
    filled_QN = models.CharField(max_length=128, blank=True) #填写的问卷ID
    bought_QN = models.CharField(max_length=128, blank=True) #购买的问卷ID


class ConfirmString(models.Model):
    code = models.CharField(max_length=256)#用于存储确认码
    user = models.OneToOneField('User', on_delete=models.CASCADE)#与 User 模型关联，表示这个确认码对应的用户。当用户被删除时，相应的确认码也会被删除
    c_time = models.DateTimeField(auto_now_add=True)#用于存储确认码创建时间，在确认码创建时自动添加当前时间。

    def __str__(self):
        return self.user.username + ": " + self.code

    class Meta:
        db_table = 'tb_confirmCode'#数据库表名
        ordering = ['-c_time']#排序方式
        verbose_name = '确认码'
        verbose_name_plural = verbose_name