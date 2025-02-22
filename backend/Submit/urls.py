from django.urls import path
from .views import *


urlpatterns = [
    path('create_QN', create_qn),  # 创建问卷
    path('fill_in_qn_FS', fill_in_QN_FS),  # 填写问卷第一步
    path('fill_in_qn_SE', fill_in_QN_SE),  # 填写问卷第二部
    path('deploy_qn', deploy_qn),  # 发布问卷
    path('pause_qn', pause_qn),  # 下架问卷
    path('delete_survey_not_real', delete_survey_not_real),  # 将问卷放入回收站
    path('get_survey_data', get_survey_data),  # 获取所有未放入回收站问卷的信息
    path('get_survey_in_recyclebin_data', get_survey_in_recyclebin_data),  # 获取所有放入回收站问卷的信息
    path('recover_survey_from_delete', recover_survey_from_delete),  # 将回收站中的问卷恢复
    path('delete_survey_real', delete_survey_real),  # 将回收站中的问卷彻底删除
    path('delete_all_survey_real', delete_all_survey_real),  # 将回收站中的所有问卷一键彻底删除
    path('cross_analyse_FS', cross_analyse_FS),  # 交叉分析第一步
    path('cross_analyse_SE', cross_analyse_SE),  # 交叉分析第二步
    path('copy_survey', copy_survey),  # 复制问卷
    path('edit_survey_FS', edit_survey_FS),  # 编辑问卷第一步
    path('edit_survey_SE', edit_survey_SE),  # 编辑问卷第二步
    path('data_analysis_FS', data_analysis_FS),  # 数据分析第一步
    path('data_analysis_SE',data_analysis_SE),  # 数据分析第二步
    path('data_analysis_TH',data_analysis_TH),  # 数据分析第三步
    path('release_to_square',release_to_square),  # 发布问卷到广场
    path('get_square_survey_data',get_square_survey_data),  # 获取所有广场上问卷的信息以及该用户已收藏的问卷的ID
    path('collect_survey',collect_survey),  # 收藏问卷
    path('buy_survey', buy_survey),  # 购买问卷
    path('cancel_collections',cancel_collections),  # 取消收藏
    path('get_history',get_history) # 获取用户填写历史记录
]