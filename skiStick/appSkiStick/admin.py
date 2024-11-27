from django.contrib import admin
from django.contrib.auth.models import Group, User
from django.contrib.auth.admin import UserAdmin
from django.contrib.admin.sites import AdminSite
from .models import Estacion, Localizacion, TipoDePista, EstacionTipoDePista

class EstacionTipoDePistaInline(admin.TabularInline):
    model = EstacionTipoDePista
    extra = 1

class EstacionAdmin(admin.ModelAdmin):
    inlines = [EstacionTipoDePistaInline]

    def has_view_permission(self, request, obj=None):
        # Siempre permitir a superusuarios
        if request.user.is_superuser:
            return True
        return request.user.has_perm("appSkiStick.view_estacion")

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return request.user.has_perm("appSkiStick.change_estacion")

    def has_module_permission(self, request):
        # Controla el módulo en la barra lateral
        return self.has_view_permission(request)


class TipoDePistaAdmin(admin.ModelAdmin):
    def has_view_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return request.user.has_perm("appSkiStick.view_tipodepista")

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return request.user.has_perm("appSkiStick.change_tipodepista")

    def has_module_permission(self, request):
        return self.has_view_permission(request)

admin.site.register(Localizacion)
admin.site.register(TipoDePista, TipoDePistaAdmin)
admin.site.register(Estacion, EstacionAdmin)

class CustomAdminSite(AdminSite):
    site_header = "SkiStick Admin"
    site_title = "SkiStick Admin Portal"
    index_title = "Bienvenido al Portal de Administración SkiStick"

    # Incluir el CSS personalizado
    def get_urls(self):
        from django.urls import path
        urls = super().get_urls()
        from django.contrib.staticfiles.urls import staticfiles_urlpatterns
        return urls + staticfiles_urlpatterns()

    def each_context(self, request):
        context = super().each_context(request)
        context['css'] = '/static/admin/css/admin.css'
        return context

admin.site = CustomAdminSite()
