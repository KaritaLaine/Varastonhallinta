from django.shortcuts import render, redirect

# Tarvittavat json-importit hakukentän toimimiseen
import json
from django.http import JsonResponse

# Djangon autentikaatiot sisään- ja uloskirjautumiseen
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
from django.views.generic.edit import CreateView

# Models importit
from .models import Tuote

from .forms import LisaaTuoteForm


def kirjautuminen(request):
    """
    Funktio sisäänkirjautumista varten, sekä uudelleenohjaus etusivulle jos
    käyttäjä on jo kirjautunut ja uudelleenohjaus kirjautumissivulle jos
    käyttäjän antamat todentamistiedot ovat virheelliset.
    """
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
                return redirect('kirjautuminen')
        else:
            return render(request, 'kirjautuminen.html')


def uloskirjautuminen(request):
    """
    Funktio uloskirjautumista varten, sekä viesti kirjautumislomakkeeseen
    että käyttäjä on nyt kirjautunut ulos
    """
    logout(request)
    messages.success(request, ('Olet nyt kirjautunut ulos.'))
    return redirect('kirjautuminen')


class JosEiOikeuttaUserMixin(LoginRequiredMixin, UserPassesTestMixin):
    """
    Kun käyttäjällä ei ole oikeutta johonkin sivuun...
    1. Käyttäjällä ei ole oikeutta johonkin sivuun uudelleenohjaus --> 'kirjautuminen'
    2. tai jos käyttäjä on kirjautunut --> 'kirjautuminen' -> '/'
    """

    def handle_no_permission(self):
        return redirect('kirjautuminen')


class KaikkiKayttajatUserMixin(JosEiOikeuttaUserMixin, UserPassesTestMixin):
    """
    Pääsyoikeidet kaikille käyttäjätyypeille --> esim etusivua varten
    --> Tätä classia käytetään parametrina tietyissä class näkymissä.
    """
    
    def test_func(self):
        sallitut_kayttajatyypit = ['oppilas', 'varastonhoitaja', 'opettaja', 'hallinto']

        if self.request.user.rooli in sallitut_kayttajatyypit:
            return True


class PaakayttajatUserMixin(JosEiOikeuttaUserMixin, UserPassesTestMixin):
    """
    Pääsyoikeidet kaikille pääkäyttäjäjille --> varastonhoitajat, opettajat, hallinto jne.
    --> Tätä classia käytetään parametrina tietyissä class näkymissä.
    """
    
    def test_func(self):
        sallitut_kayttajatyypit = ['varastonhoitaja', 'opettaja', 'hallinto']

        if self.request.user.rooli in sallitut_kayttajatyypit:
            return True


class EtusivuView(KaikkiKayttajatUserMixin, TemplateView):
    """
    Näkymä etusivulle johon pääse kaikki kirjautuneet käyttäjät joiden
    rooli on joko --> 'oppilas', 'varastonhoitaja', 'opettaja' tai 'hallinto'
    """
    template_name = 'etusivu.html'


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


# HALLINTA NÄKYMÄ FUNKTIONA --> JOS CLASS VIEW EI TOIMI
# MUISTA VAIHTAA MYÖS URLS.PY:SSÄ!
# @login_required
# def hallinta(request):
#     return render(request, 'hallinta.html')


class HallintaView(PaakayttajatUserMixin, TemplateView):
    template_name = 'hallinta.html'


#@login_required
# def lisaaminen(request):
#     return HttpResponse('tuotteiden lisääminen')


class TuotteidenLisaaminenView(PaakayttajatUserMixin, CreateView):
    form_class = LisaaTuoteForm
    template_name = 'lisaa-tuote.html'
    success_url = '/lisaa-tuotteita'

    def get_form_kwargs(self):
        kwargs = super(TuotteidenLisaaminenView, self).get_form_kwargs()
        kwargs['kayttajan_rooli'] = self.request.user.rooli
        return kwargs

    def form_valid(self, form):
        messages.success(self.request, f'Tuote on nyt lisätty! Lisätäänkö saman tien toinen?')
        return super().form_valid(form)
