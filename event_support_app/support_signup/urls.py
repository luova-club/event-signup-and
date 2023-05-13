from django.urls import path
from django.views.i18n import set_language
from .views import (
    ParticipantCreateView,
    LanguageSwitchView,
    home,
    ParticipantConfirmView,
    get_shifts_for_role
)
from . import views


urlpatterns = [
    path('create/', ParticipantCreateView.as_view(), name='participant_create'),
    path('', home, name='home'),
    path('about/', views.about, name='about'),
    path('confirm/<str:token>', ParticipantConfirmView.as_view(),
         name='confirm_attendance'),
    path('thank_you', views.thank, name="thank_you"),
    path("roles", views.role_list, name="role_list"),
    path('get_shifts_for_role/<int:role_id>/',
         get_shifts_for_role, name='get_shifts_for_role'),


]
