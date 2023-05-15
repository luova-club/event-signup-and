from .models import Shift, Role, RoleShift
from django.utils import timezone
from django.db import models
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Participant, Role, ParticipantShift
from django.contrib import admin
from django import forms
from datetime import datetime


class ParticipantShiftInline(admin.TabularInline):
    model = ParticipantShift


class TimeInput(forms.TimeInput):
    input_type = 'time'

    def format_value(self, value):
        if isinstance(value, int):
            # Convert integer input to HH:MM format
            return f'{value:02}:00:00'
        return super().format_value(value)


class ShiftInline(admin.TabularInline):
    model = Role.shifts.through


class RoleShiftInline(admin.TabularInline):
    model = RoleShift


class ShiftAdmin(admin.ModelAdmin):
    inlines = [RoleShiftInline]


class RoleAdmin(admin.ModelAdmin):
    inlines = [ShiftInline, RoleShiftInline]


admin.site.register(Shift, ShiftAdmin)
admin.site.register(Role, RoleAdmin)


@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'role')
    search_fields = ('name', 'email', 'role')
    inlines = [ParticipantShiftInline]


@admin.register(ParticipantShift)
class ParticipantShiftAdmin(admin.ModelAdmin):
    list_display = ('participant', 'shift')
    search_fields = ('participant__name', 'shift__date')
    list_filter = ['shift__date']
