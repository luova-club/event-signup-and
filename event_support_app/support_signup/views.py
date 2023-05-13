from django.conf import settings
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.utils.crypto import get_random_string
from django.utils.translation import activate, get_language, gettext_lazy as _
from django.views import View
from django.views.decorators.http import require_GET
from django.views.generic.edit import CreateView

from .forms import ParticipantForm
from .models import Role, Schedule, Shift, Participant, ParticipantShift, RoleShift

class LanguageSwitchView(View):
    def post(self, request, *args, **kwargs):
        lang_code = kwargs.get('lang_code')
        activate(lang_code)
        request.LANGUAGE_CODE = lang_code

        set_language(request)
        # set_language(lang_code)
        redirect_url = request.META.get(
            'HTTP_REFERER', reverse('participant_create'))
        return redirect(redirect_url)


def thank(request):
    return render(request, 'thank_you.html')


def home(request):
    return render(request, 'support_signup/home.html')


def about(request):
    return render(request, 'support_signup/about.html')


def event_schedule(request):
    event_schedule = Schedule.objects.filter()
    context = {'schedule': event_schedule}
    return render(request, 'event_schedule.html', context)

# views.py

from django.shortcuts import render
from .models import Role, Shift

from django.shortcuts import render
from .models import Role

def role_list(request):
    roles = Role.objects.all()
    context = {'roles': roles}
    return render(request, 'role_list.html', context)


from django.http import JsonResponse
from django.views.decorators.http import require_GET
from .models import RoleShift


@require_GET
def get_shifts_for_role(request, role_id):
    shifts = RoleShift.objects.filter(role_id=role_id)
    data = [{'id': shift.shift.id, 'date': shift.shift.date.strftime('%Y-%m-%d'),
             'start_time': shift.shift.start_time.strftime('%H:%M:%S'),
             'end_time': shift.shift.end_time.strftime('%H:%M:%S')} for shift in shifts]
    return JsonResponse(data, safe=False)


class ParticipantCreateView(CreateView):
    model = Participant
    form_class = ParticipantForm
    success_url = reverse_lazy('thank_you')

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

        # Generate confirmation token
        token = get_random_string(length=32)

        # Save token to participant model
        participant.token = token
        participant.save()

        # Send confirmation email
        subject = _('Confirm your attendance')
        message = _('Please confirm your attendance by clicking on the following link: http://%s%s') % (
            self.request.get_host(), reverse('confirm_attendance', args=[token]))

        from_email = "info@chillauskeskus.luova.club"
        recipient_list = [participant.email]
        send_mail(subject, message, from_email,
                  recipient_list, fail_silently=False)

        return super().form_valid(form)


class ParticipantConfirmView(View):
    def get(self, request, token):
        participant = Participant.objects.get(token=token)
        participant.is_confirmed = True
        participant.save()
        return redirect('home')
