from django.shortcuts import render, redirect

# Tarvittavat json-importit hakukentän toimimiseen
import json
from django.http import JsonResponse

# Djangon autentikaatiot sisään- ja uloskirjautumiseen
from django.contrib.auth import authenticate, login, logout
# MUUT KIRJAUTUMISEEN / ULOSKIRJAUTUMISEEN TARVITTAVAT ASETUKSET
# LÖYTYVÄT --> settings.py!

from django.contrib.auth.decorators import login_required

# "messages" avulla voimme näyttää kustomoituja viestejä käyttäjille
# + näyttää ne templeiteissä.
from django.contrib import messages

# Importit "testeille joiden käyttäjien on läpäistävä" jotta he pääsevät tietyille sivulle 
from django.contrib.auth.mixins import UserPassesTestMixin

# Importit class näkymän parametrille joka vaatii käyttäjää
# olemaan sisäänkirjautuneena nähdäkseen sivun
from django.contrib.auth.mixins import LoginRequiredMixin

# Importit class näkymä tyypeille
from django.views.generic import ListView, UpdateView
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, DeleteView

# Import class näkymä tyypille jonka avulla käyttäjä voi vaihtaa salasanansa
from django.contrib.auth.views import PasswordChangeView

# Models importit
from .models import Tuote

# Lomakkeen import --> "forms.py"
from .forms import RekisteroityminenForm, MuokkaaKayttajaaForm, TuoteForm



class EiOikeuttaUserMixin(LoginRequiredMixin, UserPassesTestMixin):
    """
    Kun käyttäjällä ei ole oikeutta johonkin sivuun...
    1. Käyttäjällä ei ole oikeutta johonkin sivuun uudelleenohjaus --> 'kirjautuminen'
    2. tai jos käyttäjä on kirjautunut mutta ei oikeutta --> 'kirjautuminen' -> 'etusivu'
    """

    def handle_no_permission(self):
        return redirect('kirjautuminen')


kaikki_kayttajatyypit = ['oppilas', 'varastonhoitaja', 'opettaja', 'hallinto']
paakayttajat = ['varastonhoitaja', 'opettaja', 'hallinto']
henkilokunta = ['opettaja', 'hallinto']


class KaikkiKayttajatUserMixin(EiOikeuttaUserMixin, UserPassesTestMixin):
    """
    Pääsyoikeidet kaikille käyttäjätyypeille --> esim etusivua varten
    --> Tätä classia käytetään parametrina tietyissä class näkymissä.
    """
    
    def test_func(self):
        if self.request.user.rooli in kaikki_kayttajatyypit:
            return True


class PaakayttajatUserMixin(EiOikeuttaUserMixin, UserPassesTestMixin):
    """
    Pääsyoikeidet kaikille pääkäyttäjäjille --> varastonhoitajat, opettajat, hallinto jne.
    --> Tätä classia käytetään parametrina tietyissä class näkymissä.
    """
    
    def test_func(self):
        if self.request.user.rooli in paakayttajat:
            return True


class HenkilokuntaUserMixin(EiOikeuttaUserMixin, UserPassesTestMixin):
    """
    Pääsyoikeidet henkilökunnalle --> opettajat, hallinto.
    --> Tätä classia käytetään parametrina tietyissä class näkymissä.
    """
    
    def test_func(self):
        if self.request.user.rooli in henkilokunta:
            return True


class RekisteroityminenView(HenkilokuntaUserMixin, CreateView):
    form_class = RekisteroityminenForm
    success_url = '/rekisteroityminen/'
    template_name = "rekisteroityminen.html"

    def form_valid(self, form):
        messages.success(self.request, f'Käyttäjä on nyt lisätty! Lisätäänkö saman tien toinen?')
        return super().form_valid(form)


class MuokkaaKayttajaaView(KaikkiKayttajatUserMixin, UpdateView):
    form_class = MuokkaaKayttajaaForm
    success_url = '/muokkaa-kayttajaa/'
    template_name = "muokkaa-kayttajaa.html"

    def get_object(self):
      return self.request.user

    def form_valid(self, form):
        messages.success(self.request, f'Tietojasi on nyt muokattu!')
        return super().form_valid(form)


class VaihdaSalasanaView(KaikkiKayttajatUserMixin, PasswordChangeView):
    success_url = '/muokkaa-kayttajaa/'
    template_name = "vaihda-salasana.html"

    def form_valid(self, form):
        messages.success(self.request, f'Salasanasi on nyt vaihdettu!')
        return super().form_valid(form)


def kirjautuminen(request):
    """
    Funktio sisäänkirjautumista varten, sekä uudelleenohjaus etusivulle jos
    käyttäjä on jo kirjautunut tai uudelleenohjaus kirjautumissivulle jos
    käyttäjän antamat todentamistiedot ovat virheelliset.
    """
    if request.user.is_authenticated:
        return redirect('/')
    else:
        # Jos lomake lähetetään (submit) metodi on POST
        if request.method == 'POST':
            username = request.POST['käyttäjätunnus']
            password = request.POST['salasana']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                # Kirjautumistiedot ovat väärät, näytä viesti
                # ja uudelleenohjaa kirjautumissivulle.
                messages.success(request, ('Antamasi salasana tai käyttäjätunnus on väärä!'))
                return redirect('kirjautuminen')
        else:
            # Jos metodi on GET renderöidään kirjautumissivu
            return render(request, 'kirjautuminen.html')


