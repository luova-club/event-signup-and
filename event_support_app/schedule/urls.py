from django.urls import path
from django.views.i18n import set_language
from .views import (
    event_schedule
)

urlpatterns = [
    path('', event_schedule, name='schedule'),
]
