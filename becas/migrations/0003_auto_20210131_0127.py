# Generated by Django 3.1.4 on 2021-01-31 01:27

import becas.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('becas', '0002_student_img'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='img',
        ),
        migrations.AddField(
            model_name='student',
            name='pic',
            field=models.ImageField(default=1, help_text='Esta fotografía se imprimira en la solicitud y expendiente. Se requiere fotografía tipo pasaporte.', upload_to=becas.models.path_and_rename, verbose_name='Foto de perfil'),
            preserve_default=False,
        ),
    ]