from .models import Localizacion  # Importa el modelo de Localizacion
from django import forms
from .models import Incidente

class IncidenteForm(forms.ModelForm):
    class Meta:
        model = Incidente
        fields = ['ubicacion_pista', 'descripcion', 'fecha_hora', 'fotos', 'datos_contacto']
        widgets = {
            'ubicacion_pista': forms.Select(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control'}),
            'fecha_hora': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'fotos': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'datos_contacto': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'ubicacion_pista': 'Localizacion',
            'descripcion': 'Descripcion del incidente',
            'fecha_hora': 'Fecha y hora del incidente',
            'fotos': 'Fotos del incidente (opcional)',
            'datos_contacto': 'Datos de contacto (opcional)',
        }
