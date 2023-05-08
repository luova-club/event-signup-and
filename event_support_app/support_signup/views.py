from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from .models import SupportRoleShift, Participant, Role, ParticipantShift
from .forms import ParticipantForm

class ParticipantListView(ListView):
    model = Participant

class ParticipantCreateView(CreateView):
    model = Participant
    form_class = ParticipantForm
    success_url = reverse_lazy('participant_list')

    def form_valid(self, form):
        participant = form.save(commit=False)
        participant.save()
        shifts = form.cleaned_data.get('shifts', [])
        for shift in shifts:
            role = form.cleaned_data.get('role')
            role = Role.objects.get(name=role)
            ParticipantShift.objects.create(
                participant=participant,
                role=role,
                shift=shift
            )
        return redirect(self.success_url)

class ParticipantUpdateView(UpdateView):
    model = Participant
    form_class = ParticipantForm
    success_url = reverse_lazy('participant_list')

    def form_valid(self, form):
        participant = form.save(commit=False)
        participant.save()
        shifts = form.cleaned_data.get('shifts', [])
        ParticipantShift.objects.filter(participant=participant).delete()
        for shift in shifts:
            ParticipantShift.objects.create(
                participant=participant,
                role=shift['role'],
                shift=shift['shift']
            )
        return redirect(self.success_url)

class ParticipantDeleteView(DeleteView):
    model = Participant
    success_url = reverse_lazy('participant_list')
