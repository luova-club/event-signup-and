from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import SupportRoleShift, Participant, Role, ParticipantShift
from django.contrib import admin
from django import forms
from datetime import datetime

from .models import SupportRoleShift


class ParticipantShiftInline(admin.TabularInline):
    model = ParticipantShift


from django import forms
from django.contrib import admin
from django.db import models
from django.utils import timezone


class TimeInput(forms.TimeInput):
    input_type = 'time'

    def format_value(self, value):
        if isinstance(value, int):
            # Convert integer input to HH:MM format
            return f'{value:02}:00:00'
        return super().format_value(value)


class SupportRoleShiftForm(forms.ModelForm):
    class Meta:
        model = SupportRoleShift
        fields = '__all__'
        widgets = {
            'start_time': TimeInput(),
            'end_time': TimeInput(),
        }


class SupportRoleShiftAdmin(admin.ModelAdmin):
    form = SupportRoleShiftForm


admin.site.register(SupportRoleShift, SupportRoleShiftAdmin)


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')


@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = ('name', 'email')
    search_fields = ('name', 'email')
    inlines = [ParticipantShiftInline]


@admin.register(ParticipantShift)
class ParticipantShiftAdmin(admin.ModelAdmin):
    list_display = ('participant', 'role', 'shift')
    search_fields = ('participant__name', 'role__name', 'shift__date')
    list_filter = ('shift__date', 'role__name')
