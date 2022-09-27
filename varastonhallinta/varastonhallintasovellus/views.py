# Tarvittavat json-importit hakukentän toimimiseen
import json

# "messages" avulla voimme näyttää kustomoituja viestejä käyttäjille
# + näyttää ne templeteissä.
from django.contrib import messages
# Djangon autentikaatiot sisään- ja uloskirjautumiseen
from django.contrib.auth import authenticate, login, logout
# Importit class näkymän parametrille joka vaatii käyttäjää
# olemaan sisäänkirjautuneena nähdäkseen sivun (funktionäkymät)
from django.contrib.auth.decorators import login_required, user_passes_test
# Importit "testeille joiden käyttäjien on läpäistävä" jotta he pääsevät tietyille sivulle (class näkymät)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
# Import class näkymä tyypille jonka avulla käyttäjä voi vaihtaa salasanansa
from django.contrib.auth.views import PasswordChangeView
# Importit "toimenpiteille" joita tehdään jos käyttäjällä ei ole oikeutta sivuun
from django.core.exceptions import PermissionDenied, ValidationError
# Pagination, eli sivutus importit
from django.core.paginator import Paginator
from django.db.models import F
# Import 404 (sivua ei löydy) näkymään
from django.http import Http404, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
# Importit class näkymä tyypeille
from django.views import View
from django.views.generic import ListView, UpdateView
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, DeleteView

# Lomakkeiden importit --> "forms.py"
from .forms import (LainaaTuoteForm, MuokkaaKayttajaaForm, PalautaTuoteForm,
                    RekisteroityminenForm, TuoteForm)
# Models importit
from .models import Tuote, Varasto, Varastotapahtuma

# MUUT KIRJAUTUMISEEN / ULOSKIRJAUTUMISEEN TARVITTAVAT ASETUKSET
# LÖYTYVÄT --> settings.py!


class EiOikeuttaUserMixin(LoginRequiredMixin, UserPassesTestMixin):
    """
    Kun käyttäjällä ei ole oikeutta johonkin sivuun...
    1. Käyttäjällä ei ole oikeutta johonkin sivuun --> näytä '403.html'
    2. tai jos ei ole kirjautuneena ja yrittää päästä sivulle --> näytä 'kirjautuminen.html'
    """

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            raise PermissionDenied()
        else:
            return redirect('/kirjautuminen/')


class ErrorView(View):
    def index(self):
        raise Http404


kaikki_kayttajatyypit = ['oppilas', 'varastonhoitaja', 'opettaja', 'hallinto']
paakayttajat = ['varastonhoitaja', 'opettaja', 'hallinto']
varastonhoitajat = ['varastonhoitaja', 'opettaja']
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


class VarastonhoitajatUserMixin(EiOikeuttaUserMixin, UserPassesTestMixin):
    """
    Pääsyoikeidet henkilökunnalle --> opettajat, hallinto.
    --> Tätä classia käytetään parametrina tietyissä class näkymissä.
    """

    def test_func(self):
        if self.request.user.rooli in varastonhoitajat:
            return True


class HenkilokuntaUserMixin(EiOikeuttaUserMixin, UserPassesTestMixin):
    """
    Pääsyoikeidet henkilökunnalle --> opettajat, hallinto.
    --> Tätä classia käytetään parametrina tietyissä class näkymissä.
    """

    def test_func(self):
        if self.request.user.rooli in henkilokunta:
            return True


def role_check(user):
    if user.rooli != 'oppilas':
        return True

    raise PermissionDenied()


class RekisteroityminenView(CreateView):
    form_class = RekisteroityminenForm
    success_url = '/rekisteroityminen/'
    template_name = 'rekisteroityminen.html'
    etusivu_url = '/'

    def get(self, request):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(self.etusivu_url)
        else:
            return render(request, 'rekisteroityminen.html', {'form' : self.form_class})

    def form_valid(self, form):
        messages.success(
            self.request,
            f'Käyttäjätunnuksesi on nyt luotu, vahvistusviesti on lähetetty sähköpostiisi'
        )
        return super().form_valid(form)


class MuokkaaKayttajaaView(KaikkiKayttajatUserMixin, UpdateView):
    form_class = MuokkaaKayttajaaForm
    success_url = '/muokkaa-kayttajaa/'
    template_name = 'muokkaa-kayttajaa.html'

    def get_object(self):
        return self.request.user

    def get_form_kwargs(self):
        kwargs = super(MuokkaaKayttajaaView, self).get_form_kwargs()
        kwargs['kayttajan_rooli'] = self.request.user.rooli
        return kwargs

    def form_valid(self, form):
        messages.success(self.request, f'Tietojasi on nyt muokattu!')
        return super().form_valid(form)


