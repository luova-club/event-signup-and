
from django import forms
from .models import Participant, Role, SupportRoleShift
from django.utils.translation import gettext as _


class ParticipantForm(forms.ModelForm):
    role = forms.ModelChoiceField(queryset=Role.objects.all(), empty_label=None, widget=forms.Select(attrs={'class': 'form-select', 'aria-label': 'Role'}))
    shifts = forms.ModelMultipleChoiceField(queryset=SupportRoleShift.objects.all(), widget=forms.SelectMultiple(attrs={'class': 'form-select', 'aria-label': 'Shifts'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Sort shifts per day
        self.fields['shifts'].queryset = SupportRoleShift.objects.all().order_by('date', 'start_time')

    class Meta:
        model = Participant
        fields = ['name', 'email', 'shifts', 'role']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Nickname')}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': _('Email')}),
        }

