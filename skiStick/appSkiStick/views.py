from urllib import request
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, TemplateView
from .models import Estacion, Localizacion, TipoDePista, EstacionTipoDePista
from django.db.models import F
from django.db.models.functions import Abs


class HomeView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['estaciones_destacadas'] = {
            #Pongo la primera de cada cadena montañosa
            'Andorra': Estacion.objects.filter(localizacion__nombre='Andorra').order_by('-km_pistas').first(),
            'Pirineo Catalán': Estacion.objects.filter(localizacion__nombre='Pirineo Catalán').order_by('-km_pistas').first(),
            'Pirineo Aragonés': Estacion.objects.filter(localizacion__nombre='Pirineo Aragonés').order_by('-km_pistas').first(),
            'Sistema Penibético': Estacion.objects.filter(localizacion__nombre='Sistema Penibético').order_by('-km_pistas').first(),
            'Cordillera Cantábrica': Estacion.objects.filter(localizacion__nombre='Cordillera Cantábrica').order_by('-km_pistas').first(),
            'Sistema Ibérico': Estacion.objects.filter(localizacion__nombre='Sistema Ibérico').order_by('-km_pistas').first(),
            'Sierra de Guadarrama': Estacion.objects.filter(localizacion__nombre='Sierra de Guadarrama').order_by('-km_pistas').first(),
        }
        context['localizaciones'] = Localizacion.objects.all()
        context['tipos_de_pista'] = TipoDePista.objects.all()
        return context


# Detalle de una estación
class EstacionDetailView(DetailView):
    model = Estacion
    template_name = "estacion_detail.html"
    context_object_name = "estacion"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Obtener el número de pistas por tipo para esta estación
        estacion = self.get_object()
        tipos_con_cantidad = EstacionTipoDePista.objects.filter(estacion=estacion)
        context['tipos_con_cantidad'] = tipos_con_cantidad

        #Indicaremos como sugerencia la estación más cercana en km de pistas de la misma cadena (excluyendo la actual)
        estacion_similar = Estacion.objects.filter(
            localizacion=estacion.localizacion
        ).exclude(id=estacion.id).annotate(
            diferencia_km=Abs(F('km_pistas') - estacion.km_pistas)
        ).order_by('diferencia_km').first()  
        context['estacion_similar'] = estacion_similar

        return context

# Lista de localizaciones
class LocalizacionListView(ListView):
    model = Localizacion
    template_name = "localizacion_list.html"
    context_object_name = "localizaciones"

# Detalle de una localización
class LocalizacionDetailView(DetailView):
    model = Localizacion
    template_name = "localizacion_detail.html"
    context_object_name = "localizacion"

# Lista de tipos de pistas
class PistaListView(ListView):
    model = TipoDePista
    template_name = "pista_list.html"
    context_object_name = "pistas"

# Detalle de tipo de pista
class PistaDetailView(DetailView):
    model = TipoDePista
    template_name = "pista_detail.html"
    context_object_name = "pista"

# Lista de estaciones + filtro por localización y/o tipo de pista
class EstacionListView(ListView):
    model = Estacion
    template_name = "estacion_list.html"
    context_object_name = "estaciones"

    def get_queryset(self):
        queryset = Estacion.objects.all()
        localizacion_id = self.request.GET.get("localizacion")
        tipo_de_pista_id = self.request.GET.get("tipo_de_pista")
        
        if localizacion_id:
            queryset = queryset.filter(localizacion_id=localizacion_id)
                   
        # Obtenemos las estaciones que tienen el tipo de pista seleccionado a través del modelo de la relación
        if tipo_de_pista_id:
            estaciones_con_tipo = EstacionTipoDePista.objects.filter(
                tipo_de_pista_id=tipo_de_pista_id
            ).values_list('estacion_id', flat=True)
            queryset = queryset.filter(id__in=estaciones_con_tipo)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Agregar localizaciones y tipos de pista al contexto
        context['localizaciones'] = Localizacion.objects.all()
        context['tipos_de_pista'] = TipoDePista.objects.all()
        return 
    """
    class EstacionFilterView(ListView):
        model = Estacion
        template_name = 'estacion_filter.html' 
        context_object_name = 'estaciones'

        def get_queryset(self):
            # Agregar lógica para filtrar estaciones
            query = self.request.GET.get('q')
            if query:
                return Estacion.objects.filter(nombre__icontains=query)
            return Estacion.objects.all()

        """