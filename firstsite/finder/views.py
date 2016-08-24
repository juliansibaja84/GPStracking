from django.shortcuts import render
from django.http import HttpResponse

def index(request):
	return HttpResponse(traduct())

def traduct():
	datos = open("finder/logger.html",'r')
	dleidos = datos.read()
	datos.close()
	return dleidos
