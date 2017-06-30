import operator
from itertools import chain

from django.shortcuts import render, get_object_or_404

# Create your views here.
from eventex.core.models import Speaker, Talk, Course


def home(request):
    speakers = Speaker.objects.all()

    return render(request, 'index.html', {'speakers': speakers})


def speaker_detail(request, slug):
    speaker = get_object_or_404(Speaker, slug=slug)
    return render(request, 'core/speaker_detail.html', {'speaker': speaker})


def talk_list(request):
    morning_talks = chain(Talk.objects.at_morning(),
                          Course.objects.at_morning())
    morning_talks = sorted(morning_talks, key=operator.attrgetter('start'))
    afternoon_talks = chain(Talk.objects.at_afternoon(),
                            Course.objects.at_afternoon())
    afternoon_talks = sorted(afternoon_talks, key=operator.attrgetter('start'))
    context = {
        'morning_talks': morning_talks,
        'afternoon_talks': afternoon_talks,
    }
    return render(request, 'core/talk_list.html', context)
