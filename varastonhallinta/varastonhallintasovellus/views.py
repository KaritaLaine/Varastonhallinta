from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
#from django.contrib.auth import login, logout

# from django.http import (
#     HttpResponse, 
#     HttpResponseBadRequest,
#     HttpResponseNotFound)

#from .models import Henkilo

def kirjautuminen(request):
    if request.method == 'POST':
        username = request.POST['käyttäjätunnus']
        password = request.POST['salasana']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('hallinta/')
        else:
            messages.success(request, ("Antamasi salasana tai käyttäjätunnus on väärä!"))
            return redirect('/')
    else:
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