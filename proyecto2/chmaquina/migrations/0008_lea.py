# Generated by Django 2.2.1 on 2020-05-18 19:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chmaquina', '0007_auto_20200516_1725'),
    ]

    operations = [
        migrations.CreateModel(
            name='lea',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lea', models.TextField(blank=True, null=True)),
            ],
        ),
    ]
