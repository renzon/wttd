from collections import namedtuple

from django.shortcuts import render


# Create your views here.

def home(request):
    Speaker = namedtuple('Speaker', 'name, photo')
    speakers = [
        Speaker('Grace Hopper', '//hbn.link/hopper-pic'),
        Speaker('Alan Turing', '//hbn.link/turing-pic')
    ]

    return render(request, 'index.html', {'speakers': speakers})
