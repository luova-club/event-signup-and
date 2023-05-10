from django.urls import path
from django.views.i18n import set_language
from .views import (
    ParticipantCreateView,
    ParticipantUpdateView,
    ParticipantDeleteView,
    LanguageSwitchView,
    home
)
from . import views


urlpatterns = [
    path('create/', ParticipantCreateView.as_view(), name='participant_create'),
    path('', home, name='home'),
    path('<int:pk>/update/', ParticipantUpdateView.as_view(), name='participant_update'),
    path('<int:pk>/delete/', ParticipantDeleteView.as_view(), name='participant_delete'),
    path('schedule/', views.event_schedule, name='schedule'),
    path('about/', views.about, name='about')

]