from django.shortcuts import render, redirect
# Tarvittavat json-importit hakukentän toimimiseen
import json
from django.http import JsonResponse
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
    context = {'tuotteet':tuotteet,}
    return render(request, 'lainaus.html', context)


def tuotehaku(request):
    if request.method=='POST':
        # Hakuun syötettävät asiat muutetaan python dictionaryksi
        haku_str = json.loads(request.body).get('hakuteksti')
        # Tallentaa tuotteet-muuttujaan haut, jotka vastaavat haun sisältöä
        tuotteet = Tuote.objects.filter(nimike__icontains=haku_str)
    data = tuotteet.values()
    # Palauttaa tulokset JSON-muodossa
    return JsonResponse(list(data), safe=False)



#@login_required
# def palautus(request):
#     return HttpResponse('palautussivu')


@login_required
def hallinta(request):
    return render(request, 'hallinta.html')


#@login_required
# def lisaaminen(request):
#     return HttpResponse('tuotteiden lisääminen')