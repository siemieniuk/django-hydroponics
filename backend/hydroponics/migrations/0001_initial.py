# Generated by Django 5.0 on 2024-03-21 07:38

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='HydroponicSystem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=1000)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Measurement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('when_measured', models.DateTimeField(auto_now_add=True)),
                ('water_ph', models.FloatField(null=True)),
                ('water_tds', models.FloatField(null=True)),
                ('water_temp', models.FloatField(null=True)),
                ('hydroponic_system', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='measurements', to='hydroponics.hydroponicsystem')),
            ],
            options={
                'ordering': ['-when_measured'],
                'indexes': [models.Index(fields=['hydroponic_system', '-when_measured'], name='hydroponics_hydropo_8fa71b_idx')],
            },
        ),
    ]
