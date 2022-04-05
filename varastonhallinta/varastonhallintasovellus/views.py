from django.shortcuts import render
from .models import Tuote

# from django.http import (
#     HttpResponse, 
#     HttpResponseBadRequest,
#     HttpResponseNotFound)


#from .models import Henkilo

def kirjautuminen(request):
    return render(request, 'kirjautuminen.html')


# def tuotehaku(request):
    # return HttpResponse('tuotehaku')


def lainaus(request):
    tuotteet = Tuote.objects.all()
    context = {'tuotteet':tuotteet}
    return render(request, 'lainaus.html', context)


# def palautus(request):
#     return HttpResponse('palautussivu')


def hallinta(request):
    return render(request, 'hallinta.html')


# def lisaaminen(request):
#     return HttpResponse('tuotteiden lisääminen')