from django.urls import path
from django.views.i18n import set_language
from .views import (
    ParticipantCreateView,
    LanguageSwitchView,
    home,
    ParticipantConfirmView
)
from . import views


urlpatterns = [
    path('create/', ParticipantCreateView.as_view(), name='participant_create'),
    path('', home, name='home'),
    path('schedule/', views.event_schedule, name='schedule'),
    path('about/', views.about, name='about'),
    path('confirm/<str:token>', ParticipantConfirmView.as_view(),
         name='confirm_attendance'),
    path('thank_you', views.thank, name="thank_you")

]
