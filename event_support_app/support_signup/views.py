from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from django.views.i18n import set_language

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from .models import SupportRoleShift, Participant, Role, ParticipantShift
from .forms import ParticipantForm

from django.shortcuts import redirect
from django.urls import reverse
from django.views import View
from django.utils.translation import activate, get_language
from django.views.i18n import set_language
from django.conf import settings

class LanguageSwitchView(View):
    def post(self, request, *args, **kwargs):
        lang_code = kwargs.get('lang_code')
        print(get_language())
        activate(lang_code)
        print(lang_code)
        print(request.LANGUAGE_CODE)
        request.LANGUAGE_CODE = lang_code
        print(request.LANGUAGE_CODE)

        set_language(request)
        #set_language(lang_code)
        redirect_url = request.META.get('HTTP_REFERER', reverse('participant_create'))
        return redirect(redirect_url)


def home(request):
    return render(request, 'support_signup/home.html')

def about(request):
    return render(request, 'support_signup/about.html')

from django.shortcuts import render
from .models import Schedule

def event_schedule(request):
    event_schedule = Schedule.objects.filter()
    context = {'schedule': event_schedule}
    return render(request, 'event_schedule.html', context)


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
            role = form.cleaned_data.get('role')
            role = Role.objects.get(name=role)
            ParticipantShift.objects.create(
                participant=participant,
                role=role,
                shift=shift
            )
        return render(self.request, "thank_you.html")

class ParticipantDeleteView(DeleteView):
    model = Participant
    success_url = reverse_lazy('participant_list')
