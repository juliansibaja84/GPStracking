from django.shortcuts import render
from django.http import HttpResponse
#import codecs

def index(request):
	return HttpResponse(traduct())

def traduct():
	datos = open("finder/logger.html",'r')
	dleidos = datos.read()
	datos.close()
	return dleidos
