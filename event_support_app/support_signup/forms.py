from django import forms
from .models import Participant, SupportRoleShift, Role


class ParticipantForm(forms.ModelForm):
    role = forms.ModelChoiceField(queryset=Role.objects.all(), empty_label=None)


    class Meta:
        model = Participant
        fields = ['name', 'email', 'shifts', 'role']
        widgets = {
            'shifts': forms.CheckboxSelectMultiple,
        }