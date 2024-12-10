from django.contrib import admin
from django.contrib.admin.sites import AdminSite
from .models import Estacion, Localizacion, TipoDePista, EstacionTipoDePista
from django.templatetags.static import static
from .models import Incidente

class EstacionTipoDePistaInline(admin.TabularInline):
    model = EstacionTipoDePista
    extra = 1

class EstacionAdmin(admin.ModelAdmin):
    inlines = [EstacionTipoDePistaInline]

    def has_view_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return request.user.has_perm("appSkiStick.view_estacion")

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return request.user.has_perm("appSkiStick.change_estacion")
    
    def has_add_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.has_perm("appSkiStick.add_estacion")

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.has_perm("appSkiStick.delete_estacion")

    def has_module_permission(self, request):
        return self.has_view_permission(request)

    class Media:
        css = {
            'all': ('admin/css/admin.css',) 
        }

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

    class Media:
        css = {
            'all': ('admin/css/admin.css',)
        }

@admin.register(Incidente)
class IncidenteAdmin(admin.ModelAdmin):
    list_display = ('ubicacion', 'fecha_hora', 'descripcion', 'resuelto')
    list_filter = ('resuelto', 'ubicacion_pista')
    search_fields = ('descripcion', 'ubicacion_pista__nombre')
    ordering = ('-fecha_hora',)
    readonly_fields = ('fecha_hora',)

    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.has_perm("appSkiStick.view_incidente")

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.has_perm("appSkiStick.change_incidente")

    def has_add_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.has_perm("appSkiStick.add_incidente")

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.has_perm("appSkiStick.delete_incidente")

    def has_module_permission(self, request):
        return self.has_view_permission(request)
    
    class Media:
        css = {
            'all': ('admin/css/admin.css',)
        }

class CustomAdminSite(AdminSite):
    site_header = "SkiStick Admin"
    site_title = "SkiStick Admin Portal"
    index_title = "Bienvenido al Portal de Administración SkiStick"

    def each_context(self, request):
        context = super().each_context(request)
        context['custom_css'] = static('admin/css/admin.css')
        return context

custom_admin_site = CustomAdminSite(name="custom_admin")

custom_admin_site.register(Localizacion)
custom_admin_site.register(TipoDePista, TipoDePistaAdmin)
custom_admin_site.register(Estacion, EstacionAdmin)
custom_admin_site.register(Incidente, IncidenteAdmin)
