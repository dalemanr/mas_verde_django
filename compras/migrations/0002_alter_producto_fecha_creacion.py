# Generated by Django 5.0.2 on 2024-02-24 16:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compras', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producto',
            name='fecha_creacion',
            field=models.DateField(auto_now_add=True),
        ),
    ]
