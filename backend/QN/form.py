from django import forms
from django.forms import formset_factory

class SurveyIdForm(forms.Form):
    qn_id = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control'}))



class CreateOptionForm(forms.Form):
    content = forms.CharField(max_length=256)  # 选项内容/描述

OptionFormSet = formset_factory(CreateOptionForm, extra=5)

class CreateQuestionForm(forms.Form):
    type = forms.IntegerField()  # 题目类型
    arg1 = forms.IntegerField(required=False)  # 参数1
    arg2 = forms.IntegerField(required=False)  # 参数2
    content = forms.CharField(max_length=256)  # 题目内容/描述
    options = OptionFormSet()  # 使用 FormSet 表示选项列表

QuestionFormSet = formset_factory(CreateQuestionForm, extra=5)

class CreateNewQnForm(forms.Form):
    username = forms.CharField(label="用户名", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))#问卷所属用户
    title = forms.CharField(label="标题", max_length=128,required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))#问卷标题
    description = forms.CharField(label="简介", max_length=256,required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))#问卷简介
    type = forms.CharField(label="类型", max_length=32, widget=forms.TextInput(attrs={'class': 'form-control'}))#问卷类型
    list = QuestionFormSet()  # 问卷的题目列表，以JSON格式保存
    finished_time = forms.DateTimeField(label="截止时间")
    do_time = forms.DateTimeField(label="填写时间")

class CreateNewQnForm_new(forms.Form):
    username = forms.CharField(label="用户名", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))#问卷所属用户
    title = forms.CharField(label="标题", max_length=128,required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))#问卷标题
    description = forms.CharField(label="简介", max_length=256,required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))#问卷简介
    type = forms.CharField(label="类型", max_length=32, widget=forms.TextInput(attrs={'class': 'form-control'}))#问卷类型
    list = QuestionFormSet()  # 问卷的题目列表，以JSON格式保存
    old_ID = forms.IntegerField(label="旧问卷ID")
    finished_time = forms.DateTimeField(label="截止时间")