def uloskirjautuminen(request):
    """
    Funktio uloskirjautumista varten, sekä viesti kirjautumislomakkeeseen
    että käyttäjä on nyt kirjautunut ulos
    """
    logout(request)
    messages.success(request, ('Olet nyt kirjautunut ulos.'))
    return redirect('kirjautuminen')


class EtusivuView(KaikkiKayttajatUserMixin, TemplateView):
    """
    Näkymä etusivulle johon pääse kaikki kirjautuneet käyttäjät joiden
    rooli on joko --> 'oppilas', 'varastonhoitaja', 'opettaja' tai 'hallinto'
    """
    template_name = 'etusivu.html'


@login_required
def lainaus(request):
    tuotteet = Tuote.objects.all()
    context = {'tuotteet':tuotteet,}
    return render(request, 'lainaus.html', context)

def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

def haku_tulokset(request):
    if is_ajax(request=request):
        response = None
        tuote = request.POST.get('tuote')
        tuotteet = Tuote.objects.filter(nimike__icontains=tuote)
        if len(tuotteet) > 0 and len(tuote) > 0:
            data = []
            for objekti in tuotteet:
                iteemit = {
                    'nimike': objekti.nimike,
                    'tuotekuva': str(objekti.tuotekuva.url),
                    'kappalemaara': objekti.kappalemaara,
                    'tuoteryhma': str(objekti.tuoteryhma),
                    'valmistaja': objekti.valmistaja,
                    'hankintapaikka': objekti.hankintapaikka,
                    'hankintapaiva' : objekti.hankintapaiva,
                    'hankintahinta': objekti.hankintahinta,
                    'laskun_numero': objekti.laskun_numero,
                    'kustannuspaikka': objekti.kustannuspaikka,
                    'takuuaika': (objekti.takuuaika),
                }

                data.append(iteemit)
            response = data
        else:
            response = '</br> <b>Ei hakutulosta..</b>'
        return JsonResponse({'data': response})
    return JsonResponse({})

#@login_required
# def palautus(request):
#     return HttpResponse('palautussivu')


class HallintaView(PaakayttajatUserMixin, ListView):
    """
    Vain pääkäyttäjät (varastonhoitaja', 'opettaja', 'hallinto) pääsevät hallinta
    näkymään, jossa listataan kaikki tietokannassa olevat tuotteet ja joissa on linkit
    niiden poistamiseen ja muokkaamiseen + tiedot tuotteista
    --> (tiedon määrä riippuen käyttäjän roolista).
    """
    template_name = 'hallinta.html'
    model = Tuote
    context_object_name = "tuotteet"


class LisaaTuoteView(PaakayttajatUserMixin, CreateView):
    """
    Näkymä tuotteiden lisäämistä varten joka myös tarkistaa käyttäjän roolin
    jonka avulla 'TuoteForm' ei näytä kaikkia modelin kenttiä varastonhoitajalle
    """
    model = Tuote
    form_class = TuoteForm
    template_name = 'lisaa-tuote.html'
    success_url = '/lisaa-tuote/'

    def get_form_kwargs(self):
        kwargs = super(LisaaTuoteView, self).get_form_kwargs()
        kwargs['kayttajan_rooli'] = self.request.user.rooli
        return kwargs

    def form_valid(self, form):
        messages.success(self.request, f'Tuote on nyt lisätty! Lisätäänkö saman tien toinen?')
        return super().form_valid(form)


class MuokkaaTuotettaView(PaakayttajatUserMixin, UpdateView):
    """
    Näkymä tuotteiden muokkaamista varten joka myös tarkistaa käyttäjän roolin
    jonka avulla 'TuoteForm' ei näytä kaikkia modelin kenttiä varastonhoitajalle
    """
    model = Tuote
    form_class = TuoteForm
    template_name = 'muokkaa-tuotetta.html'
    success_url = '/hallinta/'

    def get_form_kwargs(self):
        kwargs = super(MuokkaaTuotettaView, self).get_form_kwargs()
        kwargs['kayttajan_rooli'] = self.request.user.rooli
        return kwargs

    def form_valid(self, form):
        messages.success(self.request, f'Tuotetta on nyt muokattu!')
        return super().form_valid(form)


class PoistaTuoteView(PaakayttajatUserMixin, DeleteView):
    """
    Näkymä tuotteen poistamista varten joka uudelleenohjaa käyttäjän
    hallinta sivulle tuotteen poistamisen jälkeen.
    """
    model = Tuote
    template_name = 'poista-tuote.html'
    success_url = '/hallinta/'