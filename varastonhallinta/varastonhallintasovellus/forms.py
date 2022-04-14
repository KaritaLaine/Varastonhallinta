from django import forms

from .models import Tuote

class LisaaTuoteForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('kayttajan_rooli')
        super(LisaaTuoteForm, self).__init__(*args, **kwargs)
        if self.user == 'varastonhoitaja':
            for kentta in ['hankintapaikka', 'hankintapaiva', 'hankintahinta', 'laskun_numero', 'kustannuspaikka', 'takuuaika']:
                del self.fields[kentta]

    class Meta():
        model = Tuote

        fields = '__all__'

        labels = {
            "viivakoodi": "Lisää tuotteen viivakoodi",
            "nimike": "Lisää tuotteen nimi",
            "valmistaja": "Lisää tuotteen valmistaja",
            "kappalemaara": "Lisää tuotteiden kappalemäärä",
            "tuotekuva": "Anna tuotteelle kuva",
            "hankintapaikka": "Mistä tuote on ostettu?",
            "hankintavuosi": "Vuosi jona tuote on ostettu",
            "hankintapaiva": "Lisää päivä jona tuote on ostettu",
            "hankintahinta": "Tuotteen hankintahinta",
            "laskun_numero": "Laskun numero",
            "kustannuspaikka": "Mille osastolle tuote on ostettu",
            "takuuaika": "Jos tuotteella on takuu, mihin asti se on voimassa",
        }

        error_messages = {
            "nimike": {
                "required": "Sinun on annettava tuotteelle nimi.",
                "max_length": "Tuotteen nimen on oltava maksimissaan 100 merkkiä."
            },
            "valmistaja": {
                "max_length": "Valmistajan nimen on oltava maksimissaan 100 merkkiä."
            },
            "hankintapaikka": {
                "max_length": "Hankintapaikan nimen on oltava maksimissaan 100 merkkiä."
            },
        }