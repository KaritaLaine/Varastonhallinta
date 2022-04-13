from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser

from django.core.validators import MinValueValidator


class Henkilo(AbstractUser):
    email = models.EmailField(max_length=254, default=None, verbose_name="sähköpostiosoite")
    rooli = models.CharField(max_length=20, default="oppilas", choices=[
        ("oppilas", _("Oppilas")),
        ("varastonhoitaja", _("Varastonhoitaja")),
        ("opettaja", _("Opettaja")),
        ("hallinto", _("Hallinto")),
        ])
    vastuuopettaja = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True)

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
    nimike = models.CharField(max_length=50)
    valmistaja = models.CharField(max_length=100, null=True, blank=True)
    kappalemaara = models.IntegerField(validators=[MinValueValidator(1)], default=1, verbose_name="kappalemäärä")
    tuotekuva = models.ImageField(upload_to=None, null=True, blank=True) #BUG Ei vielä toiminnallisuutta
    hankintapaikka = models.CharField(max_length=50, null=True, blank=True)
    hankintavuosi = models.IntegerField(null=True, blank=True)
    hankintapaiva = models.DateField(null=True, blank=True, verbose_name="hankintapäivä")
    hankintahinta = models.FloatField(null=True, blank=True)
    laskun_numero = models.IntegerField(null=True, blank=True)
    kustannuspaikka = models.CharField(max_length=10, null=True, blank=True)
    takuuaika = models.DateField(null=True, blank=True, verbose_name="takuun päättymispäivä")
    varaston_nimi = models.ForeignKey(Varasto, on_delete=models.RESTRICT)

    class Meta:
        verbose_name_plural = "Tuotteet"

    def __str__(self):
        return self.nimike


class Varastotapahtuma(models.Model):
    tuote = models.ForeignKey(Tuote, on_delete=models.RESTRICT)
    maara = models.IntegerField(validators=[MinValueValidator(1)], default=1, verbose_name="määrä")
    arkistotunnus = models.CharField(max_length=50)
    varasto = models.ForeignKey(Varasto, on_delete=models.RESTRICT)
    aikaleima = models.DateField(auto_now=True)
    palautuspaiva = models.DateField(verbose_name="palautuspäivä")
    asiakas = models.ForeignKey(Henkilo, related_name="asiakas", on_delete=models.RESTRICT)
    varastonhoitaja = models.ForeignKey(Henkilo, related_name="varastonhoitaja", on_delete=models.RESTRICT)

    class Meta:
        verbose_name_plural = "Varastotapahtumat"
