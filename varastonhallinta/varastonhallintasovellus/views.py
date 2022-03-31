from django.shortcuts import render

# from django.http import (
#     HttpResponse, 
#     HttpResponseBadRequest,
#     HttpResponseNotFound)

from django.shortcuts import render

#from .models import Henkilo

def kirjautuminen(request):
    return render(request, 'kirjautuminen.html')


# def tuotehaku(request):
    # return HttpResponse('tuotehaku')


def lainaus(request):
    return render(request, 'lainaus.html')


# def palautus(request):
#     return HttpResponse('palautussivu')


def hallinta(request):
    return render(request, 'hallinta.html')


# def lisaaminen(request):
#     return HttpResponse('tuotteiden lisääminen')