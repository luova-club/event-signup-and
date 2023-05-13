from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Participant, Role, ParticipantShift, Schedule
from django.contrib import admin
from django import forms
from datetime import datetime



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



# admin.py

from django.contrib import admin
from .models import Shift, Role, RoleShift

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
    list_display = ('name', 'email')
    search_fields = ('name', 'email')
    inlines = [ParticipantShiftInline]

@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_time', 'end_time')
    search_fields = ['title']

@admin.register(ParticipantShift)
class ParticipantShiftAdmin(admin.ModelAdmin):
    list_display = ('participant', 'role', 'shift')
    search_fields = ('participant__name', 'role__name', 'shift__date')
    list_filter = ('shift__date', 'role__name')
