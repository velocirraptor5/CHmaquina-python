# Generated by Django 2.2.1 on 2020-05-19 14:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chmaquina', '0021_archivo_lea'),
    ]

    operations = [
        migrations.RenameField(
            model_name='archivo',
            old_name='lea',
            new_name='leaLea',
        ),
    ]
