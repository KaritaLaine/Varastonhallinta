from django.contrib import admin

from .models import Varastotyyppi, Varasto, Henkilo, Tuoteryhma, Tuote, Varastotapahtuma


@admin.register(Varastotyyppi)
class TuoteAdmin(admin.ModelAdmin):
    pass


@admin.register(Varasto)
class VarastoAdmin(admin.ModelAdmin):
    pass


@admin.register(Henkilo)
class HenkiloAdmin(admin.ModelAdmin):
    pass


@admin.register(Tuoteryhma)
class TuoteryhmaAdmin(admin.ModelAdmin):
    pass


@admin.register(Tuote)
class TuoteAdmin(admin.ModelAdmin):
    pass


@admin.register(Varastotapahtuma)
class VarastotapahtumaAdmin(admin.ModelAdmin):
    pass