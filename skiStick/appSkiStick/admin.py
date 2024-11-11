from django.contrib import admin
from .models import Estacion, Localizacion, TipoDePista, EstacionTipoDePista

# Para editar los tipos de pista con cantidad directamente en el admin de Estacion añado este inline
class EstacionTipoDePistaInline(admin.TabularInline):
    model = EstacionTipoDePista
    extra = 1
class EstacionAdmin(admin.ModelAdmin):
    inlines = [EstacionTipoDePistaInline]

admin.site.register(Localizacion)
admin.site.register(TipoDePista)
admin.site.register(Estacion, EstacionAdmin)

