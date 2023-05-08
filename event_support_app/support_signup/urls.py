from django.urls import path

from .views import (
    ParticipantListView,
    ParticipantCreateView,
    ParticipantUpdateView,
    ParticipantDeleteView,
)

urlpatterns = [
    path('', ParticipantListView.as_view(), name='participant_list'),
    path('create/', ParticipantCreateView.as_view(), name='participant_create'),
    path('<int:pk>/update/', ParticipantUpdateView.as_view(), name='participant_update'),
    path('<int:pk>/delete/', ParticipantDeleteView.as_view(), name='participant_delete'),
]