class VaihdaSalasanaView(KaikkiKayttajatUserMixin, PasswordChangeView):
    success_url = '/muokkaa-kayttajaa/'
    template_name = 'vaihda-salasana.html'

    def form_valid(self, form):
        messages.success(self.request, f'Salasanasi on nyt vaihdettu!')
        return super().form_valid(form)


def kirjautuminen(request):
    """
    Funktio sisäänkirjautumista varten, sekä uudelleenohjaus etusivulle jos
    käyttäjä on jo kirjautunut tai uudelleenohjaus kirjautumissivulle jos
    käyttäjän antamat todentamistiedot ovat virheelliset.
    """
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
        # Jos metodi on GET tarkistetaan onko käyttäjä kirjautunut ja renderöidään etusivu
        # jos ei, renderöidään kirjautumissivu.
        if request.user.is_authenticated:
            return redirect('etusivu')
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
@user_passes_test(role_check)
def lainattavat(request):
    tuotteet = Tuote.objects.filter(kappalemaara__gt=F('kappalemaara_lainassa'))

    for tuote in tuotteet:
        if tuote.kappalemaara_lainassa > 0:
            tuote.kappalemaara -= tuote.kappalemaara_lainassa

    maara = tuotteet.count()
    # Asetetaan pagination eli sivutus
    per_page = 20
    paginator = Paginator(tuotteet, per_page)
    sivunumero = request.GET.get('sivu', 1)
    sivu_obj = paginator.get_page(sivunumero)
    context = {
        'tuotteet':sivu_obj,
        'paginator':paginator,
        'sivunumero': int(sivunumero),
        'maara':int(maara),
        'per_page': int(per_page)
        }
    return render(request, 'lainattavat.html', context)

# Käytetään XMLHttp-apia ajax-pyyntöjen luomiseen.
def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

# Ajax hakuominaisuus
@user_passes_test(role_check)
def haku_tulokset(request):
    if is_ajax(request=request):
        response = None
         # Haku-muuttujaan tallennetaan käyttäjän antama tuote-hakuteksti.
        haku = request.POST.get('tuote')
        # Tuotteet-muuttujaan tallennetaan hakutulokset, eli haut jotka vastaavat Tuote-taulussa olevaa nimikettä.
        tuotteet = Tuote.objects.filter(nimike__icontains=haku).filter(kappalemaara__gt=F('kappalemaara_lainassa'))

        # Tallennetaan jokaisesta hakutuloksesta pk, nimike, tuotekuva ja kappalemäärä item-sanakirjaan.
        if len(tuotteet) > 0 and len(haku) > 0:
            data = []
            for pos in tuotteet:
                itemit = {
                    'pk': pos.pk,
                    'nimike': pos.nimike,
                    'tuotekuva': str(pos.tuotekuva.url),
                    'kappalemaara': pos.kappalemaara,
                    'tuoteryhma': str(pos.tuoteryhma),
                    'valmistaja': pos.valmistaja,
                    'hankintapaikka': pos.hankintapaikka,
                    'hankintapaiva' : pos.hankintapaiva,
                    'hankintahinta': pos.hankintahinta,
                    'laskun_numero': pos.laskun_numero,
                    'kustannuspaikka': pos.kustannuspaikka,
                    'takuuaika': (pos.takuuaika),
                }
                # Lisätään itemit data-listaan ja sen jälkeen response-muuttujaan.
                data.append(itemit)
            response = data

        # Jos hakutuloksia ei ole, tallennetaan response-muuttujaan "Ei hakutulosta.."-teksti.
        else:
            response = '</br> <b>Ei hakutulosta..</b>'

        # Response-muuttuja palautetaan.
        return JsonResponse({'data': response})
    return JsonResponse({})


@login_required
@user_passes_test(role_check)
def palautettavat(request):
    varastotapahtumat = Varastotapahtuma.objects.filter(tyyppi='lainaus')
    maara = Varastotapahtuma.objects.all().count()
    # Asetetaan pagination eli sivutus
    per_page = 20
    paginator = Paginator(varastotapahtumat, per_page)
    sivunumero = request.GET.get('sivu', 1)
    sivu_obj = paginator.get_page(sivunumero)
    context = {
        'varastotapahtuma' : varastotapahtumat,
        'varastotapahtumat':sivu_obj,
        'paginator':paginator,
        'sivunumero': int(sivunumero),
        'maara':int(maara),
        'per_page': int(per_page)
        }
    return render(request, 'palautettavat.html', context)

