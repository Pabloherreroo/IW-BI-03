from django.db import models

class Localizacion(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre


class Estacion(models.Model):
    nombre = models.CharField(max_length=100)
    localizacion = models.ForeignKey(Localizacion, on_delete=models.CASCADE, related_name="estaciones")
    km_pistas = models.DecimalField(max_digits=5, decimal_places=2, help_text="Longitud total esquiable en kilómetros")
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre


class Pista(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    tipo_de_pista = models.CharField(
        max_length=20,
        help_text="Tipo de pista: Verde, Azul, Roja, Negra o Competición"
    )
    estacion = models.ForeignKey(Estacion, on_delete=models.CASCADE, related_name="pistas")

    def __str__(self):
        return f"{self.nombre} ({self.tipo_de_pista})"