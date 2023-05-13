from django.db import models
import uuid
from django.utils import timezone
from django.urls import reverse


class Schedule(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
        return self.title


class Shift(models.Model):
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.date} {self.start_time}-{self.end_time}"


class Role(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    shifts = models.ManyToManyField(Shift, through='RoleShift')

    def __str__(self):
        return f'{self.name}'


class RoleShift(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    shift = models.ForeignKey(Shift, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.role} - {self.shift}'


class Participant(models.Model):
    # existing fields
    name = models.CharField(max_length=255)
    email = models.EmailField()
    shifts = models.ManyToManyField(Shift, through='ParticipantShift')

    token = models.CharField(max_length=100)
    is_confirmed = models.BooleanField(default=False)


class ParticipantShift(models.Model):
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    shift = models.ForeignKey(Shift, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('participant', 'shift')

    def __str__(self):
        return f'{self.participant} - {self.role} - {self.shift}'
