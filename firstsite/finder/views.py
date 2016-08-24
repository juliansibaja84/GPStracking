from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.template import loader


def index(request):
    template = loader.get_template('finder/logger.html')

    return HttpResponse(template.render())


def req(request):
    return JsonResponse({'lat': '+10.98995', 'lon': '-74.82617'})
