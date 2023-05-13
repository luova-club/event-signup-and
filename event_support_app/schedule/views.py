from django.shortcuts import render
from .models import Schedule


def event_schedule(request):
    event_schedule = Schedule.objects.filter()
    context = {'schedule': event_schedule}
    return render(request, 'event_schedule.html', context)
