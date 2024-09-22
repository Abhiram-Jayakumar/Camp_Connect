# Generated by Django 5.0.4 on 2024-08-28 06:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Camp', '0006_alter_campimage_camp'),
    ]

    operations = [
        migrations.CreateModel(
            name='CampPackage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('package_name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('duration', models.CharField(blank=True, max_length=100, null=True)),
                ('availability', models.BooleanField(default=True)),
                ('camp', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='packages', to='Camp.camp')),
            ],
        ),
    ]
