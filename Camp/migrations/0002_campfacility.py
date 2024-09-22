# Generated by Django 5.0.4 on 2024-08-28 05:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Camp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CampFacility',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('facility_name', models.CharField(choices=[('Bed', 'Bed'), ('Tent', 'Tent'), ('Food', 'Food'), ('Stool', 'Stool'), ('SleepingBag', 'Sleeping Bag'), ('Lantern', 'Lantern'), ('CampFire', 'Camp Fire'), ('FirstAid', 'First Aid Kit'), ('CookingGear', 'Cooking Gear'), ('Water', 'Water Supply')], max_length=100)),
                ('quantity_available', models.PositiveIntegerField(default=0)),
                ('price_per_item', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('description', models.TextField(blank=True, null=True)),
                ('camp', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='facilities', to='Camp.camp')),
            ],
        ),
    ]
