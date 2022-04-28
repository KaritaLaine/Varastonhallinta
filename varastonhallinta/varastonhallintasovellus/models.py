import datetime
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser

from django.db.models import Q

from django.core.validators import MinValueValidator


class Henkilo(AbstractUser):
    email = models.EmailField(max_length=254, default=None, verbose_name="sähköpostiosoite")
    rooli = models.CharField(max_length=20, default="oppilas", choices=[
        ("oppilas", _("Oppilas")),
        ("varastonhoitaja", _("Varastonhoitaja")),
        ("opettaja", _("Opettaja")),
        ("hallinto", _("Hallinto")),
        ])
    vastuuopettaja = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True, limit_choices_to=Q(rooli__icontains="opettaja"))

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


def pieni_paiva_validaattori(arvo):
    if arvo < datetime.date.today():
        raise ValidationError("Et voi valita päivää menneisyydestä")
    return arvo


class Tuote(models.Model):

    def hankintapaiva_validaattori(arvo):
        if arvo > datetime.date.today():
            raise ValidationError("Hankintapäivä ei voi olla tulevaisuudessa")
        return arvo

    viivakoodi = models.CharField(max_length=30)
    nimike = models.CharField(max_length=100)
    valmistaja = models.CharField(max_length=100, null=True, blank=True)
    kappalemaara = models.IntegerField(validators=[MinValueValidator(1)], default=1, verbose_name="kappalemäärä")
    tuotekuva = models.ImageField(upload_to="tuotekuvat", blank=True, default="default.png")
    tuoteryhma = models.ForeignKey(Tuoteryhma, on_delete=models.RESTRICT)
    hankintapaikka = models.CharField(max_length=100, null=True, blank=True)
    hankintapaiva = models.DateField(null=True, blank=True, validators=[hankintapaiva_validaattori], verbose_name="hankintapäivä")
    hankintahinta = models.DecimalField(validators=[MinValueValidator(0)], decimal_places=2, max_digits=8, null=True, blank=True)
    laskun_numero = models.IntegerField(null=True, blank=True)
    kustannuspaikka = models.CharField(max_length=30, null=True, blank=True)
    takuuaika = models.DateField(null=True, blank=True, validators=[pieni_paiva_validaattori], verbose_name="takuun päättymispäivä")

    class Meta:
        verbose_name_plural = "Tuotteet"

    def __str__(self):
        return self.nimike


class Varastotapahtuma(models.Model):
    tuote = models.ForeignKey(Tuote, on_delete=models.RESTRICT)
    maara = models.IntegerField(validators=[MinValueValidator(1)], default=1, verbose_name="määrä")
    arkistotunnus = models.CharField(max_length=50)
    varasto = models.ForeignKey(Varasto, on_delete=models.RESTRICT)
    aikaleima = models.DateField(default=datetime.date.today)
    palautuspaiva = models.DateField(verbose_name="palautuspäivä", validators=[pieni_paiva_validaattori])
    asiakas = models.ForeignKey(Henkilo, related_name="asiakas", on_delete=models.RESTRICT)
    varastonhoitaja = models.ForeignKey(Henkilo, related_name="varastonhoitaja", on_delete=models.RESTRICT)

    class Meta:
        verbose_name_plural = "Varastotapahtumat"
