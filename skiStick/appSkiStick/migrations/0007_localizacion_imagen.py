# Generated by Django 5.1.2 on 2024-11-17 18:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appSkiStick', '0006_tipodepista_bandera_tipodepista_descripcion_corta_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='localizacion',
            name='imagen',
            field=models.ImageField(blank=True, null=True, upload_to='localizacion/', verbose_name='imagen_localizacion'),
        ),
    ]