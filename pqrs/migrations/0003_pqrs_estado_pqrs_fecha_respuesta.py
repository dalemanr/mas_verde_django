# Generated by Django 5.0.2 on 2024-03-15 14:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pqrs', '0002_remove_pqrs_tipo'),
    ]

    operations = [
        migrations.AddField(
            model_name='pqrs',
            name='estado',
            field=models.CharField(blank=True, default='Pendiente', max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='pqrs',
            name='fecha_respuesta',
            field=models.DateField(blank=True, null=True),
        ),
    ]
