# Generated by Django 3.1.4 on 2021-02-07 18:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('convocatoria', '0002_auto_20210207_1218'),
    ]

    operations = [
        migrations.AddField(
            model_name='aspirantes',
            name='prioritario',
            field=models.BooleanField(default=False),
        ),
    ]
