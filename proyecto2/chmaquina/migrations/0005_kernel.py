# Generated by Django 2.2.1 on 2020-05-16 14:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chmaquina', '0004_auto_20200507_1032'),
    ]

    operations = [
        migrations.CreateModel(
            name='Kernel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('memoria', models.IntegerField(blank=True, null=True)),
                ('kernel', models.IntegerField(blank=True, null=True)),
            ],
        ),
    ]
