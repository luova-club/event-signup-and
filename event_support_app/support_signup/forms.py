from django import forms
from .models import Participant, Role
from django.utils.translation import gettext as _

class ParticipantForm(forms.ModelForm):
    role = forms.ModelChoiceField(queryset=Role.objects.all(), empty_label=None, widget=forms.Select(attrs={'class': 'form-select', 'aria-label': 'Role'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Sort shifts per day

        if 'role' in self.data:
            try:
                role_id = int(self.data.get('role'))
                role = Role.objects.get(id=role_id)
            except (ValueError, TypeError, Role.DoesNotExist):
                pass
        elif self.instance.pk:
            self.fields['shifts'].queryset = self.instance.role.shifts.all().order_by('date', 'start_time')

    class Meta:
        model = Participant
        fields = ['name', 'email', 'shifts', 'role']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Nickname')}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': _('Email')}),
            'shifts': forms.SelectMultiple(attrs={'class': 'form-select', 'aria-label': 'Shifts'})
        }
