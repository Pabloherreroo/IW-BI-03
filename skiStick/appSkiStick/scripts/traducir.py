from deep_translator import GoogleTranslator
from appSkiStick.models import Estacion, Localizacion, TipoDePista
from deep_translator.exceptions import TranslationNotFound

def traducir_estaciones():
    estaciones = Estacion.objects.all()
    for estacion in estaciones:
        if not estacion.descripcion_en:  # Solo traduce si el campo en inglés está vacío
            estacion.descripcion_en = GoogleTranslator(source='es', target='en').translate(estacion.descripcion)
            estacion.save()
            print(f"Traducido Estación: {estacion.nombre} -> {estacion.descripcion_en}")

def traducir_localizaciones():
    localizaciones = Localizacion.objects.all()
    for localizacion in localizaciones:
        if not localizacion.descripcion_en:  # Solo traduce la descripción
            localizacion.descripcion_en = GoogleTranslator(source='es', target='en').translate(localizacion.descripcion)
            localizacion.save()
            print(f"Traducido Localización: {localizacion.nombre} -> {localizacion.descripcion_en}")

def traducir_tipos_de_pista():
    tipos_de_pista = TipoDePista.objects.all()
    for tipo in tipos_de_pista:
        if not tipo.descripcion_corta_en:  # Traducción de descripción corta
            tipo.descripcion_corta_en = GoogleTranslator(source='es', target='en').translate(tipo.descripcion_corta or "")
        if not tipo.descripcion_larga_en:  # Traducción de descripción larga
            tipo.descripcion_larga_en = GoogleTranslator(source='es', target='en').translate(tipo.descripcion_larga or "")
        tipo.save()
        print(f"Traducido Tipo de Pista: {tipo.nombre} -> {tipo.descripcion_corta_en}, {tipo.descripcion_larga_en}")

