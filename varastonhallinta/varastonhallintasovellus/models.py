from django.db import models

# Create your models here.
class Varastotyyppi(models.Model):
    varastotyypin_nimi = models.CharField(max_length=30)

    def __str__(self):
        return self.varastotyypin_nimi


class Varasto(models.Model):
    varaston_nimi = models.CharField(max_length=30)
    varastotyyppi_FK = models.ForeignKey(Varastotyyppi, on_delete=models.RESTRICT) # MIETITÄÄN VIELÄ!

    def __str__(self):
        return self.varaston_nimi


class Rooli(models.Model):
    roolinimitys = models.CharField(primary_key=True, max_length=20)

    def __str__(self):
        return self.roolinimitys


class Henkilo(models.Model):
    roolinimitys_FK = models.ForeignKey(Rooli, on_delete=models.RESTRICT)
    email = models.EmailField(max_length=254, default=None)
    etunimi = models.CharField(max_length=20)
    sukunimi = models.CharField(max_length=30)

    def __str__(self):
        return self.etunimi + ' ' + self.sukunimi


class Tuoteryhma(models.Model):
    ryhman_nimi = models.CharField(max_length=50)

    def __str__(self):
        return self.ryhman_nimi


class Tuote(models.Model):
    viivakoodi = models.CharField(primary_key=True, max_length=30)
    tuote_id = models.IntegerField()
    nimike = models.CharField(max_length=50)
    kappalemaara = models.IntegerField()
    tuotekuva = models.ImageField(upload_to=None, null=True, blank=True) #BUG Ei vielä toiminnallisuutta
    hankintapaikka = models.CharField(max_length=50, null=True, blank=True)
    hankintavuosi = models.IntegerField(null=True, blank=True)
    hankintahinta = models.FloatField(null=True, blank=True)
    laskun_numero = models.IntegerField(null=True, blank=True)
    kustannuspaikka = models.CharField(max_length=10, null=True, blank=True)
    takuuaika = models.DateTimeField(null=True, blank=True)
    varaston_nimi = models.ForeignKey(Varasto, related_name='tuotesijainti', on_delete=models.RESTRICT)

    def __str__(self):
        return self.nimike


class Varastotapahtuma(models.Model):
    palautuspaiva = models.DateTimeField()
    viivakoodi_FK = models.ForeignKey(Tuote, on_delete=models.RESTRICT)
    maara = models.IntegerField(default=1)
    arkistotunnus = models.CharField(max_length=50)
    varasto_FK = models.ForeignKey(Varasto, related_name='varastofk', on_delete=models.RESTRICT)
    aikaleima = models.DateTimeField()
    asiakas_FK = models.ForeignKey(Henkilo, related_name='asiakas', on_delete=models.RESTRICT)
    varastonhoitaja_FK = models.ForeignKey(Henkilo, related_name='varastonhoitaja', on_delete=models.RESTRICT)