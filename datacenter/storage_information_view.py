from datacenter.models import Passcard
from datacenter.models import Visit
from django.shortcuts import render
from django.utils.timezone import localtime


def storage_information_view(request):
    non_closed_visits = []
    active_visits = Visit.objects.filter(leaved_at__isnull=True)
    for visitor in active_visits:
        local = localtime(visitor.entered_at)
        now = localtime()
        delta = now - local
        non_closed_visits.append(
            {
            'who_entered': visitor.passcard,
            'entered_at': visitor.entered_at,
            'duration': f'{int(delta.total_seconds() / 60 / 60)}:'
                        f'{int((delta.total_seconds() / 60) % 60)}:'
                        f'{delta.seconds % 60:00}',
            }
        )
        pass
    context = {
        'non_closed_visits': non_closed_visits,  # не закрытые посещения
    }
    return render(request, 'storage_information.html', context)
