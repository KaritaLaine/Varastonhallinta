from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Varastotyyppi, Varasto, Henkilo, Tuoteryhma, Tuote, Varastotapahtuma


class HenkiloAdmin(UserAdmin):

    readonly_fields = [
        'date_joined',
    ]
    
    list_display = (
        'username', 'email', 'first_name', 'last_name', 'rooli'
        )

    list_filter = (
        'rooli', 'vastuuopettaja',
    )

    fieldsets = (
        (None, {
            'fields': ('username', 'password')
        }),
        ('Käyttäjätiedot', {
            'fields': ('first_name', 'last_name', 'email')
        }),
        ('Luvat', {
            'fields': (
                'is_active', 'is_staff', 'is_superuser',
                'groups', 'user_permissions'
                )
        }),
        ('Tärkeät päivämäärät', {
            'fields': ('last_login', 'date_joined')
        }),
        ('Lisätiedot', {
            'fields': ('rooli', 'vastuuopettaja',)
        })
    )

    add_fieldsets = (
        (None, {
            'fields': ('username', 'password1', 'password2')
        }),
        ('Personal info', {
            'fields': ('first_name', 'last_name', 'email')
        }),
        ('Permissions', {
            'fields': (
                'is_active', 'is_staff', 'is_superuser',
                'groups', 'user_permissions'
                )
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined')
        }),
        ('Additional info', {
            'fields': ('rooli', 'vastuuopettaja',)
        })
    )

admin.site.register(Henkilo, HenkiloAdmin)


@admin.register(Varastotyyppi)
class TuoteAdmin(admin.ModelAdmin):
    pass


@admin.register(Varasto)
class VarastoAdmin(admin.ModelAdmin):
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