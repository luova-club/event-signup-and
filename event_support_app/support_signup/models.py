from django.db import models
import uuid
from django.utils import timezone
from django.urls import reverse


class SupportRoleShift(models.Model):
    date = models.DateField(default=timezone.now)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f'{self.date} kello {self.start_time} - {self.end_time}'


class Schedule(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
        return self.title


class Participant(models.Model):
    # existing fields
    name = models.CharField(max_length=255)
    email = models.EmailField()
    shifts = models.ManyToManyField(SupportRoleShift, through='ParticipantShift')

    token = models.CharField(max_length=100)
    is_confirmed = models.BooleanField(default=False)


class Role(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.name}'

class ParticipantShift(models.Model):
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    shift = models.ForeignKey(SupportRoleShift, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('participant', 'shift')

    def __str__(self):
        return f'{self.participant} - {self.role} - {self.shift}'