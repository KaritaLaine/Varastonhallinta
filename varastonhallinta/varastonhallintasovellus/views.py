from django.shortcuts import render, redirect

# Importit kirjautumiseen & uloskirjautuminen
from django.contrib.auth import authenticate, login, logout
# MUUT KIRJAUTUMISEEN / ULOSKIRJAUTUMISEEN TARVITTAVAT ASETUKSET
# LÖYTYVÄT --> settings.py!
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Importit testeille joiden käyttäjien on läpäistävä jotta he pääsevät tietyille sivulle 
from django.contrib.auth.mixins import UserPassesTestMixin

# Importit class näkymän parametrille joka vaatii käyttäjää
# olemaan sisäänkirjautuneena nähdäkseen sivun
from django.contrib.auth.mixins import LoginRequiredMixin

# Importit class näkymä tyypeille
from django.views.generic.base import TemplateView

# Models importit
from .models import Tuote


# Funktio kirjautumista varten
def kirjautuminen(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        if request.method == 'POST':
            username = request.POST['käyttäjätunnus']
            password = request.POST['salasana']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                messages.success(request, ('Antamasi salasana tai käyttäjätunnus on väärä!'))
                return redirect('/')
        else:
            return render(request, 'kirjautuminen.html')


# Funktio uloskirjautumista varten
def uloskirjautuminen(request):
    logout(request)
    messages.success(request, ('Olet nyt kirjautunut ulos.'))
    return redirect('kirjautuminen')


# Jos käyttäjällä ei ole oikeutta johonkin sivuun, uudelleenohjataan
# kirjautumissivulle ja jos käyttäjä on jo kirjautuneena kirjautuminen funtio...

#if request.user.is_authenticated:
    # return redirect('/')

# uudelleenohjaa kirjautuneen käyttäjän persnonoidulle etusivulle
class JosEiOikeuttaUserMixin(LoginRequiredMixin, UserPassesTestMixin):
    def handle_no_permission(self):
        return redirect('kirjautuminen')


# Pääsyoikeidet kaikille käyttäjätyypeille --> esim etusivua varten
class KaikkiKayttajatUserMixin(JosEiOikeuttaUserMixin, UserPassesTestMixin):
    
    def test_func(self):
        sallitut_kayttajatyypit = ['oppilas', 'varastonhoitaja', 'opettaja', 'hallinto']

        if self.request.user.rooli in sallitut_kayttajatyypit:
            return True


# Pääsyoikeidet kaikille pääkäyttäjäjille --> varastonhoitajat, opettajat, hallinto jne.
class PaaKayttajatUserMixin(JosEiOikeuttaUserMixin, UserPassesTestMixin):
    
    def test_func(self):
        sallitut_kayttajatyypit = ['varastonhoitaja', 'opettaja', 'hallinto']

        if self.request.user.rooli in sallitut_kayttajatyypit:
            return True


class EtusivuView(KaikkiKayttajatUserMixin, TemplateView):
    template_name = 'etusivu.html'


#@login_required
# def tuotehaku(request):
    # return HttpResponse('tuotehaku')


@login_required
def lainaus(request):
    tuotteet = Tuote.objects.all()
    context = {'tuotteet':tuotteet}
    return render(request, 'lainaus.html', context)


#@login_required
# def palautus(request):
#     return HttpResponse('palautussivu')


# HALLINTA NÄKYMÄ FUNKTIONA --> JOS CLASS VIEW EI TOIMI
# MUISTA VAIHTAA MYÖS URLS.PY:SSÄ!
# @login_required
# def hallinta(request):
#     return render(request, 'hallinta.html')


class HallintaView(PaaKayttajatUserMixin, TemplateView):
    template_name = 'hallinta.html'




#@login_required
# def lisaaminen(request):
#     return HttpResponse('tuotteiden lisääminen')