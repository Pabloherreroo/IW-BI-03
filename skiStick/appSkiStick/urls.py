from django.urls import path
from .views import (
    EstacionListView,
    EstacionDetailView,
    LocalizacionListView,
    LocalizacionDetailView,
    PistaListView,
    PistaDetailView,
    HomeView,
    EstacionFilterView,
)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('estaciones/', EstacionListView.as_view(), name='estacion_list'),
    path('estacion/<int:pk>/', EstacionDetailView.as_view(), name='estacion_detail'),
    path('localizaciones/', LocalizacionListView.as_view(), name='localizacion_list'),
    path('localizacion/<int:pk>/', LocalizacionDetailView.as_view(), name='localizacion_detail'),
    path('pistas/', PistaListView.as_view(), name='pista_list'),
    path('pista/<int:pk>/', PistaDetailView.as_view(), name='pista_detail'),
    path('', HomeView.as_view(), name='home'),
    path('estaciones/filtrar/', EstacionFilterView.as_view(), name='estacion_filter'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
