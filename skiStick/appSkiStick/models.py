from django.db import models

class Localizacion(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, null=True)
    latitud = models.FloatField(null=True, blank=True)
    longitud = models.FloatField(null=True, blank=True)
    imagen = models.ImageField(upload_to='localizacion/', blank=True, null=True, verbose_name='imagen_localizacion')

    def __str__(self):
        return self.nombre


class TipoDePista(models.Model):
    TIPO_NIVEL = {
        'verde': 'Principiante',
        'azul': 'Amateur',
        'roja': 'Avanzado',
        'negra': 'Experto',
        'competicion': 'Competitivo',
    }   
    TIPO_CHOICES = [
        ('verde', 'Verde'),
        ('azul', 'Azul'),
        ('roja', 'Roja'),
        ('negra', 'Negra'),
        ('competicion', 'Competición'),
    ]
    nombre = models.CharField(max_length=20, choices=TIPO_CHOICES, unique=True)
    nivel = models.CharField(max_length=20, editable=False)
    bandera = models.ImageField(upload_to='pistas/', blank=True, null=True, verbose_name='bandera_pista')
    descripcion_corta = models.TextField(blank=True, null=True)
    descripcion_larga = models.TextField(blank=True, null=True)

    #Esto se incluye para que al guardar, designe automáticamente el nivel
    def save(self, *args, **kwargs):
        self.nivel = self.TIPO_NIVEL[self.nombre]
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.get_nombre_display()} ({self.nivel})"


class Estacion(models.Model):
    nombre = models.CharField(max_length=100)
    localizacion = models.ForeignKey(Localizacion, on_delete=models.CASCADE, related_name="estaciones")
    km_pistas = models.DecimalField(max_digits=5, decimal_places=2, help_text="Longitud total esquiable en kilómetros")
    descripcion = models.TextField(blank=True, null=True)
    tipos_pista = models.ManyToManyField(TipoDePista, through='EstacionTipoDePista', related_name="estaciones")
    imagen = models.ImageField(upload_to='estaciones/', blank=True, null=True, verbose_name='imagen')
    imagen_plano = models.ImageField(upload_to='estaciones/', blank=True, null=True, verbose_name='imagen_plano')

    def __str__(self):
        return self.nombre

#Tenemos que añadir un modelo de la relacion para que sea posible indicar la cantidad de pistas de cada tipo    
class EstacionTipoDePista(models.Model):
    estacion = models.ForeignKey(Estacion, on_delete=models.CASCADE)
    tipo_de_pista = models.ForeignKey(TipoDePista, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=0, help_text="Número de pistas de este tipo en la estación")

    class Meta:
        unique_together = ('estacion', 'tipo_de_pista')  #Evitamos duplicados de tipo por estación

    def __str__(self):
        return f"{self.estacion.nombre} - {self.tipo_de_pista.get_nombre_display()}: {self.cantidad} pistas"