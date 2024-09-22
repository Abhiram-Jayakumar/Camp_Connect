# Generated by Django 5.0.4 on 2024-08-28 07:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Camp', '0008_delete_camppackage'),
    ]

    operations = [
        migrations.CreateModel(
            name='CampPackage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('package_name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('location', models.TextField()),
                ('camp_start_date', models.DateField(auto_now_add=True)),
                ('camp_end_date', models.DateField()),
                ('booking_start_date', models.DateField(auto_now_add=True)),
                ('booking_end_date', models.DateField()),
                ('max_people', models.PositiveIntegerField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('availability', models.BooleanField(default=True)),
                ('camp', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='packages', to='Camp.camp')),
                ('facilities_provided', models.ManyToManyField(blank=True, related_name='camp_packages', to='Camp.campfacility')),
            ],
        ),
    ]