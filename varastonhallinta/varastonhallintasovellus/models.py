from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _


class Henkilo(AbstractUser):
    email = models.EmailField(max_length=254, default=None, verbose_name="sähköpostiosoite")
    rooli = models.CharField(max_length=20, default="oppilas", choices=[
        ("oppilas", _("Oppilas")),
        ("varastonhoitaja", _("Varastonhoitaja")),
        ("opettaja", _("Opettaja")),
        ("hallinto", _("Hallinto")),
        ])
    vastuuopettaja = models.ForeignKey(
        "self", on_delete=models.SET_NULL, null=True, blank=True,
        limit_choices_to=Q(rooli__icontains="opettaja"))

    REQUIRED_FIELDS = ["email", "first_name", "last_name"]

    def __str__(self):
        return self.first_name + " " + self.last_name


class Varastotyyppi(models.Model):
    nimi = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = "Varastotyypit"

    def __str__(self):
        return self.nimi


class Varasto(models.Model):
    nimi = models.CharField(max_length=50)
    varastotyyppi = models.ForeignKey(Varastotyyppi, on_delete=models.RESTRICT)

    class Meta:
        verbose_name_plural = "Varastot"

    def __str__(self):
        return self.nimi


class Tuoteryhma(models.Model):
    nimi = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = "Tuoteryhmät"

    def __str__(self):
        return self.nimi


class Tuote(models.Model):
    viivakoodi = models.CharField(max_length=30)
    nimike = models.CharField(max_length=100)
    valmistaja = models.CharField(max_length=100, null=True, blank=True)
    kappalemaara = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        default=1, verbose_name="kappalemäärä")
    kappalemaara_lainassa = models.PositiveIntegerField(default=0, verbose_name="kappalemäärä lainassa")
    tuotekuva = models.ImageField(upload_to="tuotekuvat", default="default.png", null=True, blank=True)
    tuoteryhma = models.ForeignKey(Tuoteryhma, on_delete=models.RESTRICT)
    hankintapaikka = models.CharField(max_length=100, null=True, blank=True)
    hankintapaiva = models.DateField(null=True, blank=True, verbose_name="hankintapäivä")
    hankintahinta = models.DecimalField(
        validators=[MinValueValidator(0)], decimal_places=2,
        max_digits=8, null=True, blank=True)
    laskun_numero = models.IntegerField(null=True, blank=True)
    kustannuspaikka = models.CharField(max_length=30, null=True, blank=True)
    takuuaika = models.DateField(null=True, blank=True, verbose_name="takuun päättymispäivä")

    def validoi_kappalemaarat(self):
        if self.kappalemaara_lainassa > self.kappalemaara:
            raise ValidationError("Varastossa ei ole tarpeeksi tätä tuotetta lainausta varten!")

    def save(self, *args, **kwargs):
        self.validoi_kappalemaarat()
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Tuotteet"

    def __str__(self):
        return self.nimike


class Varastotapahtuma(models.Model):
    tyyppi = models.CharField(max_length=10, choices=[
        ('lainaus', 'Lainaus'),
        ('palautus', 'Palautus'),
        ('poistot', 'Poistot'),
        ('lisays', 'Lisäys'),
        ])
    tuote = models.ForeignKey(Tuote, on_delete=models.RESTRICT)
    maara = models.IntegerField(
        verbose_name="määrä",
        help_text="Lainauksille ja poistoille negatiivinen, lisäyksille ja palautuksille positiivinen")
    arkistotunnus = models.CharField(max_length=50, null=True, blank=True)
    varasto = models.ForeignKey(Varasto, on_delete=models.RESTRICT)
    aikaleima = models.DateField(auto_now_add=True)
    asiakas = models.ForeignKey(Henkilo, related_name="asiakas", on_delete=models.RESTRICT, null=True, blank=True)
    varastonhoitaja = models.ForeignKey(Henkilo, related_name="varastonhoitaja", on_delete=models.RESTRICT)
    palautuspaiva = models.DateField(
        verbose_name="palautuspäivä",
        help_text="Päivä jona tuote tulisi viimeistään palauttaa", null=True, blank=True)

    class Meta:
        verbose_name_plural = "Varastotapahtumat"

    def __str__(self):
        if self.tyyppi == 'lainaus':
            return f'"{self.asiakas}" lainasi tuotteen "{self.tuote}" päivämäärällä {self.aikaleima.strftime("%d.%m.%Y")}'
        elif self.tyyppi == 'palautus':
            return f'"{self.asiakas}" palautti tuotteen "{self.tuote}" päivämäärällä {self.aikaleima.strftime("%d.%m.%Y")}'
        elif self.tyyppi == 'poistot':
            return f'"{self.varastonhoitaja}" poisti tuotteen "{self.tuote}" päivämäärällä {self.aikaleima.strftime("%d.%m.%Y")}'
        else:
            return f'"{self.varastonhoitaja}" lisäsi tuotteen "{self.tuote}" päivämäärällä {self.aikaleima.strftime("%d.%m.%Y")}'
