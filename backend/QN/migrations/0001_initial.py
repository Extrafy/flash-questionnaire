# Generated by Django 3.2.25 on 2024-05-27 12:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Survey',
            fields=[
                ('survey_id', models.AutoField(primary_key=True, serialize=False, verbose_name='id')),
                ('title', models.CharField(max_length=50, verbose_name='标题')),
                ('description', models.CharField(blank=True, max_length=256, verbose_name='简介')),
                ('question_num', models.PositiveIntegerField(default=0, verbose_name='题目数目')),
                ('recycling_num', models.PositiveIntegerField(default=0, verbose_name='回收数目')),
                ('max_recycling', models.PositiveIntegerField(default=999999, verbose_name='最大回收数目')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('release_time', models.DateTimeField(null=True, verbose_name='发布时间')),
                ('finished_time', models.DateTimeField(null=True, verbose_name='结束时间')),
                ('is_released', models.BooleanField(default=False, verbose_name='是否已发行')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='是否已删除')),
                ('is_collected', models.BooleanField(default=False, verbose_name='是否被收藏')),
                ('is_finished', models.BooleanField(default=False, verbose_name='是否已结束')),
                ('user_id', models.IntegerField(default=0, verbose_name='用户ID')),
                ('share_url', models.URLField(default='', verbose_name='分享链接')),
                ('type', models.CharField(default='0', max_length=32, verbose_name='问卷类型')),
            ],
        ),
        migrations.CreateModel(
            name='Submit',
            fields=[
                ('submit_id', models.AutoField(primary_key=True, serialize=False, verbose_name='提交编号')),
                ('submit_time', models.DateTimeField(auto_now_add=True, verbose_name='提交时间')),
                ('user_id', models.IntegerField(default=0, verbose_name='用户ID')),
                ('is_valid', models.BooleanField(default=True, verbose_name='答卷是否有效')),
                ('survey_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='QN.survey', verbose_name='问卷编号')),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('question_id', models.AutoField(primary_key=True, serialize=False, verbose_name='问题id')),
                ('title', models.CharField(blank=True, default='默认标题', max_length=64, verbose_name='标题')),
                ('description', models.CharField(blank=True, max_length=256, verbose_name='说明')),
                ('is_must_answer', models.BooleanField(default=False, verbose_name='是必答题')),
                ('sequence', models.IntegerField(default=0, verbose_name='题目顺序')),
                ('option_num', models.PositiveIntegerField(default=0, verbose_name='选项数目')),
                ('arg1', models.PositiveIntegerField(default=1, verbose_name='选项上限数量')),
                ('arg2', models.PositiveIntegerField(default=1, verbose_name='选项下限数量')),
                ('type', models.CharField(default='0', max_length=256, verbose_name='问题类型')),
                ('right_answer', models.CharField(default='', max_length=256, verbose_name='正确答案')),
                ('has_image', models.BooleanField(default=False, verbose_name='包含图片')),
                ('has_video', models.BooleanField(default=False, verbose_name='包含视频')),
                ('image_url', models.CharField(blank=True, default='', max_length=1024, verbose_name='图片链接')),
                ('video_url', models.CharField(blank=True, default='', max_length=1024, verbose_name='视频链接')),
                ('is_shown', models.BooleanField(default=True, verbose_name='展示题目')),
                ('survey_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='QN.survey', verbose_name='所属问卷id')),
            ],
        ),
        migrations.CreateModel(
            name='Option',
            fields=[
                ('option_id', models.AutoField(primary_key=True, serialize=False, verbose_name='选项编号')),
                ('order', models.PositiveIntegerField(default=1, verbose_name='选项位置')),
                ('content', models.CharField(max_length=128, verbose_name='内容')),
                ('choosed', models.BooleanField(default=False, verbose_name='是否选中')),
                ('question_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='QN.question', verbose_name='问题编号')),
            ],
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('answer_id', models.AutoField(primary_key=True, serialize=False, verbose_name='回答编号')),
                ('answer', models.CharField(max_length=256, verbose_name='答案')),
                ('user_id', models.IntegerField(default=0, verbose_name='用户ID')),
                ('type', models.CharField(default='', max_length=32, verbose_name='问题类型')),
                ('question_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='QN.question', verbose_name='问题编号')),
                ('submit_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='QN.submit', verbose_name='提交编号')),
            ],
        ),
    ]
