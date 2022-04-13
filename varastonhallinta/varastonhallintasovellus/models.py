from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser

from django.core.validators import MinValueValidator


class Henkilo(AbstractUser):
    email = models.EmailField(max_length=254, default=None, verbose_name="sähköpostiosoite")
    rooli = models.CharField(max_length=20, default="oppilas", choices=[
        ("oppilas", _("Oppilas")),
        ("varastonjoitaja", _("Varastonjoitaja")),
        ("opettaja", _("Opettaja")),
        ("hallinto", _("Hallinto")),
        ])
    vastuuopettaja = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        permissions = (
            ("varastonjoitaja", "Varastonhoitaja"),
            ("opettaja", "Opettaja"),
            ("hallinto", "Hallinto"),
        )

    REQUIRED_FIELDS = ["email", "first_name", "last_name"]

    def __str__(self):
        return self.first_name + " " + self.last_name


class Varastotyyppi(models.Model):
    nimi = models.CharField(max_length=30)

    class Meta:
        verbose_name_plural = "Varastotyypit"

    def __str__(self):
        return self.nimi


class Varasto(models.Model):
    nimi = models.CharField(max_length=30)
    varastotyyppi = models.ForeignKey(Varastotyyppi, on_delete=models.RESTRICT) # MIETITÄÄN VIELÄ!

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
    viivakoodi = models.CharField(primary_key=True, max_length=30)
    tuote_id = models.IntegerField()
    nimike = models.CharField(max_length=50)
    kappalemaara = models.IntegerField(validators=[MinValueValidator(1)], default=1)
    tuotekuva = models.ImageField(upload_to=None, null=True, blank=True) #BUG Ei vielä toiminnallisuutta
    hankintapaikka = models.CharField(max_length=50, null=True, blank=True)
    hankintavuosi = models.IntegerField(null=True, blank=True)
    hankintahinta = models.FloatField(null=True, blank=True)
    laskun_numero = models.IntegerField(null=True, blank=True)
    kustannuspaikka = models.CharField(max_length=10, null=True, blank=True)
    takuuaika = models.DateTimeField(null=True, blank=True)
    varaston_nimi = models.ForeignKey(Varasto, related_name="tuotesijainti", on_delete=models.RESTRICT)

    class Meta:
        verbose_name_plural = "Tuotteet"

    def __str__(self):
        return self.nimike


class Varastotapahtuma(models.Model):
    tuote = models.ForeignKey(Tuote, on_delete=models.RESTRICT)
    maara = models.IntegerField(default=1)
    arkistotunnus = models.CharField(max_length=50)
    varastosta = models.ForeignKey(Varasto, on_delete=models.RESTRICT, related_name="varastosta")
    varastoon = models.ForeignKey(Varasto, on_delete=models.RESTRICT, related_name="varastoon")
    aikaleima = models.DateTimeField(auto_now=True)
    palautuspaiva = models.DateTimeField()
    asiakas = models.ForeignKey(Henkilo, related_name="asiakas", on_delete=models.RESTRICT)
    varastonhoitaja = models.ForeignKey(Henkilo, related_name="varastonhoitaja", on_delete=models.RESTRICT)

    class Meta:
        verbose_name_plural = "Varastotapahtumat"
