from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, TemplateView
from .models import Estacion, Localizacion, Pista

class HomeView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['estaciones_destacadas'] = {
            'Andorra': Estacion.objects.filter(localizacion__nombre='Andorra').order_by('-km_pistas').first(),
            'Pirineo Catalán': Estacion.objects.filter(localizacion__nombre='Pirineo Catalán').order_by('-km_pistas').first(),
            # Agregar localizaciones aquí
        }
        return context


# Lista de estaciones
class EstacionListView(ListView):
    model = Estacion
    template_name = "estacion_list.html"
    context_object_name = "estaciones"

# Detalle de una estación
class EstacionDetailView(DetailView):
    model = Estacion
    template_name = "estacion_detail.html"
    context_object_name = "estacion"

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

# Lista de pistas
class PistaListView(ListView):
    model = Pista
    template_name = "pista_list.html"
    context_object_name = "pistas"

# Detalle de una pista
class PistaDetailView(DetailView):
    model = Pista
    template_name = "pista_detail.html"
    context_object_name = "pista"
