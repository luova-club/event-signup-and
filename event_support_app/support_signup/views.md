# Participant Views

This module contains views for the `Participant` model.

## List View

`ParticipantListView` is a generic `ListView` that displays a list of all `Participant` objects.

```python
from django.views.generic import ListView
from .models import Participant

class ParticipantListView(ListView):
    model = Participant
```

## Create View

`ParticipantCreateView` is a generic `CreateView` that creates a new `Participant` object. It also creates `ParticipantShift` objects for each shift selected by the participant.

```python
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .models import Participant, Role, ParticipantShift
from .forms import ParticipantForm

class ParticipantCreateView(CreateView):
    model = Participant
    form_class = ParticipantForm
    success_url = reverse_lazy('participant_list')

    def form_valid(self, form):
        participant = form.save(commit=False)
        participant.save()
        shifts = form.cleaned_data.get('shifts', [])
        for shift in shifts:
            role = form.cleaned_data.get('role')
            role = Role.objects.get(name=role)
            ParticipantShift.objects.create(
                participant=participant,
                role=role,
                shift=shift
            )
        return redirect(self.success_url)
```

## Update View

`ParticipantUpdateView` is a generic `UpdateView` that updates an existing `Participant` object. It also updates `ParticipantShift` objects for the participant's shifts.

```python
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy
from .models import Participant, Role, ParticipantShift
from .forms import ParticipantForm

class ParticipantUpdateView(UpdateView):
    model = Participant
    form_class = ParticipantForm
    success_url = reverse_lazy('participant_list')

    def form_valid(self, form):
        participant = form.save(commit=False)
        participant.save()
        shifts = form.cleaned_data.get('shifts', [])
        ParticipantShift.objects.filter(participant=participant).delete()
        for shift in shifts:
            role = form.cleaned_data.get('role')
            role = Role.objects.get(name=role)
            ParticipantShift.objects.create(
                participant=participant,
                role=role,
                shift=shift
            )
        return redirect(self.success_url)
```

## Delete View

`ParticipantDeleteView` is a generic `DeleteView` that deletes an existing `Participant` object.

```python
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy
from .models import Participant

class ParticipantDeleteView(DeleteView):
    model = Participant
    success_url = reverse_lazy('participant_list')
```

These views are used to interact with the `Participant` model in the Event Signup and Support Application.