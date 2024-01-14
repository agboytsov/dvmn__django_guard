from datacenter.models import Passcard
from datacenter.models import Visit
from django.shortcuts import render, get_object_or_404
from django.utils.timezone import localtime


def get_duration(visit):
    started = localtime(visit.entered_at)
    if not visit.leaved_at:
        stopped = localtime()
    else:
        stopped = visit.leaved_at
    delta = stopped - started
    return delta


def format_duration(delta):
    return f'{int(delta.total_seconds()/60/60)}:' \
           f'{int((delta.total_seconds()/60)%60)}:'\
           f'{delta.seconds%60:00}'


def check_suspicious(visit, amount=60):
    spent = get_duration(visit)
    if amount * 60 < spent.total_seconds():
        return True
    return False


def passcard_info_view(request, passcode):
    passcard = Passcard.objects.filter(passcode=passcode)
    get_object_or_404(passcard)
    # Программируем здесь
    all_last_visits = Visit.objects.filter(passcard=passcard[0])
    this_passcard_visits = [
        {'entered_at' : visit.entered_at,
         'duration':format_duration(get_duration(visit)),
         'is_strange':check_suspicious(visit)} for visit in all_last_visits
    ]
    context = {
        'passcard': passcard,
        'this_passcard_visits': this_passcard_visits
    }
    return render(request, 'passcard_info.html', context)
