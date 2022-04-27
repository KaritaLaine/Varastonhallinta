from django import forms

from .models import Henkilo, Tuote, Varastotapahtuma

from django.contrib.auth.forms import UserCreationForm, UserChangeForm



class RekisteroityminenForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].label = 'Salasana'
        self.fields['password2'].label = 'Salasana uudelleen'

        self.fields['password1'].help_text = 'Anna salasana joka sisältää ainakin 8 merkkiä'
        self.fields['password2'].help_text = 'Syötä sama salasana tarkistuksen vuoksi uudelleen'

    class Meta:
        model = Henkilo
        fields = ("username", "email", "first_name", "last_name", "vastuuopettaja", "password1", "password2")

        labels = {
            "username"          : "Anna käyttäjätunnus",
            "email"             : "Anna sähköpostiosoite",
            "first_name"        : "Anna etunimi",
            "last_name"         : "Anna sukunimi",
            "vastuuopettaja"    : "Vastuuopettaja",
        }

        help_texts = {
            "username"          : "Anna käyttäjätunnus, esim. oppilaan opiskelijanumero",
            "email"             : "Anna koulun tarjoama sähköpostiosoite",
            "vastuuopettaja"    : "Jos luot käyttäjää oppilaalle, valitse hänen vastuuopettajansa"
        }


class MuokkaaKayttajaaForm(UserChangeForm):
    password = None

    class Meta:
        model = Henkilo
        fields = ("username", "email", "first_name", "last_name")


class TuoteForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('kayttajan_rooli')
        super(TuoteForm, self).__init__(*args, **kwargs)
        if self.user == 'varastonhoitaja':
            for kentta in ['hankintapaikka', 'hankintapaiva', 'hankintahinta', 'laskun_numero', 'kustannuspaikka', 'takuuaika']:
                del self.fields[kentta]

    class Meta():
        model = Tuote
        fields = '__all__'
        widgets = {
            'hankintapaiva' : forms.DateInput(format=('%Y-%m-%d'), attrs={'type': 'date'}),
            'takuuaika'     : forms.DateInput(format=('%Y-%m-%d'), attrs={'type': 'date'}),
        }

        labels = {
            "viivakoodi"        : "Lisää tuotteen viivakoodi",
            "nimike"            : "Lisää tuotteen nimi",
            "valmistaja"        : "Lisää tuotteen valmistaja",
            "kappalemaara"      : "Lisää tuotteiden kappalemäärä",
            "tuotekuva"         : "Anna tuotteelle kuva",
            "tuoteryhma"        : "Valitse tuoteryhmä johon tuote kuuluu",
            "hankintapaikka"    : "Mistä tuote on ostettu?",
            "hankintapaiva"     : "Lisää päivä jona tuote on ostettu",
            "hankintahinta"     : "Tuotteen hankintahinta",
            "laskun_numero"     : "Laskun numero",
            "kustannuspaikka"   : "Mille osastolle tuote on ostettu",
            "takuuaika"         : "Jos tuotteella on takuu, mihin asti se on voimassa",
        }

        error_messages = {
            "nimike": {
                "required"      : "Sinun on annettava tuotteelle nimi.",
                "max_length"    : "Tuotteen nimen on oltava maksimissaan 100 merkkiä."
            },
            "valmistaja": {
                "max_length"    : "Valmistajan nimen on oltava maksimissaan 100 merkkiä."
            },
            "hankintapaikka": {
                "max_length"    : "Hankintapaikan nimen on oltava maksimissaan 100 merkkiä."
            },
            "tuoteryhma": {
                "required"      : "Sinun on lisättävä tuotteen tuoteryhmä johon tuote kuuluu."
            }
        }


class LainausForm(forms.ModelForm):
    class Meta:
        model = Varastotapahtuma
        fields = '__all__'
        widgets = {
            'aikaleima'         : forms.DateInput(format=('%Y-%m-%d'), attrs={'type': 'date'}),
            'palautuspaiva'     : forms.DateInput(format=('%Y-%m-%d'), attrs={'type': 'date'}),
        }


# class PalautusForm(forms.ModelForm):
#     pass