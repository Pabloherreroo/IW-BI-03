from django.db import models
from django.utils.translation import gettext_lazy as _

class Localizacion(models.Model):
    nombre = models.CharField(max_length=100, unique=True, verbose_name=_("Nombre"))
    descripcion = models.TextField(blank=True, null=True, verbose_name=_("Descripción"))
    latitud = models.FloatField(null=True, blank=True, verbose_name=_("Latitud"))
    longitud = models.FloatField(null=True, blank=True, verbose_name=_("Longitud"))
    imagen = models.ImageField(
        upload_to='localizacion/', blank=True, null=True, verbose_name=_("Imagen de la Localización")
    )

    def __str__(self):
        return self.nombre


class TipoDePista(models.Model):
    TIPO_NIVEL = {
        'verde': _("Principiante"),
        'azul': _("Amateur"),
        'roja': _("Avanzado"),
        'negra': _("Experto"),
        'competición': _("Competitivo"),
    }
    TIPO_CHOICES = [
        ('verde', _("Verde")),
        ('azul', _("Azul")),
        ('roja', _("Roja")),
        ('negra', _("Negra")),
        ('competición', _("Competición")),
    ]
    nombre = models.CharField(
        max_length=20, choices=TIPO_CHOICES, unique=True, verbose_name=_("Nombre")
    )
    nivel = models.CharField(max_length=20, editable=False, verbose_name=_("Nivel"))
    bandera = models.ImageField(
        upload_to='pistas/', blank=True, null=True, verbose_name=_("Bandera de la Pista")
    )
    descripcion_corta = models.TextField(blank=True, null=True, verbose_name=_("Descripción Corta"))
    descripcion_larga = models.TextField(blank=True, null=True, verbose_name=_("Descripción Larga"))

    def save(self, *args, **kwargs):
        print(f"Valor de nombre: '{self.nombre}'")  # Imprime el valor exacto de self.nombre
        print(f"Claves en TIPO_NIVEL: {self.TIPO_NIVEL.keys()}")  # Imprime las claves disponibles
        self.nivel = self.TIPO_NIVEL[self.nombre]
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.get_nombre_display()} ({self.nivel})"


class Estacion(models.Model):
    nombre = models.CharField(max_length=100, verbose_name=_("Nombre"))
    localizacion = models.ForeignKey(
        Localizacion,
        on_delete=models.CASCADE,
        related_name="estaciones",
        verbose_name=_("Localización"),
    )
    km_pistas = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        help_text=_("Longitud total esquiable en kilómetros"),
        verbose_name=_("Kilómetros Esquiables"),
    )
    descripcion = models.TextField(blank=True, null=True, verbose_name=_("Descripción"))
    tipos_pista = models.ManyToManyField(
        TipoDePista,
        through='EstacionTipoDePista',
        related_name="estaciones",
        verbose_name=_("Tipos de Pista"),
    )
    imagen = models.ImageField(
        upload_to='estaciones/', blank=True, null=True, verbose_name=_("Imagen")
    )
    imagen_plano = models.ImageField(
        upload_to='estaciones/', blank=True, null=True, verbose_name=_("Plano de las Pistas")
    )

    def __str__(self):
        return self.nombre


class EstacionTipoDePista(models.Model):
    estacion = models.ForeignKey(
        Estacion, on_delete=models.CASCADE, verbose_name=_("Estación")
    )
    tipo_de_pista = models.ForeignKey(
        TipoDePista, on_delete=models.CASCADE, verbose_name=_("Tipo de Pista")
    )
    cantidad = models.PositiveIntegerField(
        default=0, help_text=_("Número de pistas de este tipo en la estación"), verbose_name=_("Cantidad")
    )

    class Meta:
        unique_together = ('estacion', 'tipo_de_pista')  # Evitar duplicados de tipo por estación

    def __str__(self):
        return f"{self.estacion.nombre} - {self.tipo_de_pista.get_nombre_display()}: {self.cantidad} pistas"