@user_passes_test(role_check)
def varastotapahtuma_hakutulokset(request):
    if is_ajax(request=request):
        response = None
        tapahtuma = request.POST.get('tapahtuma')
        varastotapahtumat = Varastotapahtuma.objects.filter(tuote__nimike__icontains=tapahtuma)
        if len(varastotapahtumat) > 0 and len(tapahtuma) > 0:
            data = []
            for pos in varastotapahtumat:
                iteemit = {
                    'pk':pos.pk,
                    'nimike': pos.tuote.nimike,
                    'tuotekuva': str(pos.tuote.tuotekuva.url),
                    'kappalemaara': pos.tuote.kappalemaara_lainassa,
                    'lainaaja': str(pos.asiakas),
                }
                data.append(iteemit)
            response = data
        else:
            response = '</br> <b>Ei hakutulosta..</b>'
        return JsonResponse({'data': response})
    return JsonResponse({})


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

    #Tehdään roolimixin --> parametrina tähän classiin
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

    # Tehdään roolimixin --> parametrina tähän classiin
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


class LainaaTuoteView(VarastonhoitajatUserMixin, CreateView):
    model = Varastotapahtuma
    form_class = LainaaTuoteForm
    template_name = 'suorita-lainaus.html'
    success_url = '/lainattavat/'

    def get_form_kwargs(self):
        kwargs = super(LainaaTuoteView, self).get_form_kwargs()
        kwargs['viivakoodi'] = get_object_or_404(Tuote, pk=self.kwargs.get('pk')).viivakoodi
        return kwargs

    def get_initial(self):
        varastonhoitaja = self.request.user
        tuote = get_object_or_404(Tuote, pk=self.kwargs.get('pk'))
        varasto = Varasto.objects.get(nimi="Lainassa")
        return {
            'tyyppi' : 'lainaus',
            'tuote' : tuote,
            'maara' : 1,
            'varasto' : varasto,
            'arkistotunnus' : "Arkistotunnus Tähän!",
            'varastonhoitaja' : varastonhoitaja,
        }

    def form_valid(self, form):
        try:
            # 'get_object_or_404' already does the 'try/excerpt' does that for you!
            # MOVE IT OUTSIDE OF IT IF POSSIBLE!
            tuote = get_object_or_404(Tuote, pk=self.kwargs.get('pk'))
            maara = form.cleaned_data['maara']
            tuote.kappalemaara_lainassa += maara
            tuote.save()
            messages.success(self.request, f'Lainaus tehty!')
            return super().form_valid(form)
        except ValidationError:
            messages.error(self.request, f'Varastossa ei ole tarpeeksi tätä tuotetta lainausta varten!')
            return self.render_to_response(self.get_context_data(form=form))


class PalautaTuoteView(VarastonhoitajatUserMixin, UpdateView):
    model = Varastotapahtuma
    form_class = PalautaTuoteForm
    template_name = 'suorita-palautus.html'
    success_url = '/palautettavat/'

    def get_form_kwargs(self):
        kwargs = super(PalautaTuoteView, self).get_form_kwargs()
        tuote = get_object_or_404(Varastotapahtuma, pk=self.kwargs.get('pk')).tuote
        kwargs['viivakoodi'] = get_object_or_404(Tuote, nimike=tuote).viivakoodi
        return kwargs

    def get_initial(self):
        varasto = Varasto.objects.get(nimi='Koululla')
        return {
            'tyyppi' : 'palautus',
            'varasto' : varasto,
        }

    def form_valid(self, form):
        try:
            # 'get_object_or_404' already does the 'try/excerpt' does that for you!
            # MOVE IT OUTSIDE OF IT IF POSSIBLE!
            tuote = get_object_or_404(Tuote, nimike=form.cleaned_data['tuote'])
            maara = form.cleaned_data['maara']
            tuote.kappalemaara_lainassa -= maara
            tuote.save()
            messages.success(self.request, f'Palautus tehty!')
            return super().form_valid(form)
        except ValidationError:
            messages.error(self.request, f'Jokin meni pieleen!')
            return self.render_to_response(self.get_context_data(form=form))
