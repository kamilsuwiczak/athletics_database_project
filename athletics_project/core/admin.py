from django.contrib import admin
from .models import Konkurencje, Panstwa, RekordySwiata, RekordyZyciowe, ReprezentanciZawodnikow, Stadiony, StatusyWynikow, Trenerzy, TrenerzyZawodnicy, TypyZawodow, Wyniki, Zawodnicy, Zawody

@admin.register(Konkurencje)
class KonkurencjeAdmin(admin.ModelAdmin):
    list_display = ['id_konkurencji', 'nazwa', 'rodzaj']
    search_fields = ['nazwa', 'rodzaj']

@admin.register(Panstwa)
class PanstwaAdmin(admin.ModelAdmin):
    list_display = ['id_panstwa', 'nazwa', 'kod_iso']
    search_fields = ['nazwa', 'kod_iso']

@admin.register(RekordySwiata)
class RekordySwiataAdmin(admin.ModelAdmin):
    list_display = ['id_rekordu', 'id_konkurencji', 'rezultat', 'data_rezultatu', 'id_zawodnika']
    search_fields = ['id_konkurencji__nazwa', 'rezultat', 'id_zawodnika__imie', 'id_zawodnika__nazwisko']

@admin.register(RekordyZyciowe)
class RekordyZycioweAdmin(admin.ModelAdmin):
    list_display = ['id_rekordu_zyciowego', 'id_zawodnika', 'id_konkurencji', 'rezultat', 'data_rezultatu', 'wynik_punktowy']
    search_fields = ['id_zawodnika__imie', 'id_zawodnika__nazwisko', 'id_konkurencji__nazwa']

@admin.register(ReprezentanciZawodnikow)
class ReprezentanciZawodnikowAdmin(admin.ModelAdmin):
    list_display = ['id_reprezentanta', 'imie', 'nazwisko', 'adres_email']
    search_fields = ['imie', 'nazwisko', 'adres_email']

@admin.register(Stadiony)
class StadionyAdmin(admin.ModelAdmin):
    list_display = ['id_stadionu', 'nazwa', 'miasto', 'id_panstwa']
    search_fields = ['nazwa', 'miasto', 'id_panstwa__nazwa']

@admin.register(StatusyWynikow)
class StatusyWynikowAdmin(admin.ModelAdmin):
    list_display = ['id_statusu', 'status_wyniku']
    search_fields = ['status_wyniku']

class TrenerzyZawodnicyInline(admin.TabularInline):
    model = TrenerzyZawodnicy
    extra = 1

@admin.register(Trenerzy)
class TrenerzyAdmin(admin.ModelAdmin):
    list_display = ['id_trenera', 'imie', 'nazwisko', 'adres_email']
    inlines = [TrenerzyZawodnicyInline]


@admin.register(Zawodnicy)
class ZawodnicyAdmin(admin.ModelAdmin):
    list_display = ['id_zawodnika', 'imie', 'nazwisko', 'data_urodzenia', 'plec', 'id_panstwa', 'id_reprezentanta']
    search_fields = ['imie', 'nazwisko', 'id_panstwa__nazwa', 'plec', 'id_reprezentanta__imie', 'id_reprezentanta__nazwisko']
    inlines = [TrenerzyZawodnicyInline]

@admin.register(TypyZawodow)
class TypyZawodowAdmin(admin.ModelAdmin):
    list_display = ['id_typu_zawodow', 'nazwa_typu']
    search_fields = ['nazwa_typu']


@admin.register(Zawody)
class ZawodyAdmin(admin.ModelAdmin):
    list_display = ['id_zawody', 'nazwa', 'data_rozpoczecia', 'data_zakonczenia', 'id_typu_zawodow', 'id_stadionu', 'id_panstwa', ]
    search_fields = ['nazwa', 'id_typu_zawodow__nazwa', 'id_stadionu__nazwa']

@admin.register(Wyniki)
class WynikiAdmin(admin.ModelAdmin):
    list_display = ['id_wyniku', 'id_zawody', 'id_zawodnika', 'id_konkurencji', 'rezultat', 'data_rezultatu', 'id_statusu', 'miejsce']
    search_fields = ['id_zawody__nazwa', 'id_zawodnika__imie', 'id_zawodnika__nazwisko', 'id_konkurencji__nazwa', 'id_statusu__status_wyniku']
# Register your models here.

