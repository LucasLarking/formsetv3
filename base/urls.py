from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token

from .views import (
    home,
    surveyDetail,
    SurveyOption,
    SurveyTake,
    SurveyData,
    QuestionViewSet,
    questionAPI,
    surveyAPI,
    SurveyDetailAPIView,
    SurveyListCreateAPIView,
    SurveyUpdateAPIView,
    SurveyDeleteAPIView,
    SurveyMixinView,
    survey_alt_view,
    #  MOsh
    mosh_survey_detail,
    mosh_question_detail,
    mosh_questions,


)
router = routers.DefaultRouter()
router.register(r'questions', QuestionViewSet)

urlpatterns = [
    path('', home.as_view(), name='home'),
    path('surveydetail/<str:pk>', surveyDetail.as_view(), name='surveyDetail'),
    path('surveyoption/<str:pk>', SurveyOption.as_view(), name='surveyOption'),
    path('surveytake/<str:pk>', SurveyTake.as_view(), name='surveyTake'),
    path('surveydata/<str:pk>', SurveyData.as_view(), name='surveyData'),
    path('questionapi/<str:pk>', questionAPI.as_view(), name='questionapi'),
    path('surveyapi', surveyAPI.as_view(), name='surveyapi'),
    path('surveydetailapi/<int:pk>/', SurveyDetailAPIView.as_view(), name='surveydetailapi'),
    path('surveycreateapi/<int:pk>/', SurveyListCreateAPIView.as_view(), name='surveycreateapi'),
    path('surveyupdate/<int:pk>/', SurveyUpdateAPIView.as_view(), name='surveyupdate'),
    path('surveydelete/<int:pk>/', SurveyDeleteAPIView.as_view(), name='surveydelete'),
    path('surveymixinview/<int:pk>/', SurveyMixinView.as_view(), name='surveymixinview'),
    path('survey_alt_view/<int:pk>/', survey_alt_view, name='survey_alt_view'),
    path('auth/', obtain_auth_token, name='obtain_auth_token'),

    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('', include(router.urls)),
    #  MOsh

    path('mosh/survey_detail/<int:pk>/', mosh_survey_detail, name='survey-detail'),
    path('mosh/question_detail/<int:id>/', mosh_question_detail, name='mosh_question_detail'),
    path('mosh/questions', mosh_questions, name='mosh_questions'),

]
