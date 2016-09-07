from django.shortcuts import render


def index(request):
    template = loader.get_template('finder/logger.html')

    return HttpResponse(template.render())
