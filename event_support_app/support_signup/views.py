from django.shortcuts import render
from .models import RoleShift
from .models import Role
from .models import Role, Shift
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
from .models import Role, Shift, Participant, ParticipantShift, RoleShift


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


def role_list(request):
    roles = Role.objects.all()
    context = {'roles': roles}
    return render(request, 'role_list.html', context)


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

    def shifts_to_list(self, shiftit: list):
        shifts = ""
        for shift in shiftit:
            # Create a string representation of the shift
            shift_str = f"{str(shift)},"
            
            # Add the string representation to the list
            shifts += shift_str

        return shifts

    def form_valid(self, form):
        participant = form.save(commit=False)
        participant.save()
        shifts = form.cleaned_data.get('shifts', [])
        for shift in shifts:
            ParticipantShift.objects.create(
                participant=participant,
                shift=shift
            )
        role = form.cleaned_data.get('role')
        role = Role.objects.get(name=role)
        participant.role = role

        # Generate confirmation token
        token = get_random_string(length=32)

        # Save token to participant model
        participant.token = token
        participant.save()

        # Send confirmation email
        subject = _('Confirm your attendance')
        message = _('Thank you for signing up to help Chillauskeskus in a role `%s` in shifts: \n%s \n') % (str(role), self.shifts_to_list(shifts))
        
        message += f"{_('Please confirm your attendance by clicking on the following link:')}https://{self.request.get_host()}{reverse('confirm_attendance', args=[token])}"

        message += _('If you have any questions, you can ask them by replying to this email\n')
        
        message += _("""
        Kind regards, Oliver
        
        Oliver Vuorenmaa
        Coordinator, XR Youth Finland (Elokapina nuoret)
        Interim Head Coordinator, Chillauskeskus
        +358442378588
        vuoreol@gmail.com
        """)

 
        from_email = "info@chillauskeskus.luova.club"
        recipient_list = [participant.email]
        send_mail(subject, message, from_email,
                  recipient_list, fail_silently=False)

        return super().form_valid(form)


class ParticipantConfirmView(View):
    def shifts_to_list(self, shiftit: list):
        shifts = ""
        for shift in shiftit:
            # Create a string representation of the shift
            shift_str = f"{shift.date} {shift.start_time}-{shift.end_time},"
            
            # Add the string representation to the list
            shifts += shift_str

        return shifts

    def get(self, request, token):
        participant = Participant.objects.get(token=token)
        participant.is_confirmed = True
        participant.save()

        
        # Send confirmation email
        subject = _('Thank you for confirming your participation!')
        message = ''
        
        message += _('Thank you for confirming your participation to Chillauskeskus for the following role: %s\n in the following shifts: \n%s') % (str(participant.role), self.shifts_to_list(participant.shifts))

        message += _('If you have any questions, you can ask them by replying to this email')

        message += _("""
        Kind regards, Oliver
        
        Oliver Vuorenmaa
        Coordinator, XR Youth Finland (Elokapina nuoret)
        Interim Head Coordinator, Chillauskeskus
        +358442378588
        vuoreol@gmail.com
        """)

        from_email = "info@chillauskeskus.luova.club"
        recipient_list = [participant.email]
        send_mail(subject, message, from_email,
                  recipient_list, fail_silently=False)

        return redirect('home')
