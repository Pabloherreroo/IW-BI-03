from modeltranslation.translator import register, TranslationOptions
from .models import Localizacion, TipoDePista, Estacion

# Translation for Localizacion model
@register(Localizacion)
class LocalizacionTranslationOptions(TranslationOptions):
    fields = ('nombre', 'descripcion')  # Fields to be translated

# Translation for TipoDePista model
@register(TipoDePista)
class TipoDePistaTranslationOptions(TranslationOptions):
    fields = ('nombre', 'descripcion_corta', 'descripcion_larga')  # Fields to be translated

# Translation for Estacion model
@register(Estacion)
class EstacionTranslationOptions(TranslationOptions):
    fields = ('nombre', 'descripcion')  # Fields to be translated
