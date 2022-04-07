from django.shortcuts import render, redirect
from django.views.generic import ListView #???
import json
# Djangon autentikaatiot sisään- ja uloskirjautumiseen
from django.contrib.auth import authenticate, login, logout
# Djangon sisäänkirjautumisfunktio jolla suojataan näkymät jotta käyttäjän on
# pakko kirjautua sisään nähdäkseen ne
# MUUT KIRJAUTUMISEEN / ULOSKIRJAUTUMISEEN TARVITTAVAT ASETUKSET
# LÖYTYVÄT --> "settings.py"!
from django.contrib.auth.decorators import login_required
# Näytetään käyttäjälle viesti jos sisäänkirjautuminen ei onnistunut
from django.contrib import messages

from .models import Tuote
from .filters import TuoteFilter


def kirjautuminen(request):
    if request.user.is_authenticated:
        return redirect('hallinta/')
    else:
        if request.method == 'POST':
            username = request.POST['käyttäjätunnus']
            password = request.POST['salasana']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('hallinta/')
            else:
                messages.success(request, ("Antamasi salasana tai käyttäjätunnus on väärä!"))
                return redirect('kirjautuminen')
        else:
            return render(request, 'kirjautuminen.html')


def uloskirjautuminen(request):
    logout(request)
    messages.success(request, ("Olet nyt kirjautunut ulos."))
    return redirect('kirjautuminen')


#@login_required
# def tuotehaku(request):
    # return HttpResponse('tuotehaku')


@login_required
def lainaus(request):
    tuotteet = Tuote.objects.all()
    
    filter = TuoteFilter(request.GET, queryset=tuotteet)
    tuotteet = filter.qs


    context = {'tuotteet':tuotteet, 'filter':filter}
    return render(request, 'lainaus.html', context)



#@login_required
# def palautus(request):
#     return HttpResponse('palautussivu')


@login_required
def hallinta(request):
    return render(request, 'hallinta.html')


#@login_required
# def lisaaminen(request):
#     return HttpResponse('tuotteiden lisääminen')