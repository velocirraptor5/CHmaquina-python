# Generated by Django 2.2.1 on 2020-05-19 15:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chmaquina', '0022_auto_20200519_0944'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='archivo',
            name='leaLea',
        ),
        migrations.AlterField(
            model_name='lea',
            name='leaLea',
            field=models.TextField(null=True),
        ),
    ]
