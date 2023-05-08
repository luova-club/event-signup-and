from django.contrib import admin
from .models import SupportRoleShift, Participant, Role, ParticipantShift

class ParticipantShiftInline(admin.TabularInline):
    model = ParticipantShift

class ParticipantAdmin(admin.ModelAdmin):
    inlines = (ParticipantShiftInline,)

admin.site.register(SupportRoleShift)
admin.site.register(Role)
admin.site.register(Participant, ParticipantAdmin)
