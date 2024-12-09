import json
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, TemplateView
from .models import Estacion, Localizacion, TipoDePista, EstacionTipoDePista
from django.db.models import Count, F
from django.db.models.functions import Abs
from django.conf import settings
from django.core.serializers.json import DjangoJSONEncoder
from django.urls import reverse



class HomeView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Crear diccionario dinámico para estaciones mas largas de cada sitio
        estaciones_destacadas = {}
        for localizacion in Localizacion.objects.all():
            estacion_mas_larga = Estacion.objects.filter(localizacion=localizacion).order_by('-km_pistas').first()
            if estacion_mas_larga:
                estaciones_destacadas[localizacion.nombre] = estacion_mas_larga

        context['estaciones_destacadas'] = estaciones_destacadas
        context['localizaciones'] = Localizacion.objects.all()
        context['tipos_de_pista'] = TipoDePista.objects.all()
        context['LANGUAGES'] = settings.LANGUAGES
        context['LANGUAGE_CODE'] = self.request.LANGUAGE_CODE
        return context


# Detalle de una estación
class EstacionDetailView(DetailView):
    model = Estacion
    template_name = "estacion_detail.html"
    context_object_name = "estacion"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        estacion = self.get_object()
        #Obtener el número de pistas por tipo para esta estación
        tipos_con_cantidad = (
            EstacionTipoDePista.objects.filter(estacion=estacion)
    .       values('tipo_de_pista__id', 'tipo_de_pista__nombre', 'cantidad')
        )
        #print("Tipos con cantidad:", list(tipos_con_cantidad))
        #-- Serializar datos para el gráfico
        context['tipos_con_cantidad'] = json.dumps(
            list(tipos_con_cantidad), cls=DjangoJSONEncoder
        )
        # Añadir la URL para cada tipo de pista
        for tipo in tipos_con_cantidad:
            tipo['url'] = reverse('pista_detail', args=[tipo['tipo_de_pista__id']])

        #print("Tipos con cantidad:", list(tipos_con_cantidad))

        # Serializar los datos para el gráfico
        context['tipos_con_cantidad'] = json.dumps(list(tipos_con_cantidad), cls=DjangoJSONEncoder)

        #Indicaremos como sugerencia la estación más cercana en km de pistas de la misma cadena (excluyendo la actual)
        estacion_similar = Estacion.objects.filter(
            localizacion=estacion.localizacion
        ).exclude(id=estacion.id).annotate(
            diferencia_km=Abs(F('km_pistas') - estacion.km_pistas)
        ).order_by('diferencia_km').first()  
        context['estacion_similar'] = estacion_similar

        context['LANGUAGES'] = settings.LANGUAGES
        context['LANGUAGE_CODE'] = self.request.LANGUAGE_CODE

        return context

#Mapa de localizaciones  
class LocalizacionListView(ListView):
   model = Localizacion     
   template_name = "localizacion_list.html"
   context_object_name = "localizaciones"   

   def get_context_data(self, **kwargs):
       context = super().get_context_data(**kwargs)
       # Serializar el QuerySet a una lista de diccionarios
       localizaciones = Localizacion.objects.all().values('id', 'nombre', 'descripcion', 'latitud', 'longitud')
       context['localizaciones_json'] = json.dumps(list(localizaciones))
    

       context['LANGUAGES'] = settings.LANGUAGES
       context['LANGUAGE_CODE'] = self.request.LANGUAGE_CODE
       
       return context

# Detalle de una localizacion     
class LocalizacionDetailView(DetailView):
   model = Localizacion
   template_name = "localizacion_detail.html"   
   context_object_name = "localizacion"
   
   def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Obtener todas las estaciones asociadas a esta localizacion
        context['estaciones'] = self.object.estaciones.all()
        context['LANGUAGES'] = settings.LANGUAGES
        context['LANGUAGE_CODE'] = self.request.LANGUAGE_CODE
        return context


# Lista de tipos de pistas
class PistaListView(ListView):
    model = TipoDePista
    template_name = "pista_list.html"
    context_object_name = "pistas"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['LANGUAGES'] = settings.LANGUAGES
        context['LANGUAGE_CODE'] = self.request.LANGUAGE_CODE
        return context

# Detalle de tipo de pista
class PistaDetailView(DetailView):
    model = TipoDePista
    template_name = "pista_detail.html"
    context_object_name = "pista"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Obtener el número de pistas de ese tipo para cada estación
        context['estaciones_con_cantidad'] = EstacionTipoDePista.objects.filter(tipo_de_pista=self.object)
        context['LANGUAGES'] = settings.LANGUAGES
        context['LANGUAGE_CODE'] = self.request.LANGUAGE_CODE
        return context

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
        context['LANGUAGES'] = settings.LANGUAGES
        context['LANGUAGE_CODE'] = self.request.LANGUAGE_CODE
        return context
    
