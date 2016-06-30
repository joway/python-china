from django.shortcuts import render


def home(request):
    return render(request, 'index.html', locals())


def topic(request):
    return render(request, 'topic.html', locals())
