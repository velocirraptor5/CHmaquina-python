# Generated by Django 3.0.4 on 2020-06-27 21:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chmaquina', '0025_auto_20200520_1703'),
    ]

    operations = [
        migrations.CreateModel(
            name='MetodoPlanificacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('metodo', models.TextField(blank=True, null=True)),
            ],
        ),
    ]
