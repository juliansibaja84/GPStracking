from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.template import loader


def index(request):
    template = loader.get_template('finder/logger.html')

    return HttpResponse(template.render())


def req(request):
    dictio = load_last_element()
    return JsonResponse(dictio)


def load_last_element():
    d = dict()
    f = open('top.txt', 'r')
    line = f.read()
    f.close()
    lines = line.split(',')
    d['lat'] = lines[0]
    d['lon'] = lines[1]
    d['time'] = lines[2]

    return d
