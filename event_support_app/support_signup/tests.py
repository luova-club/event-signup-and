from datetime import date, time, timedelta

from django.test import TestCase

from .models import Participant, ParticipantShift, Role, SupportRoleShift
from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from .models import Participant, ParticipantShift, Role, SupportRoleShift


class SupportRoleShiftModelTests(TestCase):

    def test_support_role_shift_str(self):
        shift_date = date(2023, 5, 15)
        start_time = time(9, 0)
        end_time = time(12, 0)
        shift = SupportRoleShift(
            date=shift_date, start_time=start_time, end_time=end_time)
        self.assertEqual(
            str(shift), f'{shift_date} kello {start_time} - {end_time}')


class ParticipantModelTests(TestCase):

    def setUp(self):
        self.participant = Participant.objects.create(
            name='John', email='john@example.com')

    def test_participant_str(self):
        self.assertEqual(str(self.participant), 'John')


class RoleModelTests(TestCase):

    def setUp(self):
        self.role = Role.objects.create(
            name='Test Role', description='A test role')

    def test_role_str(self):
        self.assertEqual(str(self.role), 'Test Role')


class ParticipantShiftModelTests(TestCase):

    def setUp(self):
        self.shift_date = date.today()
        self.start_time = time(hour=10)
        self.end_time = time(hour=12)
        self.shift = SupportRoleShift.objects.create(
            date=self.shift_date, start_time=self.start_time, end_time=self.end_time)
        self.role = Role.objects.create(
            name='Test Role', description='A test role')
        self.participant = Participant.objects.create(
            name='John', email='john@example.com')
        self.participant_shift = ParticipantShift.objects.create(
            participant=self.participant, role=self.role, shift=self.shift)

    def test_participant_shift_str(self):
        self.assertEqual(str(self.participant_shift),
                         f'{self.participant} - {self.role} - {self.shift}')

    def test_participant_shift_unique_together(self):
        with self.assertRaises(Exception):
            ParticipantShift.objects.create(
                participant=self.participant, role=self.role, shift=self.shift)


class ParticipantViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser', password='testpass')
        self.participant = Participant.objects.create(
            name='Test Participant', email='test@test.com')
        self.role = Role.objects.create(name='Test Role')

        self.shift = SupportRoleShift.objects.create(date=date(2023, 5, 15),
            start_time=time(9, 0), end_time=time(12, 0))
        self.participant_shift = ParticipantShift.objects.create(
            participant=self.participant, role=self.role, shift=self.shift)

    def test_participant_list_view(self):
        response = self.client.get(reverse('participant_list'))
        self.assertEqual(response.status_code, 200)
        #self.assertTemplateUsed(response, 'participant_list.html, base.html')

    def test_participant_create_view(self):
        self.client.login(username='testuser', password='testpass')
        data = {
            'name': 'New Participant',
            'email': 'new@test.com',
            'role': self.role.id,
            'shifts': [self.shift.id]
        }
        response = self.client.post(reverse('participant_create'), data=data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('participant_list'))
        participant = Participant.objects.last()
        self.assertEqual(participant.name, 'New Participant')
        self.assertEqual(participant.email, 'new@test.com')
        participant_shift = ParticipantShift.objects.last()
        self.assertEqual(participant_shift.participant, participant)
        self.assertEqual(participant_shift.role, self.role)
        self.assertEqual(participant_shift.shift, self.shift)

    def test_participant_update_view(self):
        self.client.login(username='testuser', password='testpass')
        data = {
            'name': 'Updated Participant',
            'email': 'updated@test.com',
            'role': self.role.id,
            'shifts': [self.shift.id]
        }
        response = self.client.post(reverse('participant_update', args=[
                                    self.participant.id]), data=data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('participant_list'))
        participant = Participant.objects.get(id=self.participant.id)
        self.assertEqual(participant.name, 'Updated Participant')
        self.assertEqual(participant.email, 'updated@test.com')
        participant_shifts = ParticipantShift.objects.filter(
            participant=participant)
        self.assertEqual(len(participant_shifts), 1)
        participant_shift = participant_shifts.first()
        self.assertEqual(participant_shift.role, self.role)
        self.assertEqual(participant_shift.shift, self.shift)

    def test_participant_delete_view(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(
            reverse('participant_delete', args=[self.participant.id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('participant_list'))
        participant = Participant.objects.filter(id=self.participant.id)
        self.assertEqual(len(participant), 0)
        participant_shift = ParticipantShift.objects.filter(
            id=self.participant_shift.id)
        self.assertEqual(len(participant_shift), 0)
