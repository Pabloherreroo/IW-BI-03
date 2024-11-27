from django.apps import AppConfig
from django.db.models.signals import post_migrate

class AppSkiStickConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "appSkiStick"

    def ready(self):
        # Conectar la señal post_migrate para crear roles después de la migración
        post_migrate.connect(self.create_roles, sender=self)

    def create_roles(self, **kwargs):
        from django.contrib.auth.models import Group, Permission
        from django.contrib.contenttypes.models import ContentType
        from .models import Estacion, TipoDePista

        grupos = {
            "Admin Estaciones": ["change_estacion", "view_estacion"],
            "Admin Tipos de Pista": ["change_tipodepista", "view_tipodepista"],
        }

        modelos = {
            "change_estacion": Estacion,
            "view_estacion": Estacion,
            "change_tipodepista": TipoDePista,
            "view_tipodepista": TipoDePista,
        }

        for grupo_nombre, permisos_codename in grupos.items():
            group, _ = Group.objects.get_or_create(name=grupo_nombre)
            for codename in permisos_codename:
                modelo = modelos[codename]
                content_type = ContentType.objects.get_for_model(modelo)
                permission, _ = Permission.objects.get_or_create(
                    codename=codename, content_type=content_type
                )
                group.permissions.add(permission)

